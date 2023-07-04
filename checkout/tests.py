from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import Country
from .models import Order, OrderLineItem
from tennis_lessons.models import Package
from profiles.models import UserProfile


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


# Test cases for Models
class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, default_phone_number='123456789',
                                                       default_country=Country('US'), default_town_or_city='Test City',
                                                       default_street_address1='Test Street 1')
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='John Doe',
            email='johndoe@example.com',
            phone_number='987654321',
            country=Country('GB'),
            postcode='SW1A 1AA',
            town_or_city='London',
            street_address1='123 Test Street',
            street_address2='Unit 45',
            county='Test County',
            order_total=100,
            original_bag='Test bag content',
            stripe_pid='ch_1234567890',
        )

    def test_order_model_str(self):
        self.assertEqual(str(self.order), self.order.order_number)

    def test_order_model_generate_order_number(self):
        order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='123456789',
            country=Country('US'),
            town_or_city='Test City',
            street_address1='Test Street 1',
        )
        self.assertIsNotNone(order.order_number)

    def test_order_model_update_total(self):
        package = Package.objects.create(name='Test Package', price=50)
        order_line_item = OrderLineItem.objects.create(order=self.order, package=package)
        self.order.update_total()
        self.assertEqual(self.order.order_total, 50)

    def test_order_model_save_method(self):
        order = Order(
            user_profile=self.user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='123456789',
            country=Country('US'),
            town_or_city='Test City',
            street_address1='Test Street 1',
        )
        order.save()
        self.assertIsNotNone(order.order_number)


class OrderLineItemModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, default_phone_number='123456789',
                                                       default_country=Country('US'), default_town_or_city='Test City',
                                                       default_street_address1='Test Street 1')
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='John Doe',
            email='johndoe@example.com',
            phone_number='987654321',
            country=Country('GB'),
            postcode='SW1A 1AA',
            town_or_city='London',
            street_address1='123 Test Street',
            street_address2='Unit 45',
            county='Test County',
            order_total=100,
            original_bag='Test bag content',
            stripe_pid='ch_1234567890',
        )
        self.package = Package.objects.create(name='Test Package', price=50)
        self.order_line_item = OrderLineItem.objects.create(order=self.order, package=self.package)

    def test_order_line_item_model_save_method(self):
        self.assertEqual(self.order_line_item.lineitem_total, 50)
