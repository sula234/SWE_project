# Generated by Django 4.2.7 on 2023-11-25 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatcher_phone_number', models.CharField(max_length=20)),
            ],
        ),
    ]