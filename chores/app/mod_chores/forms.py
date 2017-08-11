# Import WTF and extensions
from flask_wtf import Form
from wtforms import TextField, RadioField, HiddenField, SubmitField
from wtforms.validators import Required

# Define the chore form
class ChoreForm(Form):

    title = TextField('Nueva Tarea', [Required(message='Debe ingresar un titulo')])
    owner = RadioField('Hijo', [Required(message='Debe seleccionar un hijo')], choices=[('gael', 'Gael'), ('evie', 'Evie')])


# Define the login form, this particular login doesn't use password
class LoginForm(Form):

    user = RadioField('Usuario', [Required(message='Debe seleccionar un hijo')], choices=[('gael', 'Gael'), ('evie', 'Evie')])