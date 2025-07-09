from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def about_me(request):
    return HttpResponse("This is the about page of the blog. Here you can find information about the blog and its author.")
