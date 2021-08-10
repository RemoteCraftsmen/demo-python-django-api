from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class LoginTest(TestCase):
    """
        POST /api/login
    """
    def setUp(self):
        self.client = APIClient()
        self.email = 'test_user@example.com'
        self.password = 'testing_password_123'
        get_user_model().objects.create_user(self.email, self.password)

    def test_valid_data(self):
        """" Returns OK(200) sending valid data """
        payload = {'email': self.email, 'password': self.password}
        response = self.client.post('/api/auth/login', payload)
        data = response.data

        self.assertNotIn('errors', data)
        self.assertEqual(data['email'], self.email)
        self.assertEqual(200, response.status_code)

    def test_no_data(self):
        """" Returns bad request(400) sending  no data """
        response = self.client.post('/api/auth/login')
        data = response.data

        self.assertIn('email', data)
        self.assertIn('password', data)
        self.assertEqual(data['email'][0], 'This field is required.')
        self.assertEqual(data['password'][0], 'This field is required.')
        self.assertEqual(400, response.status_code)

    def test_invalid_data(self):
        """" Returns bad request(400) sending invalid email address """
        payload = {'email': "not_valid_email"}
        response = self.client.post('/api/auth/login', payload)
        data = response.data

        self.assertIn('email', data)
        self.assertIn('password', data)
        self.assertEqual(data['email'][0], 'Enter a valid email address.')
        self.assertEqual(data['password'][0], 'This field is required.')
        self.assertEqual(400, response.status_code)

    def test_wrong_data(self):
        """" Returns Unauthorized(401) sending wrong data """
        payload = {'email': self.email, 'password': 'wrong_password'}
        response = self.client.post('/api/auth/login', payload)

        self.assertEqual(401, response.status_code)
