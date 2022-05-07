from crypt import methods
import os 
from flask import Flask, redirect, render_template, request, flash, session
from psycopg2 import IntegrityError
from models import User, db, connect_db
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

#~~~~~~ Login Management Routes ~~~~~~#

@app.route('/')
def get_home():
    """Retrieve and render home route"""

    return render_template('index.html')

# TODO: Write Basic Functionality for logging in and registering 
@app.route('/register', methods=['GET', 'POST'])
def get_registered():
    """View for registering a new user"""
    # Instantiate the Reg Form
    form = RegistrationForm()
    # IF VALIDATION 
    if form.validate_on_submit():
        try:
            # Sign-up both instantiates the User Model and Hashes the passy 
            user = User.register( username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect('/')
    # except if it doesn't 
        except IntegrityError:
            flash('Failed to register try again', 'danger')
            return render_template('register.html', form=form)

    else:
        return render_template('register.html', form=form)

    


@app.route('/login', methods =['GET', 'POST'])
def login_user():
    """View for logging in a new user"""
    # remember that the method for loggin in is called "first_authentication"
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # TODO: ONCE WE HAVE THE BASIC GOING WE'LL REDIRECT TO THE GET TOTP ROUTE
        if user:
            User.first_authentication(form.username.data, form.password.data)
            login_user(user, remember=True)
            flash(f'Hello, {user.username}!', 'success')
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']
            flash('Invalid credentials.', 'danger')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

# # THIS ROUTE GETS TOTP
# @app.route('/retrieve_totp', methods=['GET', 'POST'])
# @login_required
# def get_totp():
#     """Route for genning and sending the TOTP to users e-mail"""
#     if methods == 'POST':
#         return redirect('/authenticate')
#     # TODO: Logic for genning the TOTP on button submit
#     else:
#         return render_template('totp.html')

# # THIS ROUTE AUTHENTICATES TOTP
# @app.route('/authenticate', methods=['GET', 'POST'])
# @login_required
# def second_auth():
#     """Renders the 2FA form and then redirects on success"""
#     form = OneTimePassForm()
#     #TODO: Put logic in here for grabbing the the genned password
#     if form.validate_on_submit():
#         try:
#             #TODO: create loging for comparing the user providedc TOTP to our gen Token
#             return redirect('/')
#         except:
#            #TODO: Find particular error and do re-render
#            return render_template('auth.html')

#     else:
#         return render_template('register.html', form=form)
    
@app.route('/logout')
def logout_user():
    """View for logging out a user"""
    logout_user()
    return redirect('/')

#~~~~~~ Profile Management Routes ~~~~~~#

# TODO: 
# Get all users and display them-USER DIRECTORY
# Get the logged in user and display their profile
# Get User Details
# UPDATE ALL INFO AND ADD PFP/BIO
# UPDATE PASSWORD
# View all your blogs

#~~~~~~ Blog Management Routes ~~~~~~#

# TODO: 
# Get all of a blogs and display them - blog feed
# Get the a users blog and display them-users have an option to edit their own blog posts
# Get and Display a particular blog post
# UPDATE a blog post 
# UPDATE PASSWORD
# View all your blogs

