from django.contrib import admin
from .models import Package, Lesson
from comments.models import Comment
from contact_form.models import Contact


class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'price',
    )


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Comment)
admin.site.register(Contact)
