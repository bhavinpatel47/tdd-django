"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


import lists.views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', lists.views.home_page, name="home"),
    path('lists/<int:list_id>/', lists.views.view_list, name='view_list'),
    path('lists/<int:list_id>/add_item', lists.views.add_item, name='add_item'),
    path('lists/new', lists.views.new_list, name='new_list'),
]
