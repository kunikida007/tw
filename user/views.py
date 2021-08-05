from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'user/login.html')
    else:
        form = SignUpForm()

    context = {'form':form}
    return render(request, 'user/signup.html', context)
    