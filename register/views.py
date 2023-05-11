from django.shortcuts import render 
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from utils.blockip import FAILED_LOGIN_IP_TIMEOUT


def error_429(request) -> HttpResponse:
    content = {
        'message': _(f'لطفا بعد از {FAILED_LOGIN_IP_TIMEOUT//60} دقیقه مجددا تلاش کنید')
    }
    return render(request, 'register/429.html',context=content, status=429)
