from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import escape
from django.utils import timezone
from market.models import *

# Create your views here.

def index(request):
    return HttpResponse('<h1>Hello World</h1>')

def index2(request):
    return HttpResponse('<h1>matched "/test" </h1>')

"""
view take in a 'request' as a parameter
view must return an HttpResponse object
"""