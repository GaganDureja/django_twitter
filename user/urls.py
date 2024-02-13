

from django.urls import path, include
from . import views


app_name = 'user'

urlpatterns = [
    # path('',),
    path('signup', views.signup, name='Signup'),
    path('signin', views.signin, name='Signin')

]
