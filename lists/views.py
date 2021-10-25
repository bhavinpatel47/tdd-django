from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, "home.html", {'form': ItemForm()})


def new_list(request: HttpRequest):
    form = ItemForm(data=request.POST)
    if form.is_valid():

        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request: HttpRequest, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.html", {'list': list_, "form": form})
