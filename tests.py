import unittest
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='xale')
        u.set_password('flask')
        self.assertFalse(u.check_password('django'))
        self.assertTrue(u.check_password('flask'))

    def test_avatar(self):
        u = User(username='xale', email='xale@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'f73aca8071915c26b8b133c264c9e110'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='xale', email='xale@example.com')
        u2 = User(username='alex', email='alex@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'alex')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'xale')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)
    
    def test_follow_posts(self):
        # create four users
        u1 = User(username='xale', email='xale@example.com')
        u2 = User(username='alex', email='alex@example.com')
        u3 = User(username='flask', email='flask@example.com')
        u4 = User(username='django', email='django@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body='post from xale', author=u1,
                timestamp=now+timedelta(seconds=1))
        p2 = Post(body='post from alex', author=u2,
                timestamp=now+timedelta(seconds=1))
        p3 = Post(body='post from flask', author=u3,
                timestamp=now+timedelta(seconds=1))
        p4 = Post(body='post from django', author=u4,
                timestamp=now+timedelta(seconds=1))
        db.session.add_all([p1, p2, p3 ,p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2) # xale follows alex
        u1.follow(u4) # xale follows django
        u2.follow(u3) # alex follows flask
        u3.follow(u4) # flask follows django
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p1, p2, p4])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == "__main__":
    unittest.main(verbosity=2)