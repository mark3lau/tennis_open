from django.contrib import admin
from .models import Package, Lesson


class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image',
        'description',
        'price',
    )

    # ordering = ('',)


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Package, PackageAdmin)