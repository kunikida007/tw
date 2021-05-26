from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Post
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home(request):
    return render(request, 'twiter/home.html')



class PostListView(ListView):
    model = Post
    template_name = "tweet/list.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class PostCreateView(CreateView):
    model = Post
    fields = ['content']
    template_name = 'twiter/post_create.html'
    success_url = 'home/'

