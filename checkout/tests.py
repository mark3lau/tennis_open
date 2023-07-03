from django.test import TestCase, Client
from django.urls import reverse


# Test cases for Models



# Test cases for Views

class CheckoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cache_checkout_data(self):
        url = reverse('cache_checkout_data')
        response = self.client.post(url, {
            'client_secret': 'test_client_secret',
            'save_info': True,
            'username': 'test_user',
        })
        self.assertEqual(response.status_code, 200)
        # Assert any specific behavior you expect from the view, such as modified PaymentIntent metadata.

    def test_checkout_successful(self):
        url = reverse('checkout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert that the page loads successfully and necessary context variables are present.

        response = self.client.post(url, {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'country': 'Test Country',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': 'Test Street 1',
            'street_address2': 'Test Street 2',
            'county': 'Test County',
            'client_secret': 'test_client_secret',
        })
        self.assertEqual(response.status_code, 302)
        # Assert that the user is redirected to the checkout_success view.


def test_checkout_unsuccessful(self):
    url = reverse('checkout')
    response = self.client.post(url, {
        'full_name': '',  # Invalid: Empty value for required field.
        'email': 'test@example.com',
        'phone_number': '1234567890',
        'country': 'Test Country',
        'postcode': '12345',
        'town_or_city': 'Test City',
        'street_address1': 'Test Street 1',
        'street_address2': 'Test Street 2',
        'county': 'Test County',
        'client_secret': 'test_client_secret',
    })
    self.assertEqual(response.status_code, 200)
    self.assertFormError(response, 'order_form', 'full_name', 'This field is required.')
    # Assert that the user is shown an error message for the 'full_name' field.

    # Test for scenarios where the form data is not provided at all.
    
    response = self.client.post(url, {})
    self.assertEqual(response.status_code, 200)
    self.assertFormError(response, 'order_form', 'full_name', 'This field is required.')
    # Assert that the user is shown an error message for the 'full_name' field when no data is provided.


    def test_checkout_success(self):
        order_number = 'test_order_number'
        url = reverse('checkout_success', args=[order_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert that the checkout success page loads successfully and necessary context variables are present.

