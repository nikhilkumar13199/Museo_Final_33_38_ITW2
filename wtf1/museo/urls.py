from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth import urls

from .feed import LatestEntriesFeed

app_name='museo'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.login, {'template_name':'login.html'},name='login'),
    path('logout/',auth_views.logout,{'template_name':'logged_out.html'},name='logout'),
    path('feed/',views.feed,name='feed'),
    path('createpost/',views.createpost,name='createpost'),
    path('topusers/',views.topusers,name='topusers'),
    path('',views.index2,name='index2'),
    path('profile/',views.profile,name='profile'),
    path('rssfeed/',LatestEntriesFeed()),
]

#latestentriesfeed() is the feed class in feed.py