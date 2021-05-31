from django.test import TestCase,Client
from user.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, resolve
from django.contrib.auth.models import AbstractUser as User
from .views import signup

class  TestUrls(TestCase):
    
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

class TestsignupViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('user:signup')
     

    def test_signup_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')

#ユーザー名未入力のまま登録ボタンを押すとFalseを返す
class Testforms(TestCase):
   def test_usernone(self):
        params = dict(
            name='',
            password="yY660818"
        )
        form = SignUpForm(params)
        self.assertTrue(form.is_valid())
        