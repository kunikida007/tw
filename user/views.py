from django.shortcuts import render
from .forms import *
from django.shortcuts import redirect



# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SignUpForm()

    context = {'form':form}
    return render(request, 'user/signup.html', context)


