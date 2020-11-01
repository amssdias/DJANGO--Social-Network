from django.contrib import admin

from .models import User, Posts, Followers

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser')

class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'date')

class FollowersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

admin.site.register(User, UserAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Followers, FollowersAdmin)