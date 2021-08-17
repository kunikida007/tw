from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Follow
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'user/login.html')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'user/signup.html', context)


@login_required
def logout(request):
    django_logout(request)
    return redirect('user:login')


@login_required
def follow(request, user_id):
    follower = request.user
    following = get_object_or_404(User, pk=user_id)
    if follower != following:
        Follow.objects.get_or_create(follower=follower, following=following)
    else:
        pass
    return redirect('twiter:accountpage', user_id)


@login_required
def unfollow(request, user_id):
    follower = request.user
    following = get_object_or_404(User, pk=user_id)
    follow = get_object_or_404(Follow, follower=follower, following=following)
    follow.delete()
    return redirect('twiter:accountpage', user_id)


@login_required
def follower_list(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'follower_list': Follow.objects.filter(following__username=user.username).select_related('follower').order_by('-followed_date'),
    }
    return render(request, 'user/follower_list.html', context)


@login_required
def follow_list(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'follow_list': Follow.objects.filter(follower__username=user.username).select_related('following').order_by('-followed_date'),
    }
    return render(request, 'user/follow_list.html', context)
