from flask import Blueprint, request, session, g, redirect, url_for, render_template, flash
from app import db
from app.mod_chores.forms import ChoreForm, LoginForm
from app.mod_chores.models import Chore

# Define the blueprint: chores
mod_chores = Blueprint('chores', __name__, url_prefix='/chores')

@mod_chores.route('/')
def show_chores():
    if session['active_user'] == 'admin':
        chores = Chores.query.filter(Chores.status == 1).order_by(Chores.id.desc())
    else:
        chores = Chores.query.filter(Chores.owner == session['active_user'], Chores.status == 1).order_by(Chores.id.desc())
    return render_template('show_chores.html', usernames=app.config['USERS'], chores=chores)

@mod_chores.route('/add', methods=['POST'])
def add_chore():
    chore = Chores(request.form['chore'], request.form['owner'], 1)
    db.session.add(chore)
    db.session.commit()
    flash('Nueva tarea agregada')
    return redirect(url_for('show_chores'))

@mod_chores.route('/complete', methods=['POST'])
def complete_chore():
    chore = Chores.query.filter(Chores.id == request.form['id']).first()
    chore.status = 0
    db.session.commit()
    flash('Tarea completada')
    return redirect(url_for('show_chores'))

@mod_chores.route('/remove', methods=['POST'])
def delete_chore():
    Chores.query.filter(Chores.id == request.form['id']).delete()
    db.session.commit()
    flash('Tarea eliminada')
    return redirect(url_for('show_chores'))

@mod_chores.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm(request.form)
    if form.validate_on_submit():
        if form.user.data not in app.config['USERS']:
            session['active_user'] = form.user.data
            flash('Usuario actualizado')
            return redirect(url_for('chores.home'))
        error = 'Usuario no encontrado'
    return render_template('login.html', form=form)