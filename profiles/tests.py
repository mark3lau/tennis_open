from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from .models import UserProfile
from .views import profile, order_history
from tennis_lessons.models import Order
from django_countries import countries
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from profiles.forms import UserProfileForm


# Test cases for Models


class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.user, self.user)

    def test_user_profile_str(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), self.user.username)

    def test_user_profile_default_fields(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertIsNone(profile.default_phone_number)
        self.assertIsNone(profile.default_street_address1)
        self.assertIsNone(profile.default_street_address2)
        self.assertIsNone(profile.default_town_or_city)
        self.assertIsNone(profile.default_county)
        self.assertIsNone(profile.default_postcode)
        self.assertIsNone(profile.default_country)

    def test_user_profile_default_country_choices(self):
        profile = UserProfile.objects.create(user=self.user)
        country_field = profile._meta.get_field('default_country')
        self.assertEqual(country_field.choices, countries)

    def test_create_or_update_user_profile_signal_create(self):
        user = User.objects.create_user(username='newuser', password='newpassword')
        self.assertRaises(ObjectDoesNotExist, UserProfile.objects.get, user=user)

    def test_create_or_update_user_profile_signal_update(self):
        user = User.objects.create_user(username='existinguser', password='existingpassword')
        profile = UserProfile.objects.create(user=user)
        user.username = 'updateduser'
        post_save.send(sender=User, instance=user, created=False)
        updated_profile = UserProfile.objects.get(user=user)
        self.assertEqual(updated_profile.user, user)


# Test cases for Views

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = UserProfile.objects.create(user=self.user)

    def test_profile_view_get(self):
        request = self.factory.get(reverse('profile'))
        request.user = self.user

        response = profile(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertTrue('form' in response.context)
        self.assertTrue('orders' in response.context)
        self.assertEqual(response.context['form'].instance, self.profile)

    def test_profile_view_post_valid_form(self):
        request = self.factory.post(reverse('profile'), data={
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            # Include other form fields as necessary
        })
        request.user = self.user

        response = profile(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertTrue('form' in response.context)
        self.assertTrue('orders' in response.context)
        self.assertEqual(response.context['form'].instance, self.profile)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile updated successfully')

    def test_profile_view_post_invalid_form(self):
        request = self.factory.post(reverse('profile'), data={
            'full_name': 'John Doe',
            # Include other form fields as necessary
        })
        request.user = self.user

        response = profile(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertTrue('form' in response.context)
        self.assertTrue('orders' in response.context)
        self.assertEqual(response.context['form'].instance, self.profile)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Update failed. Please ensure the form is valid.')


class OrderHistoryViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(order_number='12345')  # Add necessary fields for the order

    def test_order_history_view(self):
        request = self.factory.get(reverse('order_history', args=['12345']))
        request.user = self.user

        response = order_history(request, '12345')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertTrue('order' in response.context)
        self.assertTrue('from_profile' in response.context)
        self.assertEqual(response.context['order'], self.order)
        self.assertTrue(response.context['from_profile'])

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'This is a past confirmation for order number 12345. A confirmation email was sent on the order date.'
        )


# Test cases for forms


class UserProfileFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_profile_form_fields(self):
        form = UserProfileForm()
        expected_fields = [
            'default_postcode',
            'default_town_or_city',
            'default_street_address1',
            'default_phone_number',
            'default_street_address2',
            'default_county',
        ]
        form_fields = list(form.fields.keys())
        self.assertEqual(form_fields, expected_fields)

    def test_user_profile_form_excludes_user_field(self):
        form = UserProfileForm()
        self.assertIn('user', form.Meta.exclude)

    def test_user_profile_form_placeholders(self):
        form = UserProfileForm()
        expected_placeholders = {
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_phone_number': 'Phone Number',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }
        for field, placeholder in expected_placeholders.items():
            self.assertEqual(form.fields[field].widget.attrs.get('placeholder'), placeholder)

    def test_user_profile_form_classes(self):
        form = UserProfileForm()
        expected_classes = 'border-black round-0 profile-form-input'
        for field in form.fields:
            self.assertEqual(form.fields[field].widget.attrs.get('class'), expected_classes)

    def test_user_profile_form_autofocus(self):
        form = UserProfileForm()
        self.assertEqual(form.fields['default_phone_number'].widget.attrs.get('autofocus'), True)

    def test_user_profile_form_labels(self):
        form = UserProfileForm()
        for field in form.fields:
            self.assertFalse(form.fields[field].label)
