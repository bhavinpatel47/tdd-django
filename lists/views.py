from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import Item, List

User = get_user_model()

def home_page(request: HttpRequest):
    return render(request, "home.html", {'form': ItemForm()})

def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
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

def my_lists(request, email):
    owner = User.objects.get(email=email)
    context={'owner': owner}
    return render(request, 'my_lists.html', context=context)