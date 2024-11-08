from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Core app is working!")