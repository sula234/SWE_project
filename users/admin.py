from django.contrib import admin
from .models import Auction, AuctionImage, Route, User, Driver, FuelPreson, MaintenancePerson, Vehicle, FuelReport

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(FuelPreson)
admin.site.register(MaintenancePerson)
admin.site.register(Vehicle)
admin.site.register(Route)
admin.site.register(Auction)
admin.site.register(AuctionImage)
admin.site.register(FuelReport)
