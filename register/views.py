from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.contrib.auth import logout, login

from utils.blockip import FAILED_LOGIN_IP_TIMEOUT, success_login
from register.forms import CheckPhoneForm, LoginForm, CreateUserForm, OTPFrom


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
            form = OTPFrom(request.POST)
            form.is_valid()
            form.send_otp(request)
            return redirect(reverse('sign-up-step-1'))

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
    

class SignUpStep1View(View):
    ''' confirm phone number with OTP '''
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_anonymous:
            logout(request)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = OTPFrom(request.POST)
        form.is_valid()
        if request.session.get('otp', False) and not form.verify_otp(request):
            return render(request, 'register/sign_up_step_1.html', context={
                'error_message': _('کد ورودی اشتباه می‌باشد')
            })
        else:
            return redirect(reverse('sign-up-step-2'))
    
    def get(self, request, *args, **kwargs):
        return render(request, 'register/sign_up_step_1.html')



class SignUpStep2View(View):
    ''' fill information '''
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_anonymous:
            logout(request)
        
        if not request.session.get('phone_verified', False):
            return redirect(reverse('sign-up-step-1'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs): 
        form = CreateUserForm(request.POST)
        if not form.is_valid():
            return render(request, 'register/sign_up_step_2.html', context={'form': form})
        else:
            user = form.save(request)
            login(request, user)
            success_login(request)
            return redirect('/admin')
    
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        return render(request, 'register/sign_up_step_2.html', context={'form': form})