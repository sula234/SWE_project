# Generated by Django 4.2.7 on 2023-11-26 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='title',
            new_name='full_name',
        ),
        migrations.RenameField(
            model_name='vechilepart',
            old_name='size',
            new_name='name',
        ),
    ]
