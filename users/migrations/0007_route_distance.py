# Generated by Django 4.2.7 on 2023-11-26 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_fuelreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='distance',
            field=models.IntegerField(default=0),
        ),
    ]
