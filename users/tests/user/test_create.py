from django.test import TestCase
from rest_framework.test import APIClient
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from to_do.models.Todo import Todo


class CreateUserTest(TestCase):
    """
        POST /api/todos
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user_1 = get_user_model().objects.create_user(self.user1Data['email'],
                                               self.user1Data['password'])

        self.adminData = {
            'email': 'admin@example.com',
            'password': 'testing_password_123'
        }
        self.admin = get_user_model().objects.create_user(self.adminData['email'],
                                              self.adminData['password'])
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name="admin_item1", owner=self.admin)

    def test_admin_can_create_users(self):
        """" Returns Created(201) creating user  as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post('/api/auth/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_user_data = {
            'email': 'newmail@example.com',
            'password': self.user1Data['password']}

        response = self.client.post('/api/users/', payload_new_user_data)
        data = response.data

        self.assertEqual(data['email'], payload_new_user_data['email'])
        self.assertEqual(201, response.status_code)

    def test_empty_data(self):
        """" Returns Bad Request(400) sending no data  as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post('/api/auth/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.post('/api/users/')

        self.assertEqual(400, response.status_code)

    def test_user_can_not_create_other_users(self):
        """" Returns FORBIDDEN(403) creating user as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/auth/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_user_data = {
            'email': 'newmail@example.com',
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/users/', payload_new_user_data)
        self.assertEqual(403, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.post('/api/users/')

        self.assertEqual(403, response.status_code)
