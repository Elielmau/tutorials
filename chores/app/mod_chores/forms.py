# Import WTF and extensions
from flask_wtf import Form
from wtforms import TextField, RadioField, HiddenField, SubmitField
from wtforms.validators import Required

from app import app

# Helper function to build the list of users, choices for radio buttons (Might need to move this)
def get_user_list(no_admin=True):

    user_list = []

    for user in app.config['USERS']:
        if no_admin and user == 'admin': continue
        user_list.append((user, user.capitalize()))

    return user_list

# Define the chore form
class ChoreForm(Form):

    title = TextField('Nueva Tarea', [Required(message='Debe ingresar un titulo')])
    owner = RadioField('Hijo', [Required(message='Debe seleccionar un hijo')], choices=get_user_list())


# Define the login form, this particular login doesn't use password
class LoginForm(Form):

    user = RadioField('Usuario', [Required(message='Debe seleccionar un hijo')], choices=get_user_list(no_admin=False))