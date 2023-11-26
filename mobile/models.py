from django.db import models


# Create your models here.
class Dispatcher(models.Model):
    dispatcher_phone_number = models.CharField(max_length=20)
