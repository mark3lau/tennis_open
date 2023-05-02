from django.urls import path
from . import views

urlpatterns = [
    path('', views.comment_list, name='comment_list'),
    path('create/', views.comment_create, name='comment_create'),
    path('<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
