from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class ShowTest(TestCase):
    """
        /api/users/:id
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

    def test_admin_can_see_other_user(self):
        """" Returns OK(200) as user """
        payload_user = {'email': self.adminData['email'], 'password': self.adminData['password']}
        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/users/{}/'.format(self.user_1.id))
        data = response.data

        self.assertEqual(data['id'], self.user_1.id)
        self.assertEqual(data['username'], self.user_1.username)
        self.assertEqual(data['email'], self.user_1.email)
        self.assertEqual(data['is_staff'], self.user_1.is_staff)

        self.assertEqual(200, response.status_code)

    def test_user_can_not_see_another_user(self):
        """" Returns Forbidden(403) as user """
        payload_user = {'email': self.user1Data['email'], 'password': self.user1Data['password']}
        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/users/{}/'.format(self.user_2.id))
        self.assertEqual(403, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get('/api/users/{}/'.format(self.user_1.id))

        self.assertEqual(403, response.status_code)
