from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Faker

from to_do.models.todo import Todo

faker = Faker()


class IndexToDoTest(TestCase):
    """
        GET /api/todos
    """
    def setUp(self):
        self.client = APIClient()
        self.todo_list_url = reverse('todo-list')

        self.user_1 = get_user_model().objects.create_user(
            email=faker.ascii_safe_email(),
            password=faker.password(length=12))

        self.user_1_items = [
            Todo.objects.create(name=faker.pystr_format(), owner=self.user_1),
            Todo.objects.create(name=faker.pystr_format(), owner=self.user_1),
            Todo.objects.create(name=faker.pystr_format(), owner=self.user_1)
        ]


        user_2 = get_user_model().objects.create_user(
            email=faker.ascii_safe_email(),
            password=faker.password(length=12))

        self.user_2_items = [
            Todo.objects.create(name=faker.pystr_format(), owner=user_2),
            Todo.objects.create(name=faker.pystr_format(), owner=user_2)
        ]

        self.admin = get_user_model().objects.create_user(
            email=faker.ascii_safe_email(),
            password=faker.password(length=12))
        self.admin.is_staff = True
        self.admin.save()

        self.admin_items = [
            Todo.objects.create(name=faker.pystr_format(), owner=self.admin),
            Todo.objects.create(name=faker.pystr_format(), owner=self.admin)
        ]

    def test_user1_can_see_only_his_items(self):
        """" Returns Ok(200) as user """
        self.client.force_login(self.user_1)

        response = self.client.get(self.todo_list_url)
        data = response.data
        self.assertIn('next', data)
        self.assertIn('previous', data)

        count = data['count']
        self.assertEqual(len(self.user_1_items), count)

        results = data['results']
        self.assertEqual(len(self.user_1_items), len(results))

        for todo_item in self.user_1_items:
            self.assertTrue(
                any(item['id'] == str(todo_item.id)
                    for item in results))
            self.assertTrue(
                any(item['name'] == str(todo_item.name)
                    for item in results))
            self.assertTrue(
                all(str(item['owner']['id']) == str(todo_item.owner.id)
                    for item in results))

        for todo_item in self.user_2_items:
            self.assertFalse(
                any(item['id'] == str(todo_item.id)
                    for item in results))
            self.assertFalse(
                any(str(item['owner']['id']) == str(todo_item.owner.id)
                    for item in results))

        for todo_item in self.admin_items:
            self.assertFalse(
                any(item['id'] == str(todo_item.id)
                    for item in results))
            self.assertFalse(
                any(str(item['owner']['id']) == str(todo_item.owner.id)
                    for item in results))

        self.assertEqual(200, response.status_code)
        self.client.logout()

    def test_admin_can_see_only_all_items(self):
        """" Returns Ok(200) as admin """
        self.client.force_login(self.admin)

        response = self.client.get(self.todo_list_url)
        data = response.data
        self.assertIn('next', data)
        self.assertIn('previous', data)

        results = data['results']
        all_items = self.user_1_items + self.user_2_items + self.admin_items
        count = data['count']
        self.assertEqual(len(all_items), count)

        self.assertEqual(len(all_items), len(results))

        for todo_item in all_items:
            self.assertTrue(
                any(item['id'] == str(todo_item.id)
                    for item in results))
            self.assertTrue(
                any(item['name'] == str(todo_item.name)
                    for item in results))

        self.assertEqual(200, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get(self.todo_list_url)

        self.assertEqual(403, response.status_code)
