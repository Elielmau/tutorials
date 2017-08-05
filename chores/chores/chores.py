import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='ABC123',
    USERNAME='eliel',
    USERS=['evie', 'gael'], # Move to DB
))
app.config.from_envvar('CHORES_SETTINGS', silent=True)

@app.route('/')
def show_chores():
    return render_template('show_chores.html', usernames=app.config['USERS'])

@app.route('/add', methods=['POST'])
def add_chore():
    if not session.get('logged_in'):
        abort(401)
    # Insert new entry into DB
    # Code here...
    flash('Nueva tarea agregada')
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