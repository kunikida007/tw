from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'twiter'

urlpatterns = [
     path("home/",views.home,name="home"),
     path("list/",views.post_list,name="list"),
     path('post/',views.tweet, name='post-create'),
     path('tweet_detail/<int:pk>/',views.tweet_detail,name="tweet_detail"),
     path('delete_tweet/<int:pk>/', views.delete_tweet, name='delete_tweet'),
     path('accountpage/<int:user_id>/', views.accountpage, name='accountpage'),
]     
