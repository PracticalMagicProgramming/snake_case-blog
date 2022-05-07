from crypt import methods
import os
import bcrypt 
from flask import Flask, redirect, render_template, request, flash, session
from psycopg2 import IntegrityError
from models import Post, User, db, connect_db
from forms import BlogUpdateForm, RegistrationForm, LoginForm, BlogPostForm, ChangePassForm, UpdateProfileForm, OneTimePassForm
from sqlalchemy.sql import text
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_bcrypt import check_password_hash


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
            try:
                User.first_authentication(form.username.data, form.password.data)
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

# FIXME: We'll need to initialize the page num as zero

# Get all users and display them-USER DIRECTORY
@app.route('/users/<int:page_num>')
@login_required
def get_user_dir(page_num):
    """View for seeing all of snake_case's users"""
    all_users = User.query.paginate(per_page=5, page=page_num, error_out=True)
    return render_template('user-dir.html', all_users=all_users)

# Get the user and display their profile
@app.route('/users/profile/<int:user_id>')
@login_required
def get_user_profile(user_id):
    """View for seeing users profile"""
    # if the profile is the users profile display an edit button
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)


# UPDATE and ADD to Profile
@app.route('/users/profile/<int:user_id>/edit', methods=['GET', 'PATCH'])
@login_required
def edit_user_profile(user_id):
    """View for updating logged in users profile"""
    # get user profile and pass it to the form to be edited
    user = User.get_or_404(user_id)
    form = UpdateProfileForm(obj=user)

    if form.validate_on_submit():
        try:
            #grab the data
            username = username.form.data
            pfp_url = pfp_url.form.data
            email =   email.form.data
            bio = bio.form.data
            
            #perform the update
            user_update = User.update().where(User.id==user_id).values(username=username,pfp_url=pfp_url,email=email,bio=bio)
            db.session.add(user_update)
            db.session.commit()
            return redirect(f'/users/profile/{user_id}')
        except:
                flash('update not successful try again')
                return render_template('profile-update.html', form=form)

    else:
    # TODO: we will need an update password anchor tag in our template
        return render_template('update-profile.html', form=form)
    

# UPDATE PASSWORD
@app.route('/users/profile/<int:user_id>/edit/password', methods=['GET', 'PATCH'])
@login_required
def change_user_password(user_id):
    """View for updating logged in users password"""

    # grab the user and their password, give the form the current pass to be edited
    user = User.get_or_404(user_id)
    user_pass = user.password
    form = ChangePassForm(obj=user_pass)

    if form.validate_on_submit():
        try:
            # Grab of orig pass data and compare passwords- update accordingly
            old_password= old_password.form.data
            new_password = new_password.form.data
            authenticated = bcrypt.check_password_hash(user_pass, old_password)

            if authenticated:
                # if Authenticated we grab the new password and update! e
                user_new_pass = User.update().where(User.id==user_id).values(password=new_password)
                db.session.add(user_new_pass)
                db.session.commit()
                return redirect(f'/users/profile/{user_id}')
        except:
                flash('update not successful try again')
                return render_template('pass-update.html', form=form)

    else:
    # TODO: we will need an update password anchor tag in our template
        return render_template('pass-update.html', form=form)


#FIXME: Fix the pagination for the blogs- how do we paginate only the users blogs

# View all of a users blogs-users have an option to edit their own blog posts
# Get the user and display their profile
@app.route('/users/<int:user_id>/blogs')
@login_required
def get_user_blogs(user_id):
    """View for seeing users profile"""
    # if the profile is the users profile display an edit button - TODO: In Template
    user = User.get_or_404(user_id)
    user_blogs = user.user_posts
    # Template should include toggling for whether the user can edit the blogs 
    return render_template('user-blogs.html', user_blogs=user_blogs)

#~~~~~~ Blog Management Routes ~~~~~~#

# FIXME: Initialize the pagination on the Template
# Get all of a blogs and display them - blog feed
@app.route('/blogs/<int:page_num>')
@login_required
def get_blog_feed(page_num):
    """View for seeing all of snake_case's blogs-displayed as a feed"""
    all_blogs = Post.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template('feed.html', all_blogs=all_blogs)

# Get and Display a particular blog post-users have an option to edit their own blog posts
@app.route('/blogs/<int:post_id>')
@login_required
def get_blog_detail(post_id):
    """View for seeing a particular blog post"""
    blog = Post.get_or_404(post_id)
    # if the blog is the users they should be able to edit the blog- TODO: in Template
    return render_template('blog.html', blog=blog)

# Create a new blog post
@app.route('/blogs/create', methods=['GET', 'POST'])
@login_required
def create_new_post():
    """View for creating a new blog post"""
    form = BlogPostForm()
    # get the current user and exract their id for use
    user = User.query.filter_by(current_user.id)
    user_id =user.id

    # handling the form submission
    if form.validate_on_submit():
        try:
            title = title.form.data
            content = content.form.data

            blog_post = Post(title=title, content=content, author_id=user_id)
            db.session.add(blog_post)
            db.session.commit()
            return redirect(f'/users/{user_id}/blogs')
        except:
                flash('update not successful try again')
                return render_template('create.html', user=user, form=form)

    else:
        return render_template('create.html', user=user, form=form)

# UPDATE a blog post
@app.route('/blogs/<int:post_id>/update', methods=['GET', 'PATCH'])
@login_required
def update_blog_post(post_id):
    """View for creating a new blog post"""
     # get post using id and pass the existing info to the form to display
    post = Post.query.get_or_404(post_id)
    form = BlogUpdateForm(obj=post)
    # get the current user and exract their id for use
    user = User.query.filter_by(current_user.id)
    user_id =user.id
   
    # handling the form submission
    if form.validate_on_submit():
        try:
            #grab the data
            title = title.form.data
            content = content.form.data
        
            #perform the update
            blog_post_update = Post.update().where(Post.id==post_id).values(title=title, content=content)
            db.session.add(blog_post_update)
            db.session.commit()
            return redirect(f'/blogs/{post_id}')
        except:
                flash('update not successful try again')
                return render_template('create.html', user=user, form=form)

    else:
        return render_template('create.html', user=user, form=form)


