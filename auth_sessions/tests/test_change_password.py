from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


class UpdateToDoTest(TestCase):
    """
        PUT /api/auth/change-password
    """
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.change_password_url = reverse('change_password')

        self.userData = {
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user = get_user_model().objects.create_user(self.userData['email'],
                                                         self.userData['password'])

    def test_user_can_change_password(self):
        """" Returns Ok(200) sending valid data  as user """
        payload_user = {
            'email': self.userData['email'],
            'password': self.userData['password']
        }

        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_password = {
            'password': '$new_password123',
            'password_confirm': "$new_password123",
            'old_password': self.userData['password']}

        response = self.client.put(self.change_password_url, payload_new_password)
        self.assertEqual(200, response.status_code)

        payload_user = {
            'email': self.userData['email'],
            'password': self.userData['password']
        }

        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(401, response.status_code)

        payload_user['password'] = payload_new_password['password']
        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(200, response.status_code)

    def test_invalid_data(self):
        """" Returns Ok(400) sending invalid data  as user """
        payload_user = {
            'email': self.userData['email'],
            'password': self.userData['password']
        }

        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_password = {
            'password': '$new_password123',
            'password_confirm': "$qwerty123456789",
            'old_password': self.userData['password']}

        response = self.client.put(self.change_password_url, payload_new_password)
        self.assertEqual(400, response.status_code)
        data = response.data

        self.assertEqual(data['password'][0], "Password fields didn't match.")

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.put(self.change_password_url)

        self.assertEqual(403, response.status_code)
