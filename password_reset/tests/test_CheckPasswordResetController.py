from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from password_reset.services.PasswordResetTokenGeneratorHandler import PasswordResetTokenGeneratorHandler
from password_reset.services.DateService import DateService
from django.urls import reverse


class TestCheckPasswordResetController(TestCase):
    """
        POST /api/todos
    """
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')

        self.user1Data = {
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user_1 = get_user_model().objects.create_user(self.user1Data['email'],
                                                           self.user1Data['password'])

    def test_admin_can_create_users(self):
        """" Returns Created(201) creating user  as admin """
        user = get_user_model().objects.filter(email=self.user1Data['email']).first()
        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.tomorrow()
        user.save()

        password = 'M4Y7Tp`Xb4#d~'

        payload_user = {
            'password': password,
            'password_confirm': password
        }

        response = self.client.post(reverse('password_reset_token', args=[user.passwordResetToken]), payload_user)

        self.assertEqual(200, response.status_code)

        user = get_user_model().objects.filter(email=self.user1Data['email']).first()
        self.assertIsNone(user.passwordResetToken)
        self.assertIsNone(user.passwordResetTokenExpiresAt)
        self.assertTrue(user.is_password_reset_token_expired())

        payload = {'email': self.user1Data['email'], 'password': password}
        response = self.client.post(self.login_url, payload)
        self.assertEqual(200, response.status_code)

    def test_old_token(self):
        """" Returns Created(201) creating user  as admin """
        user = get_user_model().objects.filter(email=self.user1Data['email']).first()
        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.yesterday()
        user.save()
        self.assertTrue(user.is_password_reset_token_expired())

        password = 'M4Y7Tp`Xb4#d~'

        payload_user = {
            'password': password,
            'password_confirm': password
        }

        response = self.client.post(reverse('password_reset_token', args=[user.passwordResetToken])
                                    , payload_user)
        self.assertEqual(204, response.status_code)

        payload = {'email': self.user1Data['email'], 'password': password}
        response = self.client.post(self.login_url, payload)
        self.assertEqual(401, response.status_code)

    def test_no_data(self):
        """" Returns Forbidden(403) as not logged in """
        user = get_user_model().objects.filter(email=self.user1Data['email']).first()
        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.tomorrow()
        user.save()

        response = self.client.post(reverse('password_reset_token', args=[user.passwordResetToken]))
        data = response.data

        self.assertEqual("This field is required.", data['password'][0])
        self.assertEqual("This field is required.", data['password_confirm'][0])

        self.assertEqual(400, response.status_code)

    def test_wrong_data(self):
        """" Returns Forbidden(403) as not logged in """
        user = get_user_model().objects.filter(email=self.user1Data['email']).first()
        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.tomorrow()
        user.save()

        password = 'M4Y7Tp`Xb4#d~'

        payload = {
            'password': password,
            'password_confirm': password+password
        }

        response = self.client.post(reverse('password_reset_token', args=[user.passwordResetToken])
                                    , payload)
        data = response.data

        self.assertEqual("Password fields didn't match.", data['password'][0])

        self.assertEqual(400, response.status_code)
