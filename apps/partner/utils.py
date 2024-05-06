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


def generate_qr_code(establishment, domain):
    url = f"{domain}/api/v1/partner/menu/{establishment.id}/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    filename = f"qr_code_{establishment.name}.png"
    return filename, buffer.getvalue()
