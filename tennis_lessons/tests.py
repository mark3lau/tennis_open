from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Package


# Test cases for Models

from django.test import TestCase
from tennis_lessons.models import Lesson, Package


class LessonModelTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(name='Tennis Lesson', friendly_name='Friendly Tennis Lesson')

    def test_lesson_model_str(self):
        self.assertEqual(str(self.lesson), 'Tennis Lesson')

    def test_lesson_model_get_friendly_name(self):
        self.assertEqual(self.lesson.get_friendly_name(), 'Friendly Tennis Lesson')


class PackageModelTestCase(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(name='Tennis Lesson')
        self.package = Package.objects.create(
            lesson=self.lesson,
            name='Package 1',
            description='Package 1 description',
            detail_1='Detail 1',
            detail_2='Detail 2',
            detail_3='Detail 3',
            detail_4='Detail 4',
            price=100
        )

    def test_package_model_str(self):
        self.assertEqual(str(self.package), 'Package 1')



# Test cases for Views

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


# Test cases for forms


from django.test import TestCase
from tennis_lessons.models import Lesson, Package
from tennis_lessons.forms import PackageForm


class PackageFormTestCase(TestCase):
    def setUp(self):
        self.lesson1 = Lesson.objects.create(name='Tennis Lesson 1', friendly_name='Friendly Tennis Lesson 1')
        self.lesson2 = Lesson.objects.create(name='Tennis Lesson 2', friendly_name='Friendly Tennis Lesson 2')

    def test_package_form_fields(self):
        form = PackageForm()
        expected_fields = ['lesson', 'name', 'description', 'detail_1', 'detail_2', 'detail_3', 'detail_4', 'price']
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_package_form_lesson_choices(self):
        form = PackageForm()
        expected_choices = [(self.lesson1.id, 'Friendly Tennis Lesson 1'), (self.lesson2.id, 'Friendly Tennis Lesson 2')]
        self.assertEqual(form.fields['lesson'].choices, expected_choices)

    def test_package_form_widget_classes(self):
        form = PackageForm()
        expected_widget_classes = 'border-black rounded-0'
        for field_name, field in form.fields.items():
            self.assertEqual(field.widget.attrs.get('class', ''), expected_widget_classes)
