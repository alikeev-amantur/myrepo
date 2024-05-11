import re
from io import BytesIO
import qrcode

from rest_framework.exceptions import ValidationError


def phone_number_validation(validated_data):
    """
    Checks phone number format
    :param validated_data:
    :return:
    """
    phone_pattern = r"^996\d{9}$"
    if "phone_number" in validated_data:
        if not re.match(phone_pattern, validated_data["phone_number"]):
            raise ValidationError("Invalid phone number. Must be kgz national format")
