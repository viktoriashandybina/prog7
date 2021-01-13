import datetime

from flask import Markup
from markdown import markdown
from micawber import parse_html
from peewee import *

from app import db, oembed

class Note(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def html(self):
        html = parse_html(
            markdown(self.content),
            oembed,
            maxwidth=300,
            urlize_all=True)
        return Markup(html)
