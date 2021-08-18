from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('<int:user_id>/follow_list/', views.follow_list, name='follow_list'),
    path('<int:user_id>/follower_list/', views.follower_list, name='follower_list'),
    path('<int:user_id>/follow/', views.follow, name='follow'),
    path('<int:user_id>/unfollow/', views.unfollow, name='unfollow'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]
