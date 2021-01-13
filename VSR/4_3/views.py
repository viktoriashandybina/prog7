from flask import abort, render_template, request, redirect, url_for

from app import app
from models import Note

@app.route('/', methods=['GET', 'POST'])
def homepage():
    notes = Note.select()
    if request.method == 'POST':
        if request.form.get('content'):
            note = Note.create(content=request.form['content'])
            rendered = render_template('note.html', note=note)
            return render_template('homepage.html', notes=notes)


    return render_template('homepage.html', notes=notes)

@app.route('/delete/<int:pk>/', methods=['POST', 'GET'])
def delete_note(pk):
    try:
        note = Note.get(Note.id == pk)
    except Note.DoesNotExist:
        abort(404)
    note.delete_instance()
    note.save()
    return redirect(url_for('homepage'))


@app.route('/update/<int:pk>/', methods=['POST', 'GET'])
def update_note(pk):
    if request.method == 'POST':
        if request.form.get('updated_parts'):
            query = Note.update(content=request.form['updated_parts']).where(Note.id==pk)
            query.execute()
            return redirect(url_for('homepage'))


    try:
        note = Note.get(Note.id == pk)
    except Note.DoesNotExist:
        abort(404)

    return render_template('update.html', note=note)

