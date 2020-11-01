from django.test import TestCase

from .models import User, Posts, Followers
import datetime

# Create your tests here.

class PostsModelTests(TestCase):

    def setUp(self):
        # Insert users into table
        user1 = User.objects.create(username='User1', password='something1')
        user2 = User.objects.create(username='User2', password='something2')
        user3 = User.objects.create(username='User3', password='something3')
        user4 = User.objects.create(username='User4', password='something4')

        # Insert Posts
        post1 = Posts.objects.create(post='Post1', user=user1, date=datetime.datetime.now())
        post2 = Posts.objects.create(post='Post2', user=user2, date=datetime.datetime.now())
        post3 = Posts.objects.create(post='Post3', user=user3, date=datetime.datetime.now())

        # Give likes to each post
        post1.likes.add(user1)
        post1.likes.add(user2)
        post2.likes.add(user1)
        post2.likes.add(user1)
        post2.likes.add(user3)
        post3.likes.add(user2)

        # Add user on Followers
        follow1 = Followers.objects.create(user=user1)
        follow2 = Followers.objects.create(user=user2)
        follow3 = Followers.objects.create(user=user3)
        follow4 = Followers.objects.create(user=user4)

        # Add user to follow others
        follow1.followers.add(user2)
        follow1.followers.add(user3)
        follow1.followers.add(user4)

        follow2.followers.add(user1)
        follow2.followers.add(user3)

        follow3.followers.add(user1)
        
        follow4.followers.add(user1)


    def test_user_was_well_inserted(self):
        ''' Check if all users were well inserted
        '''
        self.assertEqual(User.objects.all().count(), 4)
    
    def test_posts_was_well_inserted(self):
        ''' Check if all posts were well inserted
        '''
        self.assertEqual(Posts.objects.all().count(), 3)

    def test_likes_were_well_inserted(self):
        ''' Check if all likes were well inserted
        '''
        post_check = Posts.objects.get(pk=1)
        self.assertEqual(post_check.likes.count(), 2)

    def test_likes2_were_well_inserted(self):
        ''' Check if all likes were well inserted
        '''
        post_check = Posts.objects.get(pk=2)
        self.assertEqual(post_check.likes.count(), 2)
    
    def test_followers_well_inserted(self):
        ''' Check if all Followers were well inserted
        '''
        self.assertEqual(Followers.objects.all().count(), 4)

    def test_user_followers_inserted(self):
        ''' Check how many users, is user following
        '''
        user_1 = User.objects.get(username="User1")
        user_2 = User.objects.get(username="User2")
        followers1_check = Followers.objects.get(user=user_1)
        followers2_check = Followers.objects.get(user=user_2)
        self.assertEqual(followers1_check.followers.all().count(), 3)
        self.assertEqual(followers2_check.followers.all().count(), 2)

    def test_user_followers_deleted(self):
        ''' Check if user stopped following other users, well deleted
        '''
        user_1 = User.objects.get(username="User1")
        user_2 = User.objects.get(username="User2")
        followers1_check = Followers.objects.get(user=user_1)
        followers1_check.followers.remove(user_2)
        self.assertEqual(followers1_check.followers.all().count(), 2)
    
    def test_how_many_user_are_following_user(self):
        ''' Check how many are following the user
        '''
        user_1 = User.objects.get(username="User1")
        self.assertEqual(user_1.follow.count(), 3)