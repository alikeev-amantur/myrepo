from django.db import models

from apps.partner.models import Establishment


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Beverage(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    availability_status = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="beverages"
    )

    establishment = models.ForeignKey(
        Establishment, on_delete=models.CASCADE, related_name="beverages"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Beverage"
        verbose_name_plural = "Beverages"
        ordering = ["name"]
