import logging
import random

from django import forms

from register.models import User
from utils.validators import is_phone_number, validate_phone
from utils.sms import send_sms


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
