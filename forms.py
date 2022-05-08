from wsgiref.validate import validator
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import Length, InputRequired


# This seems a bit redunant bc both forms take the same info but it helps me with distinguishing their function/role
class RegistrationForm(FlaskForm):
    """Reg form for new users"""
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=10)])
    
class LoginForm(FlaskForm):
    """Login Form for existing Users"""
    email = EmailField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=10)])

class OneTimePassForm(FlaskForm):
    """A form for entering a users onetime pass at login"""
    authorization_code = StringField('One time auth code', validators=[InputRequired()])

class UpdateProfileForm(FlaskForm):
    """Allows a user to add pfp and bio as well as update information"""
    username = StringField('Username', validators=[])
    pfp_url = StringField('Profile Pic URL', validators=[])
    email = EmailField('Username', validators=[])
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=10)])
    bio = TextAreaField('Enter your Bio', validators=[])

class BlogPostForm(FlaskForm):
    """Posting a blog to your Profile"""
    title = StringField('Post Title', validators=[InputRequired()])
    content = TextAreaField('Enter your thoughts', validators=[])

class BlogUpdateForm(FlaskForm):
    """Posting a blog to your Profile"""
    title = StringField('Post Title', validators=[])
    content = TextAreaField('Enter your thoughts', validators=[])
