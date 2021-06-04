from django.test import TestCase,Client
from user.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import signup
from config import settings

username = "onoderayuto"
username2 = "new_username" 

class  TestUrls(TestCase):

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

class Test_signup_get_Views(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('user:signup')


    def test_signup_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')

class Sigup_post_Tests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username, '', 'password_a')


    def test_already_existed_name(self):

        form = UserCreationForm({'username': username, 'password1': 'password_b', 'password2': 'password_b'})
        self.assertFalse(form.is_valid())


    def test_same_password(self):

        form = UserCreationForm({'username': username2, 'password1': 'password1', 'password2': 'password2'})
        self.assertFalse(form.is_valid())   

    def test_save_user(self):

        form = UserCreationForm({'username': username2, 'password1': 'password_b', 'password2': 'password_b'})
        form.save()
        self.assertTrue(User.objects.filter(username='new_username').exists())  


class Login_tests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username, '', 'password_a')

    def test_with_correct_user(self):

        form = AuthenticationForm(data = {'username': username, 'password': 'password_a'})
        self.assertTrue(form.is_valid())
        data = {
            'username': username,
            'password': 'password_a'
        }
        response = self.client.post(reverse('user:login'), data=data)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_with_not_existed_user(self):

        form = AuthenticationForm(data = {'username': username2, 'password': 'password_b'})
        self.assertFalse(form.is_valid())            

