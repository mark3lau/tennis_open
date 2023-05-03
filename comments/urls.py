from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.comments, name='comments'),
    path('post/', views.post_comment, name='post_comment'),
    path('<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]
