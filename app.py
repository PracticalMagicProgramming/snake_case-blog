import os
import bcrypt 
from flask import Flask, redirect, render_template, flash
from psycopg2 import IntegrityError
from models import Post, User, db, connect_db, bcrypt
from forms import BlogUpdateForm, RegistrationForm, LoginForm, BlogPostForm, UpdateProfileForm, OneTimePassForm
from sqlalchemy.sql import text
from flask_sqlalchemy import Pagination
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
import pdb
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


@app.route('/register', methods=['GET', 'POST'])
def get_registered():
    """View for registering a new user"""
  
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            # Sign-up both instantiates the User Model and Hashes the passy 
            user = User.register( username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect('/')
    
        except IntegrityError:
            flash('Failed to register. Please try again', 'danger')
            return render_template('register.html', form=form)

    else:
        return render_template('register.html', form=form)



@app.route('/login', methods =['GET', 'POST'])
def user_login():
    """View for logging in a new user"""
    # remember that the method for loggin in is called "first_authentication"
    form = LoginForm()

    if form.validate_on_submit():
        # We use filter_by bc until the user is logged on, no access to PK
        user = User.query.filter_by(username=form.username.data).first()

        # TODO: ONCE WE HAVE THE BASIC GOING WE'LL REDIRECT TO THE GET TOTP ROUTE
        if user:
            try:
                User.first_authentication(user.username, form.password.data)
                login_user(user, remember=True)
                flash(f'Hello, {user.username}!', 'success')
                return redirect('/')
            except:
                form.username.errors = ['Invalid username/password.']
                flash('Invalid credentials.', 'danger')
                return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

# # THIS ROUTE GETS TOTP
# @app.route('/retrieve_totp', methods=['GET', 'POST'])
# @login_required
# def get_totp():
#     """Route for genning and sending the TOTP to users e-mail"""
#     TODO: Grab Current user
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
#     TODO: Grab Current user
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
@login_required
def logout_user():
    """View for logging out a user"""
    logout_user()
    return redirect('/')

#~~~~~~ Profile Management Routes ~~~~~~#


@app.route('/users/<int:page_num>', defaults={'page_num' : 1})
@app.route('/users/<int:page_num>')
@login_required
def get_user_dir(page_num):
    """View for seeing all of snake_case's users"""
    all_users = User.query.paginate(per_page=5, page=page_num, error_out=True)
    return render_template('user-dir.html', all_users=all_users)

@app.route('/users/profile/<int:user_id>')
@login_required
def get_user_profile(user_id):
    """View for seeing users profile"""
  
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)



@app.route('/users/profile/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user_profile(user_id):
    """View for updating logged in users profile"""
    # get user profile and pass it to the form to be edited
    user = User.query.get_or_404(user_id)
    form = UpdateProfileForm(obj=user)

    if form.validate_on_submit():
        try:

            user.username = form.username.data
            user.email = form.email.data
            #grab password from form, hash and update it
            new_password = form.password.data
            new_pass_hash = bcrypt.generate_password_hash(new_password).decode('UTF-8')
            user.password = new_pass_hash
            user.bio = form.bio.data
            
            #perform the update
            db.session.commit()
            return redirect(f'/users/profile/{user_id}')
        except:
                flash('update not successful try again')
                return render_template('profile-update.html', form=form, user=user)

    else:
        return render_template('profile-update.html', form=form, user=user)
    

# Set two route configs- one has the inital default for the page num
@app.route('/users/<int:user_id>/blogs/<int:page_num>', defaults={'page_num' : 1})
@app.route('/users/<int:user_id>/blogs/<int:page_num>')
@login_required
def get_user_blogs(user_id, page_num):
    """View for seeing users profile"""
    user = User.query.filter_by(id=user_id).first()
    posts = Post.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template('user-blogs.html', user=user, posts=posts)

#~~~~~~ Blog Management Routes ~~~~~~#


# We have the two routes for the pagination config
@app.route('/blogs/<int:page_num>', defaults={'page_num' : 1})
@app.route('/blogs/<int:page_num>')
@login_required
def get_blog_feed(page_num):
    """View for seeing all of snake_case's blogs-displayed as a feed"""
    all_blogs = Post.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template('feed.html', all_blogs=all_blogs)


@app.route('/blogs/view/<int:post_id>')
@login_required
def get_blog_detail(post_id):
    """View for seeing a particular blog post"""
    post = Post.query.get_or_404(post_id)
   
    return render_template('view-blog.html', post=post)


@app.route('/blogs/create', methods=['GET', 'POST'])
@login_required
def create_new_post():
    """View for creating a new blog post"""
    form = BlogPostForm()
    # get the current user and exract their id for use
    user = User.query.get_or_404(current_user.id)
    user_id =user.id

    # handling the form submission
    if form.validate_on_submit():
        try:
            title = form.title.data
            content = form.content.data

            blog_post = Post(title=title, content=content, author_id=user_id)
            db.session.add(blog_post)
            db.session.commit()
            return redirect(f'/users/{user_id}/blogs/1')
        except:
                flash('update not successful try again')
                return render_template('create.html', form=form, user=user)

    else:
        return render_template('create.html', form=form, user=user)

# UPDATE a blog post
@app.route('/blogs/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_blog_post(post_id):
    """View for creating a new blog post"""
     # get post using id and pass the existing info to the form to display
    post = Post.query.get(post_id)
    form = BlogUpdateForm(obj=post)
    # get the current user and exract their id for use
    user = User.query.get(current_user.id)
   
    # handling the form submission
    if form.validate_on_submit():
        try:
            #grab the data
            post.title = form.title.data
            post.content = form.title.data
        
            #perform the update
            db.session.commit()
            return redirect(f'/blogs/{post_id}')
        except:
                flash('update not successful try again')
                return render_template('update-blog.html', form=form, user=user, post=post)

    else:
        return render_template('update-blog.html', form=form, user=user, post=post)


