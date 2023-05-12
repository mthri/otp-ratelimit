from django.core.cache import cache
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from utils.blockip import FAILED_LOGIN_IP_PREFIX, MAX_ALLOWED_FAIL_LOGIN, extract_ip_from_request


# we can also use the `django-ratelimit` or `django-axe` library.
class IPBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        ip = extract_ip_from_request(request)
        ip_cache = cache.get(FAILED_LOGIN_IP_PREFIX+ip, {})

        block_it = False

        if conut := ip_cache.get('success_send_otp', False):
            if conut >= MAX_ALLOWED_FAIL_LOGIN:
                block_it = True
        
        if conut := ip_cache.get('failed_enter_otp', False):
            if conut >= MAX_ALLOWED_FAIL_LOGIN:
                block_it = True

        if conut := ip_cache.get('failed_login', False):
            if conut >= MAX_ALLOWED_FAIL_LOGIN:
                block_it = True
        
        if block_it and request.path not in ['/429', '/429/']:
            return redirect('error-429')

        response = self.get_response(request)
        return response

