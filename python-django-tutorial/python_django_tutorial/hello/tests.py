from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class TestHelloViews(TestCase):
    def test_get_homepage(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)