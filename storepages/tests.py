from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import *

class HomePageTest(SimpleTestCase):


    def setUp(self):
        self.url_reverse = reverse('home')
        self.response = self.client.get(reverse('home'))


    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_template(self):
        self.assertTemplateUsed(self.response, 'storepages/home.html')


    def test_url_resolves(self):
        view = resolve(self.url_reverse)
        self.assertEqual(view.func.__name__, HomeView.as_view().__name__)
