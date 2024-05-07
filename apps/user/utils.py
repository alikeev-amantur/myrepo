import datetime
import json
import random

from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def generate_reset_code():
    return random.randint(1000, 9999)


def datetime_serializer(obj):
    datetime_str = str(obj)
    return json.dumps({"date": datetime_str})


def datetime_deserializer(obj):
    loaded_json = json.loads(obj)
    return datetime.datetime.strptime(loaded_json["date"], "%Y-%m-%d %H:%M:%S.%f")


def send_reset_code_email(email, code):
    subject = "Password Reset Code"
    body = f"Your reset code: {code}"
    from_email = EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, body, from_email, recipient_list, fail_silently=False)
