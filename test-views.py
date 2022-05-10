""" Testing User views"""

# run these tests:
#
#    python -m unittest test-views.py


from unittest import TestCase
from models import db, User, Post
from app import app

app.config["SQLALCHEMY_DATABASE_URI"]  = "postgresql:///snake-case-test"
app.config['SQLALCHEMY_ECHO']=False
app.config['TESTING']=True
app.config['SECRET_KEY'] = 'thisshouldbeasecret'


class LoginViewTestCase(TestCase):
    """Testing our Login Route"""
    
    def setUp(self):
        """Make demo data commmit it to our testing database, clean up altered data from last test"""
    # drop and recreate the db 
        db.drop_all()
        db.create_all()

    # instantiate user data to be used by the tests
        self.testuser = User.register(username="testuser",
                                    email="test@test.com",
                                    password="testuser")
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.register("abc", "test1@test.com", "password")
        self.u1_id = 778
        self.u1.id = self.u1_id
        self.u2 = User.register("efg", "test2@test.com", "password")
        self.u2_id = 884
        self.u2.id = self.u2_id
        self.u3 = User.register("hij", "test3@test.com", "password")
        self.u4 = User.register("testing", "test4@test.com", "password")
        

    def tearDown(self):
        """Clean up crew"""
        resp = super().tearDown()
        db.session.rollback()
        return resp
        
    def test_get_login(self):
        # get request for route
        with app.test_client() as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-dark">Log Me In</button>', html)

    def test_login_redirect(self):
        # redirect for route
        with app.test_client() as client:
            resp = client.get('/login', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

class RegisterViewTestCase(TestCase):
    """Testing our Login Route"""
    
    def setUp(self):
        """Drop and recreate the db"""
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Clean up crew"""
        resp = super().tearDown()
        db.session.rollback()
        return resp
        
    def test_get_register(self):
        # get request for route
        with app.test_client() as client:
            resp = client.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
       

    def test_register_redirect(self):
        # redirect for route
            with app.test_client() as client:
                d = {'username': 'Mirii', 'email': 'mirii@gmail.com', 'password' : 'password4'}
                resp = client.post('/register', data=d, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
        



         

