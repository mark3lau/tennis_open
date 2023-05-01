from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_packages, name='packages'),
    path('add/', views.add_package, name='add_package'),
]
