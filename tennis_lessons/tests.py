from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Package


class AllPackagesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.package = Package.objects.create(name='Test Package')

    def test_all_packages_get(self):
        response = self.client.get(reverse('all_packages'))
        self.assertEqual(response.status_code, 200)  # Successful response
        # Check if the packages are present in the context
        self.assertQuerysetEqual(response.context['packages'], [repr(self.package)])

    def test_all_packages_post_with_package_id(self):
        response = self.client.post(reverse('all_packages'), {
            'package_id': self.package.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after adding to bag
        self.assertEqual(len(get_messages(response.wsgi_request)), 1)  # Check success message
        self.assertIn(f'Added {self.package.name} to your bag', str(get_messages(response.wsgi_request)))
        # Check if the package is added to the bag in the session
        self.assertIn(str(self.package.id), self.client.session['bag'])

    def test_all_packages_post_without_package_id(self):
        response = self.client.post(reverse('all_packages'))
        self.assertEqual(response.status_code, 200)  # Successful response
        # Check if the packages are present in the context
        self.assertQuerysetEqual(response.context['packages'], [repr(self.package)])
