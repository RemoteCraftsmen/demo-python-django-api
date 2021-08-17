from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from faker import Faker

from to_do.models.todo import Todo

faker = Faker()


class DeleteTodoTest(TestCase):
    """
        DELETE /api/todos/:id
    """
    def setUp(self):
        self.client = APIClient()

        self.user_1_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.password(length=12)
        }

        self.user_1 = get_user_model().objects.create_user(**self.user_1_data)
        self.user_1_item = Todo.objects.create(name=faker.pystr_format(), owner=self.user_1)

        self.user_2_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.password(length=12)
        }
        self.user_2 = get_user_model().objects.create_user(**self.user_2_data)
        self.user_2_item = Todo.objects.create(name=faker.pystr_format(), owner=self.user_2)
        self.admin_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.password(length=12)
        }

        self.admin = get_user_model().objects.create_user(**self.admin_data)
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name=faker.pystr_format(), owner=self.admin)

    def test_user_can_delete_only_his_item(self):
        """" Returns No_Content(204) selecting own to-do item  as user """
        self.client.force_login(self.user_1)

        response = self.client.delete(reverse('todo-detail', args=[self.user_1_item.id]))

        is_deleted_item_exist = Todo.objects.filter(id=self.user_1_item.id).exists()
        self.assertFalse(is_deleted_item_exist)

        self.assertEqual(204, response.status_code)
        self.client.logout()

    def test_admin_can_delete_all_item(self):
        """" Returns No_Content(204) selecting to-do item  as admin """
        self.client.force_login(self.admin)

        self.user_1_item = Todo.objects.create(name="User1_item1", owner=self.user_1)

        response = self.client.delete(reverse('todo-detail', args=[self.user_1_item.id]))
        is_deleted_item_exist = Todo.objects.filter(id=self.user_1_item.id).exists()
        self.assertFalse(is_deleted_item_exist)
        self.assertEqual(204, response.status_code)

        response = self.client.delete(reverse('todo-detail', args=[self.user_2_item.id]))
        is_deleted_item_exist = Todo.objects.filter(id=self.user_2_item.id).exists()
        self.assertFalse(is_deleted_item_exist)
        self.assertEqual(204, response.status_code)

        response = self.client.delete(reverse('todo-detail', args=[self.admin_item.id]))
        is_deleted_item_exist = Todo.objects.filter(id=self.user_2_item.id).exists()
        self.assertFalse(is_deleted_item_exist)
        self.assertEqual(204, response.status_code)
        self.client.logout()

    def test_user_can_not_delete_other_users_item(self):
        """" Returns Not_Found(404) selecting to-do item of another user as user """
        self.client.force_login(self.user_1)

        self.user_2_item = Todo.objects.create(name="User2_item1", owner=self.user_2)

        response = self.client.delete(reverse('todo-detail', args=[self.user_2_item.id]))
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.delete(reverse('todo-detail', args=[self.user_1_item.id]))

        self.assertEqual(403, response.status_code)
