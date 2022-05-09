from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import UserMixin


bcrypt = Bcrypt() 
db = SQLAlchemy()
migrate = Migrate()


class User(UserMixin, db.Model):
    """Creates a User for our db"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(30), nullable=False, unique=True)
    
    email = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.String, nullable=False)

    bio = db.Column(db.Text)

    # Using a join to get all of the users posts as a list 
    users_posts =  db.relationship(
        "Post",
        secondary="user_posts",
        backref='users',
    )


    @classmethod 
    def register(cls, username, email, password):
        """Class method to register a User"""

        hash_word = bcrypt.generate_password_hash(password).decode('UTF-8')

        new_user = User(username=username, email=email, password=hash_word)

        db.session.add(new_user)

        return(new_user)

    @classmethod
    def first_authentication(cls, username, password):
        """Method to perform first level of authentication"""

        user = cls.query.filter_by(username=username).first()

        if user:
            authenticated = bcrypt.check_password_hash(user.password, password)
            if authenticated:
                return user
        return False

class Post(db.Model):
    """A users Blog post"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(30), nullable=False)
    
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class User_Post(db.Model):
    """M2M Table for users and their posts"""

    __tablename__ = "user_posts"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

def connect_db(app):
    """Connects our db to our application"""
    db.app =app
    db.init_app(app)
    migrate=Migrate(app,db) #Initializing migrate
    