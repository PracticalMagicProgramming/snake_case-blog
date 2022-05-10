"""Testing Our SQLAlchemy Models"""

# run these tests like:
#
#    python -m unittest test-models.py

from unittest import TestCase
from models import db, User, Post
from app import app

app.config["SQLALCHEMY_DATABASE_URI"]  = "postgresql:///snake-case-test"
app.config['SQLALCHEMY_ECHO']=False
app.config['TESTING']=True



class ModelTestCase(TestCase):
    """Testing our SQLA Models"""
    
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        
    def setUp(self):
        """Clear models"""

        User.query.delete()
        db.session.commit()

        Post.query.delete()
        db.session.commit()

    def tearDown(self):
        """clearing session after each test"""

        db.session.rollback()
        

    def test_user_model(self):
        """Adding to User Model"""

        u = User(
           
            username='mirii',
            email='test@test.com',
            password = 'password1',
            bio ='i like cats'
        )

        db.session.add(u)
        db.session.commit()
        
        
        self.assertEqual(u.username, 'mirii')
        self.assertEqual(u.password, 'password1')

    def test_sign_up(self):
        """tests our sign_up class method"""

        new_user = User.register(username='mirii2', email='test2@test.com', password = 'password2')
        db.session.add(new_user)
        db.session.commit()

        self.assertEqual(new_user.username, 'mirii2')

    def test_authenticate(self):
        """Test User Model Authenticate Method"""

        #sign member up
        other_new_user = User.register(username='mirii3', email='test3@test.com', password = 'password3')
        db.session.add(other_new_user)
        db.session.commit()
        
        # test authenticate for new person logging in
        returning_user = User.first_authentication(username='mirii3', password = 'password3')

        self.assertTrue(returning_user)

    def test_user_post_model(self):
            """Adding to User Model"""

            
            u = User(
                id= 1,
                username='mirii',
                email='test@test.com',
                password = 'password1',
                bio ='i like cats'
            )

            db.session.add(u)
            db.session.commit()
        

            p = Post(
                id = 1,
                title= 'a test',
                content = 'this is a test post',
                author_id = 1

            )

            db.session.add(p)
            db.session.commit()

        
            self.assertEqual(p.title, 'a test')
            self.assertEqual(p.content, 'this is a test post')
            self.assertIsInstance(p, object )
            

