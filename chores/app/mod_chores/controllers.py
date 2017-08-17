from flask import Blueprint, request, session, g, redirect, url_for, render_template, flash, current_app
from app import db
from app.mod_chores.forms import ChoreForm, LoginForm
from app.mod_chores.models import Chore

# Define the blueprint: chores
mod_chores = Blueprint('chores', __name__, url_prefix='/chores')

@mod_chores.route('/')
def show_chores():

    login_form = LoginForm(request.form)
    chore_form = ChoreForm(request.form)
    if 'active_user' in session:
        if session['active_user'] == 'admin':
            chores = Chore.query.filter(Chore.status == 1).order_by(Chore.id.desc())
        else:
            chores = Chore.query.filter(Chore.owner == session['active_user'], Chore.status == 1).order_by(Chore.id.desc())
    else:
        chores = []
    return render_template('mod_chores/show_chores.html', chores=chores, login_form=login_form, chore_form=chore_form)

@mod_chores.route('/add', methods=['POST'])
def add_chore():

    form = ChoreForm(request.form)
    if request.method == 'POST' and form.validate():
        chore = Chore(form.title.data, form.owner.data, 1)
        db.session.add(chore)
        db.session.commit()
        flash('Nueva tarea agregada')
    return redirect(url_for('chores.show_chores'))

@mod_chores.route('/complete', methods=['POST'])
def complete_chore():

    chore = Chore.query.filter(Chore.id == request.form['id']).first()
    chore.status = 0
    db.session.commit()
    flash('Tarea completada')
    return redirect(url_for('chores.show_chores'))

@mod_chores.route('/remove', methods=['POST'])
def delete_chore():

    Chore.query.filter(Chore.id == request.form['id']).delete()
    db.session.commit()
    flash('Tarea eliminada')
    return redirect(url_for('chores.show_chores'))

@mod_chores.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.user.data in current_app.config['USERS']:
            session['active_user'] = form.user.data
            flash('Usuario actualizado')
    return redirect(url_for('chores.show_chores'))