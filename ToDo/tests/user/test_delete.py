from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class DeleteToDoTest(TestCase):
    """
        DELETE /api/todos/:id
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user_1 = User.objects.create_user(self.user1Data['username'], self.user1Data['email'],
                                               self.user1Data['password'])
        self.user2Data = {
            'username': 'test_user2',
            'email': 'test_user2@example.com',
            'password': 'testing_password_123'
        }
        self.user_2 = User.objects.create_user(self.user2Data['username'], self.user2Data['email'],
                                               self.user2Data['password'])
        self.adminData = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'testing_password_123'
        }

        self.admin = User.objects.create_user(self.adminData['username'], self.adminData['email'],
                                              self.adminData['password'])
        self.admin.is_staff = True
        self.admin.save()

    def test_admin_can_delete_users(self):
        """" Returns No_Content(204) selecting to-do item  as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.delete('/api/users/{}/'.format(self.user_2.id))
        is_deleted_item_exist = User.objects.filter(id=self.user_2.id).exists()
        self.assertFalse(is_deleted_item_exist)
        self.assertEqual(204, response.status_code)

    def test_user_can_not_delete_other_users(self):
        """" Returns FORBIDDEN(403) deleting user as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.delete('/api/users/{}/'.format(self.user_2.id))
        self.assertEqual(403, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.delete('/api/users/{}/'.format(self.user_2.id))

        self.assertEqual(403, response.status_code)