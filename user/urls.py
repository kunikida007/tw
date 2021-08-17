from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('follow_list/<int:user_id>/', views.follow_list, name='follow_list'),
    path('follower_list/<int:user_id>/', views.follower_list, name='follower_list'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('logout/', views.logout, name='logout'),
]
