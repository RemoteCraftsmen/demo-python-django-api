from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from faker import Faker

faker = Faker()


class LoginTest(TestCase):
    """
        POST /api/login
    """
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')

        self.email = faker.ascii_safe_email()
        self.password = faker.password(length=12)

        get_user_model().objects.create_user(self.email, self.password)

    def test_valid_data(self):
        """" Returns OK(200) sending valid data """

        payload = {'email': self.email, 'password': self.password}
        response = self.client.post(self.login_url, payload)
        data = response.data

        self.assertNotIn('errors', data)
        self.assertEqual(data['email'], self.email)
        self.assertEqual(200, response.status_code)

    def test_no_data(self):
        """" Returns bad request(400) sending  no data """
        response = self.client.post(self.login_url)
        data = response.data

        self.assertIn('email', data)
        self.assertIn('password', data)
        self.assertEqual(data['email'][0], 'This field is required.')
        self.assertEqual(data['password'][0], 'This field is required.')
        self.assertEqual(400, response.status_code)

    def test_invalid_data(self):
        """" Returns bad request(400) sending invalid email address """
        payload = {'email': "not_valid_email"}
        response = self.client.post(self.login_url, payload)
        data = response.data

        self.assertIn('email', data)
        self.assertIn('password', data)
        self.assertEqual(data['email'][0], 'Enter a valid email address.')
        self.assertEqual(data['password'][0], 'This field is required.')
        self.assertEqual(400, response.status_code)

    def test_wrong_data(self):
        """" Returns Unauthorized(401) sending wrong data """
        payload = {'email': self.email, 'password': 'wrong_password'}
        response = self.client.post(self.login_url, payload)

        self.assertEqual(401, response.status_code)
