from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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
    # TODO: ROUTE, VEHICLE


class MaintenancePerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='maintenance_person')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # TODO: JOB
