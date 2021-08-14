from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from to_do.models.Todo import Todo
from django.urls import reverse
from faker import Factory
faker = Factory.create()


class UpdateToDoTest(TestCase):
    """
        PUT /api/todos/:id
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }
        self.user_1 = get_user_model().objects.create_user(**self.user1Data)
        self.user_1_item = Todo.objects.create(name=faker.pystr_format(), owner=self.user_1)

        self.user2Data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }
        self.user_2 = get_user_model().objects.create_user(**self.user2Data)
        self.user_2_item = Todo.objects.create(name=faker.pystr_format(), owner=self.user_2)

        self.adminData = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }
        self.admin = get_user_model().objects.create_user(**self.adminData)
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name=faker.pystr_format(), owner=self.admin)

    def test_admin_can_update_all_users(self):
        """" Returns Ok(200) updating user  as admin """
        self.client.force_login(self.admin)

        payload_new_user_data = {
            'email': faker.ascii_safe_email(),
            'password': self.user1Data['password']}

        response = self.client.put(reverse('user-detail', args=[self.user_2.id]), payload_new_user_data)
        data = response.data

        self.assertEqual(str(data['id']), str(self.user_2.id))
        self.assertEqual(data['email'], payload_new_user_data['email'])
        self.assertEqual(200, response.status_code)
        self.client.logout()

    def test_user_can_not_update_other_users(self):
        """" Returns FORBIDDEN(403) deleting user as user """
        self.client.force_login(self.user_1)

        payload_new_user_data = {
            'email': faker.ascii_safe_email(),
            'password': self.user1Data['password']
        }

        response = self.client.put(reverse('user-detail', args=[self.user_2.id]), payload_new_user_data)
        self.assertEqual(403, response.status_code)
        self.client.logout()

    def test_user_can_not_update_itself(self):
        """" Returns FORBIDDEN(403) updating user"""
        self.client.force_login(self.user_1)

        payload_new_user_data = {'email': faker.ascii_safe_email(),
                                 'password': self.user1Data['password']}

        response = self.client.put(reverse('user-detail', args=[self.user_1.id]), payload_new_user_data)

        self.assertEqual(403, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.put(reverse('user-detail', args=[self.user_1.id]))

        self.assertEqual(403, response.status_code)
