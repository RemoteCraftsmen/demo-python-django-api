from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from faker import Faker

faker = Faker()


class ChangeProfileTest(TestCase):
    """
        PUT /api/auth/change-profile
    """
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.change_profile_url = reverse('change_profile')

        self.user_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.password(length=12)
        }

        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_user_can_change_profile(self):
        """" Returns Ok(200) sending valid data  as user """
        self.client.force_login(self.user)

        payload_new_user_data = {
            'email': faker.ascii_safe_email(),
            'last_name': faker.first_name(),
            'first_name': faker.last_name(),
            'password_confirm': self.user_data['password']}

        response = self.client.put(self.change_profile_url, payload_new_user_data)
        data = response.data

        self.assertEqual(data['email'], payload_new_user_data['email'])
        self.assertEqual(data['last_name'], payload_new_user_data['last_name'])
        self.assertEqual(data['first_name'], payload_new_user_data['first_name'])
        self.assertEqual(200, response.status_code)
        self.client.logout()

    def test_invalid_data(self):
        """" Returns Ok(400) sending invalid data  as user """
        self.client.force_login(self.user)

        payload_new_user_data = {
            'email': 'not_A_Mail',
            'last_name': '',
            'first_name': '',
            'password_confirm': self.user_data['password']}

        response = self.client.put(self.change_profile_url, payload_new_user_data)
        self.assertEqual(400, response.status_code)
        data = response.data

        self.assertEqual(data['email'][0], "Enter a valid email address.")
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.put(self.change_profile_url)

        self.assertEqual(403, response.status_code)
