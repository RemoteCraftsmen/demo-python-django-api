"""
Tests for creating users
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Faker

from to_do.models.todo import Todo

faker = Faker()


class CreateUserTest(TestCase):
    """
        POST /api/users
    """
    def setUp(self):
        self.client = APIClient()
        self.user_list_url = reverse('user-list')

        self.user_1_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }

        self.user_1 = get_user_model().objects.create_user(**self.user_1_data)

        self.admin_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }
        self.admin = get_user_model().objects.create_user(**self.admin_data)
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name=faker.pystr_format(), owner=self.admin)

    def test_admin_can_create_users(self):
        """" Returns Created(201) creating user  as admin """
        self.client.force_login(self.admin)

        payload_new_user_data = {
            'email': faker.ascii_safe_email(),
            'password': self.user_1_data['password']}

        response = self.client.post(self.user_list_url, payload_new_user_data)
        data = response.data

        self.assertEqual(data['email'], payload_new_user_data['email'])
        self.assertEqual(201, response.status_code)

        self.client.logout()

    def test_empty_data(self):
        """" Returns Bad Request(400) sending no data  as admin """
        self.client.force_login(self.admin)

        response = self.client.post(self.user_list_url)

        self.assertEqual(400, response.status_code)

        self.client.logout()

    def test_user_can_not_create_other_users(self):
        """" Returns FORBIDDEN(403) creating user as user """
        self.client.force_login(self.user_1)

        payload_new_user_data = {
            'email': faker.ascii_safe_email(),
            'password': self.user_1_data['password']
        }

        response = self.client.post(self.user_list_url, payload_new_user_data)
        self.assertEqual(403, response.status_code)

        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.post(self.user_list_url)

        self.assertEqual(403, response.status_code)
