from django.urls import path
from . import views


urlpatterns = [
    path('comments/', views.comments, name='comments'),
    path('comments/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:pk>/delete/', views.DeleteComment, name='delete_comment'),
    path('comments/post/', views.post_comment, name='post_comment'),
]