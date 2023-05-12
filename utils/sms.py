import logging

from utils.validators import is_phone_number


def send_sms(text: str, phone: str):
    if not is_phone_number(phone):
        raise Exception('Invalid Phone Number')
    
    logging.info(f'send sms to {phone}')