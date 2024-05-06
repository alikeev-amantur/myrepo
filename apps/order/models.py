from django.contrib.auth import get_user_model
from django.db import models

from apps.beverage.models import Beverage
from apps.partner.models import Establishment

User = get_user_model()


# Create your models here.
class Order(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='orders')
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE,
                                 related_name='orders')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
