from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'twiter'

urlpatterns = [
    path('home/', views.home,name="home"),
     path('', views.PostListView.as_view(), name='index'),
    path('post/', views.PostCreateView.as_view(), name='post-create'),
]  