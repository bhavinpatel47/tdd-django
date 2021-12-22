from django.contrib import admin
from django.urls import path, include


import accounts.views

urlpatterns = [
    path('login', accounts.views.login, name='login'),
    path('send_login_email', accounts.views.send_login_email, name='send_login_email'),
    path('logout', accounts.views.logout, {'next_page': '/'}, name='logout'),
]
