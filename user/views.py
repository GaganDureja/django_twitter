from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

# Create your views here.



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


            
            User.objects.create(
                password = make_password(request.POST.get('password')),
                username= request.POST.get('email'),
                first_name = request.POST.get('name'),
                email=request.POST.get('email')
            )

            # messages.success(request, "Please verify your email to continue")
            messages.success(request, "Login to continue")
            return redirect('index')            
            return redirect('users:Signup')
        

def signin(request):
    next_url =  request.POST.get('next')
    
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in")
        return redirect('index')
    else:
        if request.method == 'GET':
            return redirect('index')
            
        if request.method == 'POST':
            if User.objects.filter(email=request.POST.get('email')):
                user = authenticate(
                        request, 
                        username=request.POST.get('email'), 
                        password=request.POST.get('password')
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
                messages.warning(request, "Email not registered")      
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
    all_tweets = Tweet.objects.all().order_by('-id')
    if request.GET.get('tweet_type')=="any":
        pass
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
   
    # tweet_type = 0,
    # if request.POST.get('files[]'):
    #     tweet_type = 1

    user_mentions = ""
    tags_used = ""
    # mentions = user_mentions,
    # tweet_tags = tags_used

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
                    tag = Tags.objects.filter(name=tag)
                    tag.used_times +=1
                    tag.save()
                else:                    
                    Tags.objects.create(name=tag)
            for mension in mentions:
                if User.objects.filter(username=mension).exists():
                    Tweet.mentions.add(mension)

        tweet = Tweet.objects.create(
            user = request.user,
            msg = tweet_message,
            reply_by = request.POST.get('reply_type'),
            reply_to = reply_to,
            repost_tweet = reposting,
            
        )
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