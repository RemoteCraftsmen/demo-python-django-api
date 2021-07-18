from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class RegisterTest(TestCase):
    """
        /api/register
    """
    def setUp(self):
        self.client = APIClient()

    def test_valid_data(self):
        """" Returns OK(200) sending valid data """
        email = 'new_test_user@example.com'
        password = 'new_password'
        password_confirm = 'new_password'
        username = 'new_user'

        payload = {'email': email, 'password': password, 'password_confirm': password_confirm, 'username': username}
        response = self.client.post('/api/register', payload)
        data = response.data

        self.assertNotIn('errors', data)
        self.assertEqual(data['username'], username)
        self.assertEqual(data['email'], email)
        self.assertEqual(200, response.status_code)

        user_to_check = User.objects.filter(email=email, username=username).first()
        self.assertIsNotNone(user_to_check)
        self.assertTrue(user_to_check.check_password(password))

    def test_no_data(self):
        """" Returns bad request(400) sending  no data """
        response = self.client.post('/api/register')
        data = response.data

        self.assertIn('errors', data)
        errors = data['errors']
        self.assertIn('email', errors)
        self.assertIn('password', errors)
        self.assertIn('username', errors)
        self.assertIn('password_confirm', errors)

        self.assertEqual(errors['username'][0], 'This field is required.')
        self.assertEqual(errors['email'][0], 'This field is required.')
        self.assertEqual(errors['password_confirm'][0], 'This field is required.')
        self.assertEqual(errors['password'][0], 'This field is required.')
        self.assertEqual(400, response.status_code)

    def test_invalid_data(self):
        """" Returns bad request(400) sending invalid email address """
        payload = {'email': "not_valid_email"}
        response = self.client.post('/api/register', payload)
        data = response.data

        self.assertIn('errors', data)
        errors = data['errors']
        self.assertIn('email', errors)
        self.assertEqual(errors['email'][0], 'Enter a valid email address.')
        self.assertEqual(400, response.status_code)
