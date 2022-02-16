from django.contrib import messages, auth
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import redirect, render

from accounts.models import Token, User


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' +str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'numbmonke@gmail.com', 
        [email])


    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in.",
        )
    return redirect('/')

def login(request):
    token_uid = request.GET.get('token')
    user = auth.authenticate(request, token_uid=token_uid)

    if user:
        auth.login(request, user)
    return redirect('/')
