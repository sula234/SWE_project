from django.db import models

from users.models import User

class Report(models.Model):

    title = models.CharField(max_length=250)

    fixed_parts = models.CharField(max_length=250, default='un-branded')

    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self) -> str:
        return self.title
    
class VechilePart(models.Model):

    name = models.CharField(max_length=100, default=None)

    brand = models.CharField(max_length=250, default='un-branded')

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=5, decimal_places=2)

    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = 'vechile_parts'

    def __str__(self) -> str:
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