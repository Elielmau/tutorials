import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

app.config.from_object('config')
app.config.from_envvar('CHORES_SETTINGS', silent=True)

@app.route('/')
def show_chores():
    db = get_db()
    if session['active_user'] == 'admin':
        cur = db.execute('SELECT id, title, status FROM chores WHERE status = (?) ORDER BY id DESC', [1])
    else:
        cur = db.execute('SELECT id, title, status FROM chores WHERE owner = (?) AND status = (?) ORDER BY id DESC', [session['active_user'], 1])
    chores = cur.fetchall()
    return render_template('show_chores.html', usernames=app.config['USERS'], chores=chores)

@app.route('/add', methods=['POST'])
def add_chore():
    db = get_db()
    db.execute('INSERT INTO chores(title, owner, status) VALUES (?, ?, ?)', [request.form['chore'], request.form['owner'], 1])
    db.commit()
    flash('Nueva tarea agregada')
    return redirect(url_for('show_chores'))

@app.route('/remove', methods=['POST'])
def delete_chore():
    db = get_db()
    db.execute('DELETE FROM chores where id = (?)', [request.form['id']])
    db.commit()
    flash('Tarea eliminada')
    return redirect(url_for('show_chores'))

@app.route('/complete', methods=['POST'])
def complete_chore():
    db = get_db()
    db.execute('UPDATE chores SET status = 0 WHERE id = (?)', [request.form['id']])
    db.commit()
    flash('Tarea completada')
    return redirect(url_for('show_chores'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('user', None) not in app.config['USERS']:
            error = 'Usuario no encontrado'
        else:
            session['active_user'] = request.form.get('user', None)
            flash('Usuario actualizado')
            return redirect(url_for('show_chores'))
    return render_template('login.html', error=error)

#DB Setup and functions

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database')

def connect_db():
    print(app.config['DATABASE']) #debug
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()