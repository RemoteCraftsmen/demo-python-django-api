from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


class UpdateToDoTest(TestCase):
    """
        PUT /api/auth/change-profile
    """
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.change_profile_url = reverse('change_profile')

        self.userData = {
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user = get_user_model().objects.create_user(self.userData['email'],
                                                         self.userData['password'])

    def test_user_can_change_profile(self):
        """" Returns Ok(200) sending valid data  as user """
        payload_user = {
            'email': self.userData['email'],
            'password': self.userData['password']
        }

        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_user_data = {
            'email': 'newuser@example.com',
            'last_name': 'John',
            'first_name': 'Example',
            'password_confirm': self.userData['password']}

        response = self.client.put(self.change_profile_url, payload_new_user_data)
        data = response.data

        self.assertEqual(data['email'], payload_new_user_data['email'])
        self.assertEqual(data['last_name'], payload_new_user_data['last_name'])
        self.assertEqual(data['first_name'], payload_new_user_data['first_name'])
        self.assertEqual(200, response.status_code)

    def test_invalid_data(self):
        """" Returns Ok(400) sending invalid data  as user """
        payload_user = {
            'email': self.userData['email'],
            'password': self.userData['password']
        }

        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_user_data = {
            'email': 'not_A_Mail',
            'last_name': '',
            'first_name': '',
            'password_confirm': self.userData['password']}

        response = self.client.put(self.change_profile_url, payload_new_user_data)
        self.assertEqual(400, response.status_code)
        data = response.data

        self.assertEqual(data['email'][0], "Enter a valid email address.")

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.put(self.change_profile_url)

        self.assertEqual(403, response.status_code)
