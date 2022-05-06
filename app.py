import os 
from flask import Flask, redirect, render_template, request, flash, session
from models import User, connect_db
from forms import RegistrationForm, LoginForm, BlogPostForm, ChangePassForm, UpdateProfileForm, OneTimePassForm
from sqlalchemy.sql import text
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_INTERCEPTS_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

#instantiating an instance of the LoginManager class
login_manager = LoginManager()

connect_db(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """returns user id from session to validate login"""
    user = text(user_id)
    return User.query.filter_by(id=user).first()


@app.route('/')
def get_home():
    """Retrieve and render home route"""

    return render_template('index.html')


@app.route('/register')
def get_registered():
    """View for registering a new user"""

    return render_template('register.hmtl')


@app.route('/login')
def login_user():
    """View for logging in a new user"""

    return render_template('login.hmtl')

@app.route('/logout')
def logout_user():
    """View for logging out a user"""
    logout_user()
    return redirect('/')