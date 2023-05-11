from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def is_phone_number(phone: str) -> bool:
    if phone.startswith('09') and len(phone) == 11:
        return True
    else:
        return False


# this validator used for model field
def validate_phone(phone: str):
    if not phone.startswith('09') or len(phone) != 11:
        raise ValidationError(
            _('شماره تلفن %(value)s صحیح نمی‌باشد'),
            params={'value': phone},
        )