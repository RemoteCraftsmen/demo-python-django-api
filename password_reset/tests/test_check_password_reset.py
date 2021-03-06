"""
Test for reseting password by token
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from faker import Faker

from password_reset.services.password_reset_token_generator_handler import (
    PasswordResetTokenGeneratorHandler,
)
from password_reset.services.date_service import DateService

faker = Faker()


class TestCheckPasswordReset(TestCase):
    """
    POST /api/todos
    """

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")

        self.user_1_data = {
            "email": faker.ascii_safe_email(),
            "password": faker.password(length=12),
        }

        self.user_1 = get_user_model().objects.create_user(**self.user_1_data)

    def test_admin_can_create_users(self):
        """ " Returns Created(201) creating user  as admin"""
        user = get_user_model().objects.filter(email=self.user_1_data["email"]).first()
        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.tomorrow()
        user.save()

        password = faker.pystr_format()

        payload_user = {"password": password, "password_confirm": password}

        response = self.client.post(
            reverse("password_reset_token", args=[user.passwordResetToken]),
            payload_user,
        )

        self.assertEqual(200, response.status_code)

        user = get_user_model().objects.filter(email=self.user_1_data["email"]).first()
        self.assertIsNone(user.passwordResetToken)
        self.assertIsNone(user.passwordResetTokenExpiresAt)
        self.assertTrue(user.is_password_reset_token_expired())

        payload = {"email": self.user_1_data["email"], "password": password}
        response = self.client.post(self.login_url, payload)
        self.assertEqual(200, response.status_code)

    def test_old_token(self):
        """ " Returns Created(201) creating user  as admin"""
        user = get_user_model().objects.filter(email=self.user_1_data["email"]).first()
        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.yesterday()
        user.save()
        self.assertTrue(user.is_password_reset_token_expired())

        password = faker.pystr_format()

        payload_user = {"password": password, "password_confirm": password}

        response = self.client.post(
            reverse("password_reset_token", args=[user.passwordResetToken]),
            payload_user,
        )
        self.assertEqual(204, response.status_code)

        payload = {"email": self.user_1_data["email"], "password": password}
        response = self.client.post(self.login_url, payload)
        self.assertEqual(401, response.status_code)

    def test_no_data(self):
        """ " Returns Forbidden(403) as not logged in"""
        user = get_user_model().objects.filter(email=self.user_1_data["email"]).first()
        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.tomorrow()
        user.save()

        response = self.client.post(
            reverse("password_reset_token", args=[user.passwordResetToken])
        )
        data = response.data

        self.assertEqual("This field is required.", data["password"][0])
        self.assertEqual("This field is required.", data["password_confirm"][0])

        self.assertEqual(400, response.status_code)

    def test_wrong_data(self):
        """ " Returns Forbidden(403) as not logged in"""
        user = get_user_model().objects.filter(email=self.user_1_data["email"]).first()
        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.tomorrow()
        user.save()

        password = faker.pystr_format()

        payload = {"password": password, "password_confirm": password + password}

        response = self.client.post(
            reverse("password_reset_token", args=[user.passwordResetToken]), payload
        )
        data = response.data

        self.assertEqual("Password fields didn't match.", data["password"][0])

        self.assertEqual(400, response.status_code)
