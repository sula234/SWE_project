from django.db import models
from users.models import User


class report(models.Model):
    full_name = models.CharField(max_length=150)
    short_description = models.TextField(max_length=100)

    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'reports'

    def __str__(self):
        return self.full_name


class Image(models.Model):
    report = models.ForeignKey(
        report, on_delete=models.CASCADE, null=True
        )
    image = models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return self.report.full_name


class VechilePart(models.Model):
    report = models.ForeignKey(
        report, on_delete=models.CASCADE
        )
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name_plural = 'vechile part'

    def __str__(self):
        return self.name


class Task(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   title = models.CharField(max_length=200)
   description = models.TextField()
   category = models.CharField(max_length=100, blank=True, null=True)
   due_date = models.DateField(blank=True, null=True)
   priority = models.IntegerField(choices=((1, 'Low'), (2, 'Medium'), (3, 'High')), default=1)
   completed = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
     return self.title