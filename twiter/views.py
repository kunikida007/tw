from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST


@login_required
def home(request):
    return render(request, 'twiter/home.html')

@login_required
def tweet(request):
    if request.method == "POST":
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
        'tweet_list': models.Post.objects.select_related('author').all().order_by('-date_posted'),
    }
    return render(request, 'twiter/list.html', context)

@login_required
def tweet_detail(request, pk):
    tweet = get_object_or_404(models.Post, pk=pk)
    context = {
        'tweet': tweet,
    }
    return render(request, 'twiter/tweet_detail.html', context)    

@login_required
def delete_tweet(request, pk):
    user = request.user
    tweet = get_object_or_404(models.Post, pk=pk)
    if user == tweet.author:
        tweet.delete()
    return redirect('twiter:home',)

@login_required
def accountpage(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'tweet_list': models.Post.objects.filter(author=user_id).order_by('-date_posted'),
        'tweet_num': models.Post.objects.filter(author=user_id).count(),
    }
    return render(request, 'twiter/account.html', context)    

