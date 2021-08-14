from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


class DeleteToDoTest(TestCase):
    """
        DELETE /api/todos/:id
    """
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')

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

    def test_admin_can_delete_users(self):
        """" Returns No_Content(204) selecting to-do item  as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.delete(reverse('user-detail', args=[self.user_2.id]))
        self.assertEqual(204, response.status_code)

        response = self.client.get(reverse('user-detail', args=[self.user_2.id]))
        self.assertEqual(404, response.status_code)

    def test_user_can_not_delete_other_users(self):
        """" Returns FORBIDDEN(403) deleting user as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post(self.login_url, payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.delete(reverse('user-detail', args=[self.user_2.id]))
        self.assertEqual(403, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.delete(reverse('user-detail', args=[self.user_2.id]))

        self.assertEqual(403, response.status_code)
