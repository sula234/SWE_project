# Generated by Django 4.2.7 on 2023-11-28 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_fuelreport_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fuelreport',
            name='user',
        ),
        migrations.RemoveField(
            model_name='route',
            name='origin',
        ),
        migrations.AddField(
            model_name='fuelreport',
            name='fuel_preson',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.fuelpreson'),
        ),
    ]