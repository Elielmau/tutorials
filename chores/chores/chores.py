import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

app.config.from_object('config')
app.config.from_envvar('CHORES_SETTINGS', silent=True)
db = SQLAlchemy(app)

# Model
def init_db():
    db.create_all()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database')

class Chores(db.Model):
    __tablename__ = 'chores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title =db.Column(db.Text, nullable=False)
    owner =db.Column(db.Text, nullable=False)
    status =db.Column(db.Integer, nullable=False)

    def __init__(self, title, owner, status):
        self.title = title
        self.owner = owner
        self.status = status

    def __repr__(self):
        return '<Tarea %r>' % self.title

@app.route('/')
def show_chores():
    if session['active_user'] == 'admin':
        chores = Chores.query.filter(Chores.status == 1).order_by(Chores.id.desc())
    else:
        chores = Chores.query.filter(Chores.owner == session['active_user'], Chores.status == 1).order_by(Chores.id.desc())
    return render_template('show_chores.html', usernames=app.config['USERS'], chores=chores)

@app.route('/add', methods=['POST'])
def add_chore():
    chore = Chores(request.form['chore'], request.form['owner'], 1)
    db.session.add(chore)
    db.session.commit()
    flash('Nueva tarea agregada')
    return redirect(url_for('show_chores'))

@app.route('/complete', methods=['POST'])
def complete_chore():
    chore = Chores.query.filter(Chores.id == request.form['id']).first()
    chore.status = 0
    db.session.commit()
    flash('Tarea completada')
    return redirect(url_for('show_chores'))

@app.route('/remove', methods=['POST'])
def delete_chore():
    Chores.query.filter(Chores.id == request.form['id']).delete()
    db.session.commit()
    flash('Tarea eliminada')
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