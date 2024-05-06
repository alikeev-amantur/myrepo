from django.contrib import admin

from apps.beverage.models import Category, Beverage


# Register your models here.
admin.site.register(Category)
admin.site.register(Beverage)
