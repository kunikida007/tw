from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from django.urls import reverse
from django.core.exceptions import ValidationError

class HomeViewTest(TestCase):
 
    def test_top_username_exist(self):
        self.user1 = User.objects.create_user('username1', '','password_1')
        self.client.login(username='username1', password='password_1')
        response = self.client.get(reverse('twiter:home'))
        #ホーム画面に自分のユーザー名が表示されるか
        self.assertContains(response, self.user1.username)    

class PostViewTest(TestCase):
    
    def test_with_blankform(self):
        self.user1 = User.objects.create_user('username1', '','password_1')
        self.client.login(username='username1', password='password_1')
        response = self.client.post(reverse('twiter:post-create'), {'content': ''})
        self.assertIn('このフィールドは必須です。',response.context['form'].errors['content'])

    def test_post_redirect_nextpage(self):
        self.user1 = User.objects.create_user('username1', '','password_1')
        self.client.login(username='username1', password='password_1')
        response = self.client.post(reverse('twiter:post-create'), {'content': 'ツイート後、ホームに戻るか？'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('twiter:home'))

    def test_by_another_user(self):
        self.user1 = User.objects.create_user('username1', '','password_1')
        self.client.login(username='username1', password='password_1')
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username2', password='password_2')
        self.client.post(reverse('twiter:post-create'), {'content': 'this is test_tmeet_rqedirect', 'author': self.user1})
        self.assertFalse(Post.objects.filter(author=self.user1).exists())

    def test_is_empty(self):
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)    

    def test_tweet_in_database(self):
        self.user1 = User.objects.create_user('username1', '','password_1')
        self.client.login(username='username1', password='password_1')
        response = self.client.post(reverse('twiter:post-create'), {'content': 'ツイートはデータベースに保存されるか？'})
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 1)

class DeleteTweetTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')

    def test_tweet_delete(self):
        content="ツイート消去"
        tweet1=Post.objects.create(author=self.user1,content=content)
        self.client.post(reverse("twiter:delete_tweet",kwargs={'pk':tweet1.pk})) 
        self.assertFalse(Post.objects.filter(author=self.user1, content=content).exists())

    def test_twwet_delete_with_correctuser(self):
        content="ツイート消去はユーザー1のみから行われるか"
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username2', password='password_2')
        tweet=Post.objects.create(author=self.user1,content=content)
        self.assertTrue(Post.objects.filter(author=self.user1, content=content).exists())
    
class PostModelTest(TestCase):
  
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
 
    def test_with_over_length_tmeet(self):
        content = "1234567"
        for i in range(21):
            content += "1234567"
        test_tweet = Post.objects.create(author=self.user1, content=content)
        self.assertRaises(ValidationError)

class ListTest(TestCase):
      
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')
    
    def test_tweet_in_list(self):
        self.timeline_list = []
        content = 'ツイートはリストに表示されるか？'
        Post.objects.create(author=self.user1,content=content)
        self.timeline_list.append(content)
        response = self.client.get(reverse('twiter:list'))
        queryset = response.context['tweet_list']
        self.assertEqual(queryset[0].content, self.timeline_list[0])
    
    def test_user_tweet_match(self):
        response = self.client.post(reverse('twiter:post-create'), {'content': 'ツイートはリストに表示されるか？'})
        response2= self.client.get(reverse('twiter:list'))
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 1) 
        self.assertContains(response2, self.user1.username)

    def test_url_match_with_tweetdetail(self):
        content = 'ツイート詳細が正しく表示されるか？'
        tweet1=Post.objects.create(author=self.user1,content=content)
        response= self.client.get(reverse('twiter:tweet_detail',kwargs={'pk':tweet1.pk}))
        self.assertContains(response,content)
        