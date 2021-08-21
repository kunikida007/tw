from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Favorite
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')

    def test_top_username_exist(self):
        response = self.client.get(reverse('twiter:home'))
        self.assertContains(response, self.user1.username)


class PostViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')

    def test_with_blankform(self):
        response = self.client.post(reverse('twiter:post_create'), content='', author=self.user1)
        self.assertIn('このフィールドは必須です。', response.context['form'].errors['content'])

    def test_post_redirect_nextpage(self):
        response = self.client.post(reverse('twiter:post_create'), {'content': 'ツイート後、ホームに戻るか？'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('twiter:home'))

    def test_by_another_user(self):
        User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username2', password='password_2')
        content = '別のユーザーからのツイートはできない'
        self.client.post(reverse('twiter:post_create'), {'content': content, 'author': self.user1})
        self.assertFalse(Post.objects.filter(author=self.user1, content=content).exists(),)

    def test_is_empty(self):
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)

    def test_tweet_in_database(self):
        content = 'ツイートはデータベース上に保存されるか？'
        self.client.post(reverse('twiter:post_create'), {'content': content})
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 1)


class DeleteTweetTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')

    def test_tweet_delete(self):
        content = 'ツイート消去'
        tweet1 = Post.objects.create(author=self.user1, content=content)
        self.client.post(reverse('twiter:delete_tweet', kwargs={'pk': tweet1.pk}))
        self.assertFalse(Post.objects.filter(author=self.user1, content=content).exists())

    def test_twwet_delete_with_correctuser(self):
        content = 'ツイート消去はユーザー1のみから行われるか'
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username2', password='password_2')
        Post.objects.create(author=self.user2, content=content)
        self.assertFalse(Post.objects.filter(author=self.user1, content=content).exists())


class PostModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')

    def test_with_over_length_tweet(self):
        content = '0' * 141
        self.client.post(reverse('twiter:post_create'), {'content': content, 'author': self.user1})
        self.assertFalse(Post.objects.filter(content=content).exists())


class ListTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')

    def test_tweet_in_list(self):
        self.timeline_list = []
        content = 'ツイートはリストに表示されるか？'
        Post.objects.create(author=self.user1, content=content)
        self.timeline_list.append(content)
        response = self.client.get(reverse('twiter:list'))
        queryset = response.context['tweet_list']
        self.assertEqual(queryset[0].content, self.timeline_list[0])

    def test_user_tweet_match(self):
        self.client.post(reverse('twiter:post_create'), {'content': 'ツイートはリストに表示されるか？'})
        response = self.client.get(reverse('twiter:list'))
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 1)
        self.assertContains(response, self.user1.username)

    def test_url_match_with_tweetdetail(self):
        content = 'ツイート詳細が正しく表示されるか？'
        tweet = Post.objects.create(author=self.user1, content=content)
        response = self.client.get(reverse('twiter:tweet_detail', kwargs={'pk': tweet.pk}))
        self.assertContains(response, content)


class FavoriteTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        content = "いいねに関するテスト"
        self.tweet1 = Post.objects.create(content=content, author=self.user1)

    def test_favorite_in_database(self):
        self.client.post(reverse('twiter:favorite', kwargs={'user_id': self.user1.pk,
                         'tweet_id': self.tweet1.pk}), favorite_user=self.user1, tweet=self.tweet1)
        self.assertTrue(Favorite.objects.filter(favorite_user=self.user1, tweet=self.tweet1).exists())


class UnFavoriteTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        content = "いいねに関するテスト"
        self.tweet1 = Post.objects.create(content=content, author=self.user1)
        self.client.post(reverse('twiter:favorite', kwargs={'user_id': self.user1.pk,
                         'tweet_id': self.tweet1.pk}), favorite_user=self.user2, tweet=self.tweet1)

    def test_unfavorite_succeed(self):
        self.client.post(reverse('twiter:unfavorite', kwargs={'user_id': self.user2.pk,
                         'tweet_id': self.tweet1.pk}), favorite_user=self.user2, tweet=self.tweet1)
        self.assertFalse(Favorite.objects.filter(favorite_user=self.user1, tweet=self.tweet1).exists())


class TweetFavoriteDetailTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        content = "いいねに関するテスト"
        self.tweet1 = Post.objects.create(content=content, author=self.user1)
        self.client.post(reverse('twiter:favorite', kwargs={'user_id': self.user1.pk,
                         'tweet_id': self.tweet1.pk}), favorite_user=self.user2, tweet=self.tweet1)

    def test_favorite_in_list(self):
        response = self.client.get(reverse('twiter:tweet_favorite_detail', kwargs={'pk': self.tweet1.pk}))
        self.assertContains(response, self.user1.username)
