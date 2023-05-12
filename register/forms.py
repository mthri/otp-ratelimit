import logging
import random
from datetime import datetime

from django import forms
from django.contrib.auth import login, password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest

from register.models import User
from utils.validators import validate_phone
from utils.sms import send_sms
from utils.blockip import success_login, failed_login, success_send_otp, failed_enter_otp


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


class OTPFrom(forms.Form):
    phone = forms.CharField(max_length=11, min_length=11)
    otp = forms.IntegerField(required=False)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        validate_phone(phone)
        return phone
    
    def send_otp(self, request: HttpRequest) -> None:
        ''' get request for set value to session '''

        phone = self.cleaned_data['phone']
        otp = random.randint(11111, 99999)

        send_sms(f'کد یکبار مصرف شما: {otp}', phone)
        request.session['phone'] = phone
        request.session['otp'] = otp
        # request.session['send_otp_time'] = datetime.now().timestamp()
        success_send_otp(request)
        print(f'OTP {otp}')

    def verify_otp(self, request: HttpRequest) -> bool:
        otp = self.cleaned_data['otp']

        # also we can check for otp is expired or not with `send_otp_time`
        if otp == request.session['otp']:
            request.session['phone_verified'] = True
            return True
        else:
            failed_enter_otp(request)
            return False


class CreateUserForm(forms.ModelForm):

    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name'
        ]


    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError(_('گذرواژه ها با هم مطابقت ندارند'))
        
        password_validation.validate_password(password2)
        return password2
    
    def save(self, request: HttpRequest) -> User:
        phone_verified = request.session.get('phone_verified', False)
        if phone_verified == False:
            raise Exception('phone not verified')
        
        phone = request.session['phone']
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        password = self.cleaned_data['password1']

        # clear session for register value
        for key in ['phone_verified', 'otp', 'phone']:
            request.session.pop(key, None)

        user = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            is_active = True,
            is_staff = True,
        )
        user.set_password(password)
        user.save()

        return user