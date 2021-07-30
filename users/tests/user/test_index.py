from django.test import TestCase
from rest_framework.test import APIClient
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class IndexToDoTest(TestCase):
    """
        GET /api/users
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }
        self.user_1 = get_user_model().objects.create_user(self.user1Data['email'],
                                               self.user1Data['password'])

        self.user2Data = {
            'email': 'test_user2@example.com',
            'password': 'testing_password_123'
        }
        self.user_2 = get_user_model().objects.create_user(self.user2Data['email'],
                                               self.user2Data['password'])

        self.adminData = {
            'email': 'admin@example.com',
            'password': 'testing_password_123'
        }
        self.admin = get_user_model().objects.create_user(self.adminData['email'],
                                              self.adminData['password'])
        self.admin.is_staff = True
        self.admin.save()

        self.users = [self.user_1, self.user_2, self.admin]

    def test_admin_can_see_users(self):
        """" Returns OK(200) as Admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/users/')
        data = response.data
        self.assertIn('next', data)
        self.assertIn('previous', data)

        count = data['count']
        self.assertEqual(3, count)

        results = data['results']
        self.assertEqual(3, len(results))

        for user in self.users:
            self.assertTrue(any(str(item['id']) == str(user.id) for item in results))
            self.assertTrue(any(item['email'] == user.email for item in results))
            self.assertTrue(any(item['is_staff'] == user.is_staff for item in results))

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
