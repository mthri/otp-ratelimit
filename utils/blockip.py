from django.http import HttpRequest
from django.core.cache import cache
import logging

from decouple import config


FAILED_LOGIN_IP_TIMEOUT = config('FAILED_LOGIN_IP_TIMEOUT', cast=int, default=3600) # means 1 hour
FAILED_LOGIN_IP_PREFIX = config('FAILED_LOGIN_IP_PREFIX', cast=str, default='FAILED_IP_')
MAX_ALLOWED_FAIL_LOGIN = config('MAX_ALLOWED_FAIL_LOGIN', cast=int, default=3)


def extract_ip_from_request(request: HttpRequest) -> str:
    ''' extract the IP address from the request '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def failed_login(request: HttpRequest) -> None:
    ''' if request the IP address exists, decrease the failed login count. Otherwise, add it '''
    ip = extract_ip_from_request(request)
    ip_cache_count = cache.get(FAILED_LOGIN_IP_PREFIX+ip)
    if ip_cache_count == None:
        ip_cache_count = 0
    
    logging.info(f'set {ip} as failedlogin')
    cache.set(FAILED_LOGIN_IP_PREFIX+ip, ip_cache_count+1, FAILED_LOGIN_IP_TIMEOUT)


    