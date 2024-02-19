

from django.urls import path, include
from . import views


app_name = 'user'

urlpatterns = [
    # path('',),
    path('signup', views.signup, name='Signup'),
    path('signin', views.signin, name='Signin'),
    path('logout', views.user_logout, name='Logout'),
    path('load-more-tweets/', views.load_tweets, name='load_more_tweets'),
    path('add-tweet/', views.add_tweet, name='add_tweet'),



]
