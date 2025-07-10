from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.


def index(request):
    if request.method == "POST":
        return HttpResponse("You must have POSTed something")
    else:
        return HttpResponse(request.method)

class PostList(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'