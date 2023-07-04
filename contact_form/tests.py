from django.test import TestCase, RequestFactory
from django.urls import reverse
from .views import contact, contact_success
from .forms import ContactForm
from .models import Contact


# Test cases for Forms

from django.test import TestCase
from .forms import ContactForm


class ContactFormTestCase(TestCase):
    def test_contact_form_valid_data(self):
        form = ContactForm(data={
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '1234567890',
            'message': 'Test message'
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_missing_required_fields(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        self.assertTrue('name' in form.errors)
        self.assertTrue('email' in form.errors)
        self.assertTrue('phone' in form.errors)
        self.assertTrue('message' in form.errors)


# Test cases for Models
class ContactModelTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            phone='1234567890',
            message='Test message'
        )

    def test_contact_model_creation(self):
        self.assertEqual(self.contact.name, 'John Doe')
        self.assertEqual(self.contact.email, 'johndoe@example.com')
        self.assertEqual(self.contact.phone, '1234567890')
        self.assertEqual(self.contact.message, 'Test message')

    def test_contact_model_str_representation(self):
        self.assertEqual(str(self.contact), 'John Doe')


# Test cases for Views
class ContactViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_contact_view_get(self):
        url = reverse('contact')
        request = self.factory.get(url)
        response = contact(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_view_post_valid_form(self):
        url = reverse('contact')
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'Test message'
        }
        request = self.factory.post(url, data=data)
        response = contact(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contact_success'))

    def test_contact_view_post_invalid_form(self):
        url = reverse('contact')
        data = {
            'name': '',
            'email': 'johndoe@example.com',
            'message': 'Test message'
        }
        request = self.factory.post(url, data=data)
        response = contact(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertTrue(response.context['form'].errors)

    def test_contact_success_view(self):
        url = reverse('contact_success')
        request = self.factory.get(url)
        response = contact_success(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_success.html')
