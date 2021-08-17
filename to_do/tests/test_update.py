"""
Tests for updating to_do item
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Faker

from to_do.models.todo import Todo

faker = Faker()


class UpdateToDoTest(TestCase):
    """
    PUT /api/todos/:id
    """

    def setUp(self):
        self.client = APIClient()

        self.user_1 = get_user_model().objects.create_user(
            email=faker.ascii_safe_email(), password=faker.password(length=12)
        )

        self.user_1_item = Todo.objects.create(
            name=faker.pystr_format(), owner=self.user_1
        )

        self.user_2 = get_user_model().objects.create_user(
            email=faker.ascii_safe_email(), password=faker.password(length=12)
        )

        self.user_2_item = Todo.objects.create(
            name=faker.pystr_format(), owner=self.user_2
        )

        self.admin = get_user_model().objects.create_user(
            email=faker.ascii_safe_email(), password=faker.password(length=12)
        )
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(
            name=faker.pystr_format(), owner=self.admin
        )

    def test_user_can_update_its_item(self):
        """ " Returns Ok(200) updating to-do item  as admin"""
        self.client.force_login(self.user_1)

        payload_item = {
            "name": faker.pystr_format(),
            "completed": faker.boolean(chance_of_getting_true=50),
        }

        response = self.client.put(
            reverse("todo-detail", args=[self.user_1_item.id]), payload_item
        )
        data = response.data

        self.assertEqual(data["id"], str(self.user_1_item.id))
        self.assertEqual(data["name"], str(payload_item["name"]))
        self.assertEqual(data["owner"]["id"], str(self.user_1.id))
        self.assertEqual(data["completed"], payload_item["completed"])
        self.assertEqual(200, response.status_code)
        self.client.logout()

    def test_admin_can_update_all_item(self):
        """ " Returns Ok(200) updating to-do item  as admin"""
        self.client.force_login(self.admin)

        payload_item = {
            "name": faker.pystr_format(),
            "owner_id": self.user_2.id,
            "completed": faker.boolean(chance_of_getting_true=50),
        }

        response = self.client.put(
            reverse("todo-detail", args=[self.user_1_item.id]), payload_item
        )
        data = response.data

        self.assertEqual(data["id"], str(self.user_1_item.id))
        self.assertEqual(data["name"], str(payload_item["name"]))
        self.assertEqual(data["owner"]["id"], str(self.user_2.id))
        self.assertEqual(data["completed"], payload_item["completed"])
        self.assertEqual(200, response.status_code)
        self.client.logout()

    def test_user_can_not_update_other_users_item(self):
        """ " Returns Not_Found(404) updating to-do item of another user as user"""
        self.client.force_login(self.user_1)

        response = self.client.put(reverse("todo-detail", args=[self.user_2_item.id]))
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """ " Returns Forbidden(403) as not logged in"""
        response = self.client.put(reverse("todo-detail", args=[self.user_1_item.id]))

        self.assertEqual(403, response.status_code)
