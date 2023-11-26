# 5th

from django.contrib import admin

from .models import (
    report, Image, VechilePart
)

admin.site.register(report)
admin.site.register(Image)
admin.site.register(VechilePart)
