from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Factory
faker = Factory.create()


class RequestPasswordReset(TestCase):
    """
        POST /api/todos
    """
    def setUp(self):
        self.client = APIClient()
        self.password_reset_url = reverse('password_reset')

        self.user1Data = {
            'email': faker.ascii_safe_email(),
            'password': faker.password(length=12)
        }

        self.user_1 = get_user_model().objects.create_user(**self.user1Data)

    def test_initial_data(self):
        user = get_user_model().objects.filter(email=self.user1Data['email']).first()

        self.assertIsNone(user.passwordResetToken)
        self.assertIsNone(user.passwordResetTokenExpiresAt)
        self.assertTrue(user.is_password_reset_token_expired())

    def test_admin_can_create_users(self):
        """" Returns Created(201) creating user  as admin """
        payload_user = {
            'email': self.user1Data['email'],
        }

        response = self.client.post(self.password_reset_url, payload_user)

        user = get_user_model().objects.filter(email=self.user1Data['email']).first()

        self.assertIsNotNone(user.passwordResetToken)
        self.assertIsNotNone(user.passwordResetTokenExpiresAt)
        self.assertFalse(user.is_password_reset_token_expired())

        self.assertEqual(200, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        payload_user = {
            'email': faker.ascii_safe_email(),
        }

        response = self.client.post(self.password_reset_url, payload_user)

        self.assertEqual(200, response.status_code)

    def test_no_data(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.post(self.password_reset_url)

        self.assertEqual(400, response.status_code)

    def test_wrong_data(self):
        """" Returns Forbidden(403) as not logged in """
        payload_user = {
            'email': 'not_a_email',
        }

        response = self.client.post(self.password_reset_url, payload_user)

        self.assertEqual(400, response.status_code)
