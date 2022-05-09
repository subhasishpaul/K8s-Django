from django.test import TestCase

from .models import Circle

class CircleTestCase(TestCase):
    def setUp(self):
        Circle.objects.create(title='Hello World')

    def test_failure(self):
        qs = Circle.objects.all()
        self.assertTrue(qs.exists())