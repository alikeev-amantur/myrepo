from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Establishment


class EstablishmentAdmin(gis_admin.OSMGeoAdmin):
    pass


admin.site.register(Establishment, EstablishmentAdmin)
