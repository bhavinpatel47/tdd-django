from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError as e:
            error = "You can't have an empty list item"
    return render(request, "list.html", {'list': list_, 'error': error})


def new_list(request: HttpRequest):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError as e:
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(list_)
