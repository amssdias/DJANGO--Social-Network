
from django.urls import path

from . import views

app_name = 'network'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),
    path('following', views.following, name="following"),
    path('edit/<int:post_id>', views.edit_post, name="edit"),
    path('like/<int:post_id>', views.like_post, name='like'),
    path('profile/<str:user>', views.profile, name='profile'),
    path('follow/<int:user_id>', views.follow, name='follow'),
]
