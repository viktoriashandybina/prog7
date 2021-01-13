#!/usr/bin/env python3

import os
import json
import base64
import hashlib
from bson.objectid import ObjectId
from datetime import datetime, timedelta

from motor.motor_tornado import MotorClient
import tornado.web
import tornado.ioloop
import tornado.websocket

MONGO_HOST = os.environ.get("MONGO_HOST", "127.0.0.1")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", 8888))
MESSAGES_SHOW_LIMIT = 10


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("sessid")

    async def do_login(self, username, password):
        user = await self.application.db.users.find_one({"username": username})

        if (user is None):
            salt = os.urandom(32)
            hashed_pass = hashlib.pbkdf2_hmac(
                'sha256', password.encode('utf-8'), salt, 100000, dklen=128)
            user = {"username": username, "salt": salt,
                    "hashed_pass": hashed_pass}
            self.application.db.users.insert_one(user)

            session = {}
            session['key'] = os.urandom(16)
            session['username'] = username
            session['expires'] = datetime.now() - timedelta(days=30)
            self.application.db.sessions.insert_one(session)
            self.set_cookie("username", username)
            return session['key']

        password = hashlib.pbkdf2_hmac('sha256', password.encode(
            'utf-8'), user['salt'], 100000, dklen=128)

        if (user['hashed_pass'] != password):
            return None
        else:
            session = await self.application.db.sessions.find_one({'username': username})

            if (session["expires"] < datetime.now()):
                await self.application.db.sessions.delete_one(session)
                session['key'] = os.urandom(16)
                session['username'] = username
                session['expires'] = datetime.now() + timedelta(days=30)
                await self.application.db.sessions.insert_one(session)
            self.set_cookie("username", username)
            return session['key']


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        username = self.get_cookie("username")
        users = await self.application.db.users.find().to_list(None)

        cursor = self.application.db.messages.find().sort('_id', -1).limit(
            MESSAGES_SHOW_LIMIT
        )
        messages = await cursor.to_list(None)
        messages.reverse()
        self.render('index.html', messages=messages,
                    username=username, users=users)


class LogoutHandler(BaseHandler):
    def post(self):
        self.clear_all_cookies()
        self.redirect('/login')


class LoginHandler(BaseHandler):
    async def get(self):
        if not self.current_user:
            self.render("login.html")
        else:
            self.redirect("/")

    async def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        sessid = await self.do_login(username, password)

        if (sessid):
            self.set_secure_cookie("sessid", sessid, expires_days=30)
            self.redirect("/")
        else:
            self.write("Неверное имя пользователя или пароль")


class UserChatHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self, interlocutor):
        username = self.get_cookie("username")
        users = sorted([username, interlocutor])

        private_chat = await self.application.db.private_chats.find_one({
            "users": users})

        if (private_chat is None):
            await self.application.db.private_chats.insert_one({"users": users, "messages": []})
            private_chat = await self.application.db.private_chats.find_one(
                {"users": users})

        self.set_cookie("private_chat_id", str(private_chat["_id"]))
        messages = private_chat['messages']
        self.render('userChat.html', username=username, messages=messages,
                    interlocutor=interlocutor)


class WebSocketPrivate(tornado.websocket.WebSocketHandler):

    def open(self, private_chat_id):
        if (len(self.application.webSocketsPool) < 2):
            self.application.webSocketsPool.append(self)

    def on_message(self, message):
        message_dict = json.loads(message)

        private_chat_id = self.get_cookie("private_chat_id")
        self.application.db.private_chats.update_one(
            {"_id": ObjectId(private_chat_id)}, {'$push': {"messages": message_dict}})

        for key, value in enumerate(self.application.webSocketsPool):
            if value != self:
                value.ws_connection.write_message(message)

    def on_close(self, message=None):
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]


class WebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        self.application.webSocketsPool.append(self)

    def on_message(self, message):
        message_dict = json.loads(message)
        self.application.db.messages.insert(message_dict)
        for key, value in enumerate(self.application.webSocketsPool):
            if value != self:
                value.ws_connection.write_message(message)

    def on_close(self, message=None):
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []
        self.db = MotorClient(MONGO_HOST, MONGO_PORT).chat

        handlers = (
            (r'/', MainHandler),
            (r'/websocket/?', WebSocket),
            (r'/websocket/private/(.*)?', WebSocketPrivate),
            (r'/user/(.+)', UserChatHandler),
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler,
             {'path': 'static/'}),
        )

        settings = dict(
            cookie_secret="super secret for cookie",
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
        )

        super().__init__(handlers, **settings)


application = Application()


if __name__ == '__main__':
    application.listen(LISTEN_PORT)
    print("Server is running on: http://127.0.0.1:{0}".format(LISTEN_PORT))
    tornado.ioloop.IOLoop.instance().start()
