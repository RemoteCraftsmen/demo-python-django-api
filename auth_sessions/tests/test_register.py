from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from faker import Faker

faker = Faker()


class RegisterTest(TestCase):
    """
        POST /api/register
    """
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_valid_data(self):
        """" Returns OK(200) sending valid data """
        email = faker.ascii_safe_email()
        password = faker.password(length=12)
        password_confirm = password

        payload = {'email': email, 'password': password, 'password_confirm': password_confirm}
        response = self.client.post(self.register_url, payload)
        data = response.data

        self.assertNotIn('errors', data)
        self.assertEqual(data['email'], email)
        self.assertEqual(200, response.status_code)

        user_to_check = get_user_model().objects.filter(email=email).first()
        self.assertIsNotNone(user_to_check)
        self.assertTrue(user_to_check.check_password(password))

    def test_no_data(self):
        """" Returns bad request(400) sending  no data """
        response = self.client.post(self.register_url)
        data = response.data

        self.assertIn('email', data)
        self.assertIn('password', data)
        self.assertIn('password_confirm', data)

        self.assertEqual(data['email'][0], 'This field is required.')
        self.assertEqual(data['password_confirm'][0], 'This field is required.')
        self.assertEqual(data['password'][0], 'This field is required.')
        self.assertEqual(400, response.status_code)

    def test_invalid_data(self):
        """" Returns bad request(400) sending invalid email address """
        payload = {'email': "not_valid_email"}
        response = self.client.post(self.register_url, payload)
        data = response.data

        self.assertIn('email', data)
        self.assertEqual(data['email'][0], 'Enter a valid email address.')
        self.assertEqual(400, response.status_code)
