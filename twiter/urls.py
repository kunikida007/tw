from django.urls import path
from . import views

app_name = 'twiter'

urlpatterns = [
     path('home/', views.home, name='home'),
     path("list/", views.post_list, name='list'),
     path('post_create/', views.tweet, name='post_create'),
     path('tweet_detail/<int:pk>/', views.tweet_detail, name='tweet_detail'),
     path('delete_tweet/<int:pk>/', views.delete_tweet, name='delete_tweet'),
     path('accountpage/<int:user_id>/', views.accountpage, name='accountpage'),
     path('favorite/<int:user_id>/<int:tweet_id>/', views.favorite, name='favorite'),
     path('unfavorite/<int:user_id>/<int:tweet_id>/', views.unfavorite, name='unfavorite'),
     path('tweet_favorite_detail/<int:pk>/', views.tweet_favorite_detail, name='tweet_favorite_detail'),

]
