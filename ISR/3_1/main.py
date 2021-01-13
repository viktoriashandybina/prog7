from flask import Flask, render_template, request
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")

db = client.db
notes = db.notes

notes_array = []


@app.route('/')
def main_page():
    notes_array = notes.find()
    return render_template("index.html", notes=notes_array)


@app.route('/add', methods=["POST"])
def add():
    title = request.form["title"]
    text = request.form["text"]
    notes.insert_one({"title": title, "text": text})
    notes_array = notes.find()
    return render_template("index.html", notes=notes_array)


@app.route('/delete')
def deleteAll():
    notes.drop()
    return render_template("index.html", notes=notes_array)


if __name__ == '__main__':
    app.run()
