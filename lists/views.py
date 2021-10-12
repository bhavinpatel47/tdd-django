from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item


def home_page(request: HttpRequest):
    # TODO: Support more than 1 list
    # TODO: Display multiple items in the table

    if request.method == "POST":
        Item.objects.create(text=request.POST.get('item_text'))
        return redirect("/")
    items = Item.objects.all()
    return render(request, "home.html", {'items': items})
