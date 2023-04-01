from django.contrib import admin
from .models import Package, Lesson


admin.site.register(Lesson)
admin.site.register(Package)