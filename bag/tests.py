from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from tennis_lessons.models import Package


class BagViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.package = Package.objects.create(name='Test Package', price=10)

    def test_add_to_bag(self):
        response = self.client.get(reverse('add_to_bag', args=[self.package.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after adding to bag
        self.assertEqual(len(get_messages(response.wsgi_request)), 1)  # Check success message
        self.assertIn(f'Added {self.package.name} to your bag', str(get_messages(response.wsgi_request)))

    def test_view_bag(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)  # Successful response

    def test_remove_from_bag(self):
        # Add the package to the bag first
        self.client.get(reverse('add_to_bag', args=[self.package.id]))
        response = self.client.get(reverse('remove_from_bag', args=[self.package.id]))
        self.assertEqual(response.status_code, 200)  # Successful response
        self.assertEqual(len(get_messages(response.wsgi_request)), 1)  # Check success message
        self.assertIn(f'Removed {self.package.name} from your bag', str(get_messages(response.wsgi_request)))