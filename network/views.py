import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Posts, Followers
from .forms import NewPost

# Index
def index(request):
    all_posts = Posts.objects.order_by('-date').all()

    # Create paginator with only 10 posts per page
    p = Paginator(all_posts, 10)

    page_number = request.GET.get('page', 1)

    try:
        page = p.page(page_number)
    except:
        page = p.page(1)

    return render(request, "network/index.html", {
        'form': NewPost(),
        'posts': page
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        if username == '':
            return render(request, "network/register.html", {
                "message": "Type some username"
            })

        if email == '':
            return render(request, "network/register.html", {
                "message": "Type some email"
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user_f = Followers(user=user)
            user_f.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


# Add post function
@login_required(login_url='/login')
def add_post(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            post_clean = form.cleaned_data['post']
            user = User.objects.get(pk=request.user.id)
            post = Posts(post=post_clean, user=user)
            post.save()
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return HttpResponseRedirect(reverse("network:index"))

# Display user profile
def profile(request, user):

    # Get user
    profile = User.objects.get(pk=user)

    # Get followers from that user and who hes following
    follow = Followers.objects.get(user=profile)
    following = follow.followers.count()
    followers = User.objects.filter(followers__followers=profile).count()

    # Get Posts from user
    user_posts = Posts.objects.filter(user=profile).order_by('-date').all()

    # Make paginator with 10 posts only per page
    p = Paginator(user_posts, 10)

    # Get page number if there's one
    page_number = request.GET.get('page', 1)

    # Try create the page we want, if not go to page 1
    try:
        page = p.page(page_number)
    except:
        page = p.page(1)

    return render(request, "network/profile.html", {
        'user_profile': profile, 
        'following': following,
        'followers':  followers ,
        "follow": profile.follower.filter(user__id=request.user.id).count(),
        'posts': page
        })

# API for follow
@csrf_exempt
@login_required(login_url='/login')
def follow(request, user_id):

    try:
        # Get user id and followers
        user = User.objects.get(pk=user_id)
        follow = Followers.objects.get(user=user)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(follow.serialize(), safe=False)

    elif request.method == "PUT":

        # Get Json from fetch
        data = json.loads(request.body)

        # If data is not empty
        if data.get('follower_to_add') is not None and data.get('user') is not None:

            # Get the current user
            user_to_add = User.objects.get(pk=data.get('follower_to_add'))

            # Get current user followers table
            user_follower = Followers.objects.get(user=user_to_add)

            # If the user is not following yet the profile we looking (Which shouldn't)
            if not user_follower.followers.filter(pk=user.id).count():

                # Make current user start following the profile he's watching
                user_follower.followers.add(user)
                user_follower.save()
                
                return HttpResponse(status=200)

    elif request.method == "DELETE":

        # Get Json from fetch
        data = json.loads(request.body)

        if data.get('follower_to_remove') is not None and data.get('user') is not None:

            # Get current user followers table
            user_remove = User.objects.get(pk=data.get('follower_to_remove'))

            # Get his followers table
            user_f_remove = Followers.objects.get(user=user_remove)

            # Make him stop following the profile user he's watching
            user_f_remove.followers.remove(user)
            user_f_remove.save()

            return HttpResponse(status=200)

    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)

# Get posts from following users
@login_required(login_url='/login')
def following(request):

    # Get user
    user_f = User.objects.get(pk=request.user.id)

    # Get user followers
    user_following = Followers.objects.get(user=user_f)

    # Get posts from the following users
    following = Posts.objects.filter(user__in=user_following.followers.all()).order_by('-date')

    # Make paginator with 10 posts only per page
    p = Paginator(following, 10)

    # Get page number if there's one
    page_number = request.GET.get('page', 1)

    # Try create the page we want, if not go to page 1
    try:
        page = p.page(page_number)
    except:
        page = p.page(1)

    # Return posts from who's the user following
    return render(request, "network/following.html", {
        'posts': page
        })


# Edit post API
@csrf_exempt
@login_required(login_url='/login')
def edit_post(request, post_id):
    try:
        # Post
        post = Posts.objects.get(pk=post_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)

    if request.method == "PUT":
        data = json.loads(request.body)

        if data.get('new_post') is not None:
            post.post = data.get('new_post')
            post.save()

        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)

# Likes API
@csrf_exempt
@login_required(login_url='/login')
def like_post(request, post_id):

    try:
        # Get post
        post = Posts.objects.get(pk=post_id)
        user = User.objects.get(pk=request.user.id)
        if user not in post.likes.all():
            print("user have liked this post")
        else:
            print("User havent liked this post yet")

    except Email.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)

    if request.method == "PUT":
        data = json.loads(request.body)

        if data.get('like') is not None:
            if user not in post.likes.all():
                post.likes.add(user)
            
        return HttpResponse(status=204)

    if request.method == "DELETE":
        data = json.loads(request.body)

        if data.get('unlike') is not None:
            if user in post.likes.all():
                post.likes.remove(user)
            
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)
