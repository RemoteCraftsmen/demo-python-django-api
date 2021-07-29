from django.test import TestCase
from rest_framework.test import APIClient
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ToDo.models.Todo import Todo


class UpdateToDoTest(TestCase):
    """
        PUT /api/todos/:id
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user_1 = get_user_model().objects.create_user(self.user1Data['email'],
                                               self.user1Data['password'])
        self.user_1_item = Todo.objects.create(name="User1_item1", owner=self.user_1)
        self.user2Data = {
            'username': 'test_user2',
            'email': 'test_user2@example.com',
            'password': 'testing_password_123'
        }
        self.user_2 = get_user_model().objects.create_user(self.user2Data['email'],
                                               self.user2Data['password'])
        self.user_2_item = Todo.objects.create(name="User2_item1", owner=self.user_2)
        self.adminData = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'testing_password_123'
        }

        self.admin = get_user_model().objects.create_user(self.adminData['email'],
                                              self.adminData['password'])
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name="admin_item1", owner=self.admin)

    def test_admin_can_update_all_users(self):
        """" Returns Ok(200) updating user  as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_user_data = {
            'email': 'newmail@example.com',
            'username': "new_test_user",
            'password': self.user1Data['password']}

        response = self.client.put('/api/users/{}/'.format(self.user_2.id), payload_new_user_data)
        data = response.data

        self.assertEqual(str(data['id']), str(self.user_2.id))
        self.assertEqual(data['email'], payload_new_user_data['email'])
        self.assertEqual(200, response.status_code)

    def test_user_can_not_update_other_users(self):
        """" Returns FORBIDDEN(403) deleting user as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_user_data = {
            'email': 'newmail@example.com',
            'password': self.user1Data['password']
        }

        response = self.client.put('/api/users/{}/'.format(self.user_2.id), payload_new_user_data)
        self.assertEqual(403, response.status_code)

    def test_user_can_not_update_itself(self):
        """" Returns FORBIDDEN(403) updating user"""
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_new_user_data = {'email': 'newmail@example.com',
                                 'username': "new_test_user",
                                 'password': self.user1Data['password']}

        response = self.client.put('/api/users/{}/'.format(self.user_1.id), payload_new_user_data)

        self.assertEqual(403, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.put('/api/users/{}/'.format(self.user_1.id))

        self.assertEqual(403, response.status_code)
