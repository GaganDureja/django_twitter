from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout 
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
    
    all_tweets = Tweet.objects.all()
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


def add_tweet(request):
    pass