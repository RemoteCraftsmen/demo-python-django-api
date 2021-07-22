from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class IndexTest(TestCase):
    """
        /api/users
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

        self.users = [self.user_1, self.user_2, self.admin]

    def test_admin_can_see_users(self):
        """" Returns OK(200) as Admin """
        payload_user = {'email': self.adminData['email'], 'password': self.adminData['password']}
        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/users/')
        data = response.data

        self.assertEqual(3, len(data))

        for user in self.users:
            self.assertTrue(any(str(item['id']) == str(user.id) for item in data))
            self.assertTrue(any(item['username'] == user.username for item in data))
            self.assertTrue(any(item['email'] == user.email for item in data))
            self.assertTrue(any(item['is_staff'] == user.is_staff for item in data))

        self.assertEqual(200, response.status_code)

    def test_user_can_not_see_users(self):
        """" Returns Forbidden(403) as user """
        payload_user = {'email': self.user1Data['email'], 'password': self.user1Data['password']}
        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/users/')
        self.assertEqual(403, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get('/api/users/')

        self.assertEqual(403, response.status_code)
