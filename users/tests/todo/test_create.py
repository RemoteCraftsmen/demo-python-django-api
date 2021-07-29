from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ToDo.models.Todo import Todo


class CreateToDoTest(TestCase):
    """
        POST /api/todos
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user_1 = get_user_model().objects.create_user(self.user1Data['email'], self.user1Data['password'])

        self.adminData = {
            'email': 'admin@example.com',
            'password': 'testing_password_123'
        }
        self.admin = get_user_model().objects.create_user(self.adminData['email'], self.adminData['password'])
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name="admin_item1", owner=self.admin)

    def test_todo_item_valid_data(self):
        """" Returns Created(201) sending correct data as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_todo = {'name': 'Test item'}
        response = self.client.post('/api/todos/', payload_todo)

        data = response.data

        self.assertEqual(payload_todo['name'], data['name'])
        self.assertEqual(str(self.user_1.id), data['owner']['id'])
        created_item = Todo.objects.filter(id=data['id']).exists()
        self.assertTrue(created_item)

        self.assertEqual(201, response.status_code)

    def test_todo_admin_can_set_owner(self):
        """" Returns Created(201) sending correct data as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_todo = {
            'name': 'Test item',
            'owner_id': self.user_1.id
        }

        response = self.client.post('/api/todos/', payload_todo)
        data = response.data

        self.assertEqual(payload_todo['name'], data['name'])

        self.assertEqual(str(self.user_1.id), data['owner']['id'])

        created_item = Todo.objects.filter(id=data['id']).exists()

        self.assertTrue(created_item)

        self.assertEqual(201, response.status_code)

    def test_bad_request_when_owner_doesnt_exists(self):
        """" Returns Bad Request(400) sending incorrect data as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }
        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_todo = {
            'name': 'Test item',
            'owner_id': 'wrong_user_id'
        }

        response = self.client.post('/api/todos/', payload_todo)
        data = response.data
        errors = data['errors']

        self.assertEqual('Must be a valid UUID.', errors['owner_id'][0])

        self.assertEqual(400, response.status_code)

    def test_user_can_not_sets_owner(self):
        """" Returns Created(201) sending correct data with owner_id as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }
        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_todo = {
            'name': 'Test item',
            'owner_id': self.admin.id
        }

        response = self.client.post('/api/todos/', payload_todo)
        data = response.data

        self.assertEqual(payload_todo['name'], data['name'])
        self.assertEqual(str(self.user_1.id), data['owner']['id'])
        created_item = Todo.objects.filter(id=data['id']).exists()
        self.assertTrue(created_item)

        self.assertEqual(201, response.status_code)

    def test_todo_item_must_be_valid(self):
        """" Returns Bad Request(400) sending wrong data as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.post('/api/todos/')
        errors = response.data['errors']

        self.assertEqual('This field is required.', errors['name'][0])
        self.assertEqual(400, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.post('/api/todos/')

        self.assertEqual(403, response.status_code)
