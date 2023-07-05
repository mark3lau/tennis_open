from django.urls import path
from . import views


urlpatterns = [
    path('comments/', views.comments, name='comments'),
    path('comments/<int:pk>/edit/', views.EditComment.as_view(), name='edit_comment'),
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
    path('comments/post/', views.post_comment, name='post_comment'),
]
