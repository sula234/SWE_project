from django.contrib import admin

from django.contrib import admin
from .models import User, Driver, FuelPreson, MaintenancePerson, Vehicle

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(FuelPreson)
admin.site.register(MaintenancePerson)
admin.site.register(Vehicle)
