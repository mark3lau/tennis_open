from django.db import models


class Lesson(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Package(models.Model):
    lesson = models.ForeignKey('Lesson', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    description = models.TextField()
    detail_1 = models.TextField(blank=True)
    detail_2 = models.TextField(blank=True)
    detail_3 = models.TextField(blank=True)
    detail_4 = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0,
                                default=0, blank=False)

    def __str__(self):
        return self.name
