from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def home_page(request):
    response = HttpResponse("<html><title>To-Do lists</title></html>")
    return response
