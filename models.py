from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



bcrypt = Bcrypt() 
db = SQLAlchemy()

class User(db.Model):
    """Creates a User for our db"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(30), nullable=False, unique=True)

    email = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.String, nullable=False)

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
        authenticated = bcrypt.check_password_has(user.password, password)
        if authenticated:
            return user
    return False



def connect_db(app):
    """Connects our db to our application"""
    db.app =app
    db.init_app(app)
    