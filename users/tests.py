from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTests(TestCase):

    def test_user_create(self):
        new_user = get_user_model().objects.create(username='Test', email='test@gmail.com', password='testpassword')
        self.assertEqual(new_user.username, 'Test')
        self.assertEqual(new_user.email, 'test@gmail.com')
        self.assertTrue(new_user.is_active)