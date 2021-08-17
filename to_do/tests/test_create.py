from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from faker import Factory

from to_do.models.Todo import Todo

faker = Factory.create()


class CreateToDoTest(TestCase):
    """
        POST /api/todos
    """
    def setUp(self):
        self.client = APIClient()
        self.todo_list_url = reverse('todo-list')

        self.user1Data = {
            'email': faker.ascii_safe_email(),
            'password': faker.password(length=12)
        }

        self.user_1 = get_user_model().objects.create_user(**self.user1Data)

        self.adminData = {
            'email': faker.ascii_safe_email(),
            'password': faker.password(length=12)
        }
        self.admin = get_user_model().objects.create_user(**self.adminData)
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name=faker.pystr_format(), owner=self.admin)

    def test_todo_item_valid_data(self):
        """" Returns Created(201) sending correct data as user """
        self.client.force_login(self.user_1)

        payload_todo = {'name': 'tests item'}
        response = self.client.post(self.todo_list_url, payload_todo)

        data = response.data

        self.assertEqual(payload_todo['name'], data['name'])
        self.assertEqual(str(self.user_1.id), data['owner']['id'])
        created_item = Todo.objects.filter(id=data['id']).exists()
        self.assertTrue(created_item)

        self.assertEqual(201, response.status_code)
        self.client.logout()

    def test_todo_admin_can_set_owner(self):
        """" Returns Created(201) sending correct data as admin """
        self.client.force_login(self.admin)

        payload_todo = {
            'name': 'tests item',
            'owner_id': self.user_1.id
        }

        response = self.client.post(self.todo_list_url, payload_todo)
        data = response.data

        self.assertEqual(payload_todo['name'], data['name'])
        self.assertEqual(str(self.user_1.id), data['owner']['id'])
        created_item = Todo.objects.filter(id=data['id']).exists()
        self.assertTrue(created_item)
        self.assertEqual(201, response.status_code)
        self.client.logout()

    def test_bad_request_when_owner_doesnt_exists(self):
        """" Returns Bad Request(400) sending incorrect data as admin """
        self.client.force_login(self.admin)

        payload_todo = {
            'name': 'tests item',
            'owner_id': 'wrong_user_id'
        }

        response = self.client.post(self.todo_list_url, payload_todo)
        data = response.data
        errors = data['errors']

        self.assertEqual('Must be a valid UUID.', errors['owner_id'][0])

        self.assertEqual(400, response.status_code)
        self.client.logout()

    def test_user_can_not_sets_owner(self):
        """" Returns Created(201) sending correct data with owner_id as user """
        self.client.force_login(self.user_1)

        payload_todo = {
            'name': 'tests item',
            'owner_id': self.admin.id
        }

        response = self.client.post(self.todo_list_url, payload_todo)
        data = response.data

        self.assertEqual(payload_todo['name'], data['name'])
        self.assertEqual(str(self.user_1.id), data['owner']['id'])
        created_item = Todo.objects.filter(id=data['id']).exists()
        self.assertTrue(created_item)

        self.assertEqual(201, response.status_code)
        self.client.logout()

    def test_todo_item_must_be_valid(self):
        """" Returns Bad Request(400) sending wrong data as user """
        self.client.force_login(self.user_1)

        response = self.client.post(self.todo_list_url)
        errors = response.data['errors']

        self.assertEqual('This field is required.', errors['name'][0])
        self.assertEqual(400, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.post(self.todo_list_url)

        self.assertEqual(403, response.status_code)
