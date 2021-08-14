from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


class UpdateToDoTest(TestCase):
    """
        GET /api/auth/profile
    """
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.show_profile_url = reverse('show_profile')

        self.userData = {
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user = get_user_model().objects.create_user(self.userData['email'],
                                                         self.userData['password'])

    def test_user_can_see_its_profile(self):
        """" Returns Ok(200) sending valid data  as user """
        payload_user = {
            'email': self.userData['email'],
            'password': self.userData['password']
        }

        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.show_profile_url)
        data = response.data

        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(200, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get(self.show_profile_url)

        self.assertEqual(403, response.status_code)
