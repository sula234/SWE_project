from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import user_passes_test
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

def is_admin(user):
    return user.is_authenticated and user.is_staff


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_fuel_person = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_maintenance_person = models.BooleanField(default=False)
    

class FuelPreson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='fuel_person')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    g_station_name = models.CharField(max_length=100)

    # TODO: FUELING INFO

    
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='driver')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=0)                          # 1 - active, 0 - inactive
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=10)
    capacity = models.IntegerField()
    mileage = models.IntegerField()
    cost = models.IntegerField(default=0)


class Route(models.Model):
    enums = [
        ('pending', 'pending'),
        ('in_progress', 'in_progress'),
        ('finished', 'finished')
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_admin": True})
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=None, null=True)
    finish_time = models.DateTimeField(default=None, null=True)
    status = models.CharField(choices=enums, default='pending')


class MaintenancePerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='maintenance_person')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # TODO: JOB
