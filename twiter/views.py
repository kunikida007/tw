from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from user.models import Follow
from .models import Favorite, Post


@login_required
def home(request):
    return render(request, 'twiter/home.html')


@login_required
def tweet(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('twiter:home')
    else:
        form = PostForm()
    return render(request, 'twiter/post_create.html', {'form': form})


@login_required
def post_list(request):
    user = request.user
    context = {
        'user': user,
        'tweet_list': Post.objects.select_related('author').all().order_by('-date_posted'),
    }
    return render(request, 'twiter/list.html', context)


@login_required
def tweet_detail(request, pk):
    tweet = get_object_or_404(Post, pk=pk)
    favorited = Favorite.objects.filter(tweet=tweet, user=request.user).exists()
    context = {
        'tweet': tweet,
        'favorited': favorited,
    }
    return render(request, 'twiter/tweet_detail.html', context)


@login_required
def delete_tweet(request, pk):
    user = request.user
    tweet = get_object_or_404(Post, pk=pk)
    if tweet.perms_user(user):
        tweet.delete()
    return redirect('twiter:home',)


@login_required
def accountpage(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'tweet_list': Post.objects.filter(author=user_id).order_by('-date_posted'),
        'tweet_num': Post.objects.filter(author=user_id).count(),
        'is_following': Follow.objects.filter(follower__username=request.user.username, following__username=user.username).exists(),
    }
    return render(request, 'twiter/account.html', context)


@login_required
def favorite(request, user_id, tweet_id):
    tweet = get_object_or_404(Post, pk=tweet_id)
    user = request.user
    Favorite.objects.get_or_create(tweet=tweet, user=user)
    return redirect('twiter:tweet_detail', tweet.pk)


@login_required
def unfavorite(request, user_id, tweet_id):
    tweet = get_object_or_404(Post, pk=tweet_id)
    user = request.user
    favorite = get_object_or_404(Favorite, tweet=tweet, user=user)
    favorite.delete()
    return redirect('twiter:tweet_detail', tweet.pk)


@login_required
def tweet_favorite_detail(request, tweet_id):
    context = {
        'favorite_user_list': Favorite.objects.filter(tweet__pk=tweet_id).select_related('user').order_by('created_at')
        }
    return render(request, 'twiter/tweet_favorite_detail.html', context)
