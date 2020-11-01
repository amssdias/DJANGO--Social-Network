from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Posts(models.Model):
    post = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return self.post

    class Meta:
        verbose_name_plural = 'Posts'

    def serialize(self):
        return {
            'id': self.id,
            'post': self.post,
            'user': self.user.username,
            'likes': [x.user.username for x in self.user.likes.all()],
            'date':self.date
        }

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='follower')

    def __str__(self):
        return f"UserId: {self.user.id}, User: {self.user}"
    
    class Meta:
        verbose_name_plural = 'Followers'

    def serialize(self):
        return {
            "id": self.id,
            "user-id": self.user.pk,
            "username": self.user.username,
            "following": [[follower.id, follower.username] for follower in self.followers.all()],
            "followers": [[x.user.id, x.user.username] for x in self.user.follower.all()]
        }