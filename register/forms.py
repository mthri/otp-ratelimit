import logging
import random

from django import forms
from django.contrib.auth import login
from django.http import HttpRequest

from register.models import User
from utils.validators import validate_phone
from utils.sms import send_sms
from utils.blockip import success_login, failed_login


class CheckPhoneForm(forms.Form):
    phone = forms.CharField(max_length=11, min_length=11, required=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        validate_phone(phone)
        return phone
    
    @property
    def is_phone_exists(self):
        phone = self.cleaned_data['phone']
        return User.objects.filter(phone=phone).exists()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def authenticate(self, request: HttpRequest) -> User | None:
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        # if use default `authenticate`, check phone number
        user = User.objects.filter(username=username)
        if user.exists():
            user = user.first()
            if not user.check_password(password):
                user = None
            
        if user:
            login(request, user)
            success_login(request)
            return user
        else:
            failed_login(request)
            return None
