from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', auth_views.LoginView.as_view(template_name="user/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="user:login"), name='logout'),
]    

#ログアウト機能は後で実装