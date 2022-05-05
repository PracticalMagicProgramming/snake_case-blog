from wsgiref.validate import validator
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import Length, InputRequired


# This seems a bit redunant bc both forms take the same info but it helps me with distinguishing their function/role
class RegistrationForm(FlaskForm):
    """Reg form for new users"""

    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=10)])

class LoginForm(FlaskForm):
    """Login Form for existing Users"""

    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=10)])