from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

import accounts.views

urlpatterns = [
    path('login', accounts.views.login, name='login'),
    path('send_login_email', accounts.views.send_login_email, name='send_login_email'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
]
