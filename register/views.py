from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from utils.blockip import FAILED_LOGIN_IP_TIMEOUT
from register.forms import CheckPhoneForm


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