from django.test import TestCase,Client
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse, 
from django.contrib.auth.models import User
from .views import signup
from config import settings

class SigupTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('user:signup')

    def test_signup_view(self):

        response = self.client.get(self.index_url)
        # URLを取得できるか。
        self.assertEqual(response.status_code, 200)
        #テンプレートを表示するか
        self.assertTemplateUsed(response, 'user/signup.html')     

    def  test_post_fails_by_existed_user(self):

         User.objects.create_user("username1", '', 'yy660818')

         response = self.client.post(
         self.index_url, 
         {'username': 'username1', 'password1': 'yy660818', 'password2': 'yy660818'}
    )
        
        # ページ遷移が発生していないか。   
         self.assertEqual(response.status_code, 200)
            # テンプレートは正しいか。
         self.assertTemplateUsed(response, 'user/signup.html')
         # エラーは表示されているか。
         self.assertIn('このユーザーネームは既に使われています', response.context['form'].errors['username'])
          # ユーザー名は既に存在するのか？
         self.assertEqual(User.objects.filter(username='username1').count(), 1)

    def test_failed_with_common_password(self):
         response = self.client.post(
         self.index_url, 
         {'username': 'username1', 'password1': 'password', 'password2': 'password'}
    )

         # ページ遷移が発生していないか。   
         self.assertEqual(response.status_code, 200)
            # テンプレートは正しいか。
         self.assertTemplateUsed(response, 'user/signup.html')
         # エラーは表示されているか。
         self.assertIn('このパスワードは一般的すぎます。', response.context['form'].errors["password2"])
        
    def test_faild_with_diffrent_password(self):

        response = self.client.post(
         self.index_url, 
         {'username': 'username1', 'password1': 'yy660818', 'password2': 'yy660819'}
    )
         # エラーは表示されているか。
        self.assertIn('確認用パスワードが一致しません。', response.context['form'].errors["password2"])

    def test_failed_with_lack_password(self):
         response = self.client.post(
         self.index_url, 
         {'username': 'username1', 'password1': '81y', 'password2': '81y'}
    )
          # ページ遷移が発生していないか。   
         self.assertEqual(response.status_code, 200)
         # テンプレートは正しいか。
         self.assertTemplateUsed(response, 'user/signup.html')
         # エラーは表示されているか。
         self.assertIn('このパスワードは短すぎます。最低 8 文字以上必要です。', response.context['form'].errors["password2"])

         
    def test_save_user(self):

        data={'username': 'username6', 'password1': 'yy660818', 'password2': 'yy660818'}
        response = self.client.post(reverse('user:signup'), data=data) 

         #アカウントが作成されているか？
        self.assertEqual(User.objects.filter(username='username6').count(), 1)
         
class Login_test(TestCase):

    def test_with_not_existed_user(self):

        form = AuthenticationForm(data = {'username': "notexistuser", 'password': 'password_b'})

        #フォームが正しくないと認識する
        self.assertFalse(form.is_valid())
         # ユーザー名は存在していない。
        self.assertEqual(User.objects.filter(username='notexistuser').count(),0)
    def test_with_wrong_password(self):
        User.objects.create_user("username1", '', 'yy660818')
        data = {
            'username': "username1",
            'password': 'yy11111'
        }
        response = self.client.post(reverse('user:login'), data=data)

        # ユーザー名は存在する。
        self.assertEqual(User.objects.filter(username='username1').count(),1)
         # ページ遷移が発生しない。   
        self.assertEqual(response.status_code, 200)
        # エラーは表示されているか。
        self.assertIn("正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
                     response.context['form'].errors['__all__'])



    def test_with_correct_user(self):

         User.objects.create_user("username1", '', 'yy660818')
         data = {
            'username': "username1",
            'password': 'yy660818'
        }
         response = self.client.post(reverse('user:login'), data=data)

         # ユーザー名は存在する。
         self.assertEqual(User.objects.filter(username='username1').count(),1)
         # ページ遷移が発生するか。   
         self.assertEqual(response.status_code, 302)
         #twiterのホーム画面に移動
         self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))
    