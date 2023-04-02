from django.urls import path
from . import views

urlpatterns = [
    path('', views.tennis_fitness_packages, name='packages'),
]
