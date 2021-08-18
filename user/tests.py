from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Follow


class SigupTest(TestCase):

    def setUp(self):
        self.index_url = reverse('user:signup')

    def test_get_succeeds(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_post_fails_by_existed_user(self):
        User.objects.create_user('username1', '', 'yy660818')
        response = self.client.post(
            self.index_url,
            {'username': 'username1', 'password1': 'yy660818', 'password2': 'yy660818'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertIn('このユーザーネームは既に使われています', response.context['form'].errors['username'])
        self.assertEqual(User.objects.filter(username='username1').count(), 1)

    def test_failed_with_common_password(self):
        response = self.client.post(
            self.index_url,
            {'username': 'username1', 'password1': 'password', 'password2': 'password'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertIn('このパスワードは一般的すぎます。', response.context['form'].errors['password2'])

    def test_failed_with_diffrent_password(self):
        response = self.client.post(
            self.index_url,
            {'username': 'username1', 'password1': 'yy660818', 'password2': 'yy660819'}
        )
        # エラーは表示されているか。
        self.assertIn('確認用パスワードが一致しません。', response.context['form'].errors['password2'])

    def test_failed_with_lack_password(self):
        response = self.client.post(
            self.index_url,
            {'username': 'username1', 'password1': '81y', 'password2': '81y'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertIn('このパスワードは短すぎます。最低 8 文字以上必要です。', response.context['form'].errors['password2'])

    def test_post_succeed(self):
        data = {'username': 'username6', 'password1': 'yy660818', 'password2': 'yy660818'}
        self.client.post(reverse('user:signup'), data=data)
        # アカウントが作成されているか？
        self.assertTrue(User.objects.filter(username='username6').exists())


class LoginTest(TestCase):

    def test_with_not_existed_user(self):
        form = AuthenticationForm(data={'username': 'notexistuser', 'password': 'password_b'})
        response = self.client.post(reverse('user:login'), data=form.data)
        # フォームが正しくないと認識する
        self.assertFalse(form.is_valid())
        # ユーザー名は存在していない。
        self.assertEqual(User.objects.filter(username='notexistuser').count(), 0)
        self.assertIn('正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。', response.context['form'].errors['__all__'])

    def test_with_wrong_password(self):
        User.objects.create_user('username1', '', 'yy660818')
        data = {
            'username': 'username1',
            'password': 'yy11111'
        }
        response = self.client.post(reverse('user:login'), data=data)
        self.assertEqual(User.objects.filter(username='username1').count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。', response.context['form'].errors['__all__'])

    def test_with_correct_user(self):
        User.objects.create_user('username1', '', 'yy660818')
        data = {
            'username': 'username1',
            'password': 'yy660818'
        }
        response = self.client.post(reverse('user:login'), data=data)
        self.assertEqual(User.objects.filter(username='username1').count(), 1)
        self.assertEqual(response.status_code, 302)


class LogoutTest(TestCase):
    def setup(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')

    def test_logout_redirect_loginform(self):
        response = self.client.post(reverse('user:logout'))
        self.assertRedirects(response, '/login/?next=/logout/')


class FollowTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username1', password='password_1')

    def test_user1_follow_user2(self):
        self.client.post(reverse('user:follow', kwargs={'user_id': self.user2.pk}))
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_user_cannot_follow_myself(self):
        self.client.post(reverse('user:follow', kwargs={'user_id': self.user1.pk}))
        self.assertFalse(Follow.objects.filter(follower=self.user1, following=self.user1).exists())


class UnFollowTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username1', password='password_1')

    def test_unfollow(self):
        self.client.post(reverse('user:follow', kwargs={'user_id': self.user2.pk}))
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())
        self.client.post(reverse('user:unfollow', kwargs={'user_id': self.user2.pk}))
        self.assertFalse(Follow.objects.filter(follower=self.user1, following=self.user2).exists())


class FollowListTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username1', password='password_1')

    def test_followlist_view(self):
        self.client.post(reverse('user:follow', kwargs={'user_id': self.user2.pk}))
        response = self.client.get(reverse('user:follow_list', kwargs={'user_id': self.user1.pk}))
        self.assertContains(response, self.user1)


class FollowerListTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username1', password='password_1')

    def test_followerlist_view(self):
        self.client.post(reverse('user:follow', kwargs={'user_id': self.user2.pk}))
        response = self.client.get(reverse('user:follower_list', kwargs={'user_id': self.user2.pk}))
        self.assertContains(response, self.user1)
