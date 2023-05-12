from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.contrib.auth import logout

from utils.blockip import FAILED_LOGIN_IP_TIMEOUT
from register.forms import CheckPhoneForm, LoginForm


def error_429(request: HttpRequest) -> HttpResponse:
    content = {
        'message': _(f'لطفا بعد از {FAILED_LOGIN_IP_TIMEOUT//60} دقیقه مجددا تلاش کنید')
    }
    return render(request, 'register/429.html',context=content, status=429)


class CheckPhoneView(View):
    def post(self, request, *args, **kwargs):
        form = CheckPhoneForm(request.POST)
        if form.is_valid() is not True:
            return render(request, 'register/check_phone.html', context={'form': form})
        
        if form.is_phone_exists:
            return redirect('sign-in')
        else:
            return redirect('sign-up')


    def get(self, request, *args, **kwargs):
        return render(request, 'register/check_phone.html')
    

class SignInView(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_anonymous:
            logout(request)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        
        if not form.is_valid():
            return render(request, 'register/sign_in.html', context={'form': form})
        
        user = form.authenticate(request)

        if not user:
            content = {
                'form': form, 
                'error_message': _('نام‌کاربری یا گذرواژه اشتباه می‌باشد')
            }
            return render(request, 'register/sign_in.html', context=content)
        
        return redirect('/admin')


    def get(self, request, *args, **kwargs): 
        return render(request, 'register/sign_in.html')