from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Comment
from .forms import CommentForm


# Test cases for Models
class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.comment = Comment.objects.create(user=self.user, message='Test comment')

    def test_comment_model_str(self):
        self.assertEqual(str(self.comment), f'Comment by {self.user.username} on {self.comment.created_at}')

    def test_comment_model_fields(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.message, 'Test comment')

    def test_comment_model_created_at_auto_now_add(self):
        old_created_at = self.comment.created_at
        self.comment.save()
        self.assertEqual(self.comment.created_at, old_created_at)

    def test_comment_model_updated_at_auto_now(self):
        old_updated_at = self.comment.updated_at
        self.comment.save()
        self.assertNotEqual(self.comment.updated_at, old_updated_at)


# Test cases for Views
class CommentViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.comment = Comment.objects.create(user=self.user, message='Test comment')

    def test_post_comment(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        url = reverse('post_comment')
        response = self.client.post(url, {'message': 'New comment'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('comments'))
        self.assertEqual(Comment.objects.count(), 2)

    def test_edit_comment(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        url = reverse('edit_comment', args=[self.comment.pk])
        response = self.client.post(url, {'message': 'Updated comment'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('comments'))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.message, 'Updated comment')

    def test_comments(self):
        url = reverse('comments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments.html')
        self.assertContains(response, 'Test comment')

    def test_edit_comment_class_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        url = reverse('edit_comment_class', args=[self.comment.pk])
        response = self.client.post(url, {'message': 'Updated comment'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('comments'))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.message, 'Updated comment')

    def test_delete_comment_class_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        url = reverse('delete_comment_class', args=[self.comment.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('comments'))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())
