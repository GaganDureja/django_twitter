from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

# Create your views here.


import random
def signup(request):    
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in")
        return redirect('index')
        # return render('home/home.html')
    else:
        if request.method == 'GET':
            return redirect('index')
        if request.method == 'POST':
            email = request.POST.get('email')
            if not email:
                messages.warning(request, "Email required")
                return redirect('index')
            if User.objects.filter(email=email):
                messages.warning(request, "User already exists with this email")
                return redirect('index')

            full_name = request.POST.get('name')  
            user_name = full_name
            while User.objects.filter(username=user_name).exists():
                random_number = random.randint(1, 9999)
                user_name = f"{full_name}{random_number}"

            User.objects.create(
                password = make_password(request.POST.get('password')),
                username = user_name,
                first_name = full_name,
                email=request.POST.get('email')
            )

            # messages.success(request, "Please verify your email to continue")
            messages.success(request, "Login to continue")
            return redirect('index')            
            return redirect('users:Signup')
        
from django.db.models import Q

def signin(request):
    next_url =  request.POST.get('next')
    
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in")
        return redirect('index')
    else:
        if request.method == 'GET':
            return redirect('index')
            
        if request.method == 'POST':

            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(Q(email=email) | Q(phone=email) | Q(username=email)):
                user = authenticate(
                        request,
                        username=email,
                        password=password
                    )


                if user:
                    login(request, user)    
                    messages.success(request, "Login success")
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('index')
                else:
                    messages.error(request, "Incorrect password!!!")
                return redirect('index')       
            else:
                messages.warning(request, "Account not found")      
                return redirect('index')       
                # return render(request,'index')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout success")
    else:
        messages.warning(request, "Already Logged out")
    return redirect('index')   


def check_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'home/index.html')

def home(request):
    if request.user.is_authenticated:        
        return render(request,'home/home.html')
    return redirect('index')


from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def load_tweets(request):

    following_users = request.user.followers.all()
    all_tweets = Tweet.objects.all().order_by('-id')
    if request.GET.get('tweet_type')=="any":
        all_tweets = Tweet.objects.all().order_by('-id')
    else:
        all_tweets = Tweet.objects.filter(user__in=following_users).order_by('-id')
    page = request.GET.get('page')    
    paginator = Paginator(all_tweets, 2)  # Adjust per_page as needed
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = []

    tweets_html = render_to_string('home/tweet_list_ajax.html', {'tweets': tweets})
    return JsonResponse({'tweets_html': tweets_html})

import re
def extract_tags_and_mentions(text):
    # Regular expression patterns for extracting hashtags and mentions
    hashtag_pattern = r'#\w+'
    mention_pattern = r'@\w+'

    # Find all hashtags and mentions in the text
    hashtags = re.findall(hashtag_pattern, text)
    mentions = re.findall(mention_pattern, text)
    hashtags = [tag[1:] for tag in hashtags]
    mentions = [mention[1:] for mention in mentions]

    return hashtags, mentions


@login_required
def add_tweet(request):

    if request.POST.get('reply_to'):
        reply_to = request.POST.get('reply_to')
    else:
        reply_to = None

    if request.POST.get('repost_tweet'):
        reposting = request.POST.get('repost_tweet')
    else:
        reposting = None

    if reposting==None and request.POST.get('message')=="" and not request.FILES:
        messages.warning(request, "Message cannot be empty")

    else:
        if request.POST.get('message'):
            tweet_message = request.POST.get('message')
            hashtags, mentions = extract_tags_and_mentions(tweet_message)

            for tag in hashtags:
                if Tags.objects.filter(name=tag).exists():
                    tag = Tags.objects.filter(name=tag).first()
                    tag.used_times +=1
                    tag.save()
                else:                    
                    Tags.objects.create(name=tag)
            

        tweet = Tweet.objects.create(
            user = request.user,
            msg = tweet_message,
            reply_by = request.POST.get('reply_type'),
            reply_to = reply_to,
            repost_tweet = reposting,
            
        )
        for mention in mentions:
                mention_user = User.objects.filter(username=mention)
                if mention_user.exists():
                    tweet.mentions.add(mention_user.first())
        if 'files' in request.FILES:
            files = request.FILES.getlist('files')
            if files:
                tweet.tweet_type = 1
                tweet.save()
                for i in request.FILES.getlist('files'):
                    tweet.tweet_media.add(T_Media.objects.create(file_name=i))
        messages.success(request, "Tweet uploaded")
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))



from django.urls import reverse
from django.shortcuts import get_object_or_404
@login_required
def follow_user(request, follow_to):
    current_user = request.user
    user_to_follow = get_object_or_404(User, pk=follow_to)    

    messages.info(request, "Already Following")

    if not current_user.followers.filter(pk=user_to_follow.pk).exists():
        current_user.followers.add(user_to_follow)
        messages.success(request, "Following Successfully")

    return redirect(request.META.get('HTTP_REFERER', reverse('home')))
 


@login_required
def unfollow_user(request, unfollow_to):
    current_user = request.user
    user_to_unfollow = get_object_or_404(User, pk=unfollow_to)
    messages.info(request, "Already not Following")
    if current_user.followers.filter(pk=user_to_unfollow.pk).exists():
        current_user.followers.remove(user_to_unfollow)
        messages.success(request, "Removed from Following")
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))

@login_required
def bookmark(request, tweet_id):
    current_user = request.user
    tweet_id = get_object_or_404(Tweet, pk=tweet_id)
    if current_user.bookmarks.filter(pk=tweet_id.pk).exists():
        current_user.bookmarks.remove(tweet_id)
        messages.success(request, "Bookmark removed")
    else:
        current_user.bookmarks.add(tweet_id)
        messages.success(request, "Bookmark added")
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))

    
def user_page(request, username):
    user_det = get_object_or_404(User, username=username)
    total_tweets = Tweet.objects.filter(user=user_det.id).count()
    number_of_followers = User.objects.filter(followers=user_det.id).count()
    return render(request,'user/profile.html', {'user_det':user_det, 'total_tweets':total_tweets, 'number_of_followers':number_of_followers})


def search(request, q=None):
    return render(request,'home/search.html')

def notification(request, q=None):
    return render(request,'user/notification.html')

def message(request, q=None):
    return render(request,'user/message.html')

def bookmark(request, q=None):
    return render(request,'user/bookmark.html')