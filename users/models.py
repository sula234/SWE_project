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

    def __str__(self):
        return self.user

    # TODO: FUELING INFO

    
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='driver')
    uin = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12, unique=True)
    driving_license = models.CharField(max_length=24, unique=True)

    def __str__(self) -> str:
        return f'{self.user} ({self.first_name} {self.last_name})'


class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=0)                          # 1 - active, 0 - inactive
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=32)
    capacity = models.IntegerField()
    mileage = models.IntegerField()
    cost = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.manufacturer} {self.model} {self.license_plate}'

class FuelReport(models.Model):
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(Driver, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    cost = models.FloatField(default=0.0)
    fuelAmount = models.FloatField(default=0.0)
    totalCost = models.FloatField(default=0.0)
    driverPhoto = models.ImageField(upload_to='images/')
    carPhoto = models.ImageField(upload_to='images/')
    fuelLevelPhotoBefore = models.ImageField(upload_to='images/')
    fuelLevelPhotoAfter = models.ImageField(upload_to='images/')



class Route(models.Model):
    enums = [
        ('pending', 'pending'),
        ('in_progress', 'in_progress'),
        ('finished', 'finished'),
        ('delayed', 'delayed'),
        ('canceled', 'canceled'),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_staff": True})
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    distance = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=None, null=True)
    finish_time = models.DateTimeField(default=None, null=True)
    status = models.CharField(max_length=16, choices=enums, default='pending')

    def __str__(self):
        return f'{self.driver} {self.vehicle} -> {self.destination}'
    def duration(self):
        if (self.finish_time is not None and self.start_time is not None):
             return self.finish_time - self.start_time


class MaintenancePerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='maintenance_person')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    # TODO: JOB
