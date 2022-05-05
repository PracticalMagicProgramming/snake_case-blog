import os 
from flask import Flask, render_template, request, flash, session
from models import User, connect_db
from forms import RegistrationForm, LoginForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_INTERCEPTS_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


connect_db(app)


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
    """View for loging in a new user"""

    return render_template('login.hmtl')