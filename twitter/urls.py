"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

from user.views import *
from django.conf import settings 
from django.conf.urls.static import static 



urlpatterns = [
    # path('', TemplateView.as_view(template_name='home/index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('', check_login , name='index'),
    path('home', home, name='home'),
    path('status/<int:tweet_id>/', tweet_details, name='tweet_details'),
    path('user/', include('user.urls')),
    path('search/', search, name='search'),
    path('notification/', notification, name='notification'),
    path('message/', message, name='message'),
    path('bookmark/', bookmark, name='bookmark'),
    path('<str:username>/', user_page, name='user_page'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
