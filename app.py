import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for, abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ejLmgK034H'

#. . .

@app.route('/')
def index():
    conn = get_db_connection()
    db_notes = conn.execute('SELECT id, created, content FROM notes ORDER BY created DESC;').fetchall()
    conn.close()

    notes = []
    for note in db_notes:
        note = dict(note)
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)

    return render_template('index.html', notes=notes)

@app.route('/<int:id>', methods=['GET', 'DELETE'])
def details(id):
    conn = get_db_connection()
    if request.method == 'DELETE':
        conn.execute(f'DELETE FROM notes WHERE id = {str(id)};')
        conn.commit()
        conn.close()
        return {'status': True}
    db_note = conn.execute(f'SELECT id, created, content FROM notes WHERE id = {str(id)};').fetchall()
    conn.close()

    if len(db_note) == 0:
        return abort(404, description="Resource not found")

    note = dict(db_note[0])
    note['content'] = markdown.markdown(note['content'])

    return render_template('details.html', note=note)

@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
    conn = get_db_connection()
    db_note = conn.execute(f'SELECT id, created, content FROM notes WHERE id = {str(id)};').fetchall()
    conn.close()

    if len(db_note) == 0:
        return abort(404, description="Resource not found")

    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        content = request.form['content']
        sql = 'UPDATE notes SET content=? WHERE id = ?'
        cur.execute(sql, (content, id, ))
        conn.commit()
        conn.close()
        return redirect('/')
    
    return render_template('create.html', note=dict(db_note[0]))

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        connection = get_db_connection()
        cur = connection.cursor()
        content = request.form['content']
        sql = 'INSERT INTO notes (content) VALUES (?)'
        cur.execute(sql, (content, ))
        connection.commit()
        connection.close()
        return redirect('/')
    return render_template('create.html', note={'content': ''})
