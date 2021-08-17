from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Faker

faker = Faker()



class DeleteUsersTest(TestCase):
    """
        DELETE /api/users/:id
    """
    def setUp(self):
        self.client = APIClient()

        self.user_1_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }

        self.user_1 = get_user_model().objects.create_user(**self.user_1_data)
        self.user_2_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }
        self.user_2 = get_user_model().objects.create_user(**self.user_2_data)
        self.admin_data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }

        self.admin = get_user_model().objects.create_user(**self.admin_data)
        self.admin.is_staff = True
        self.admin.save()

    def test_admin_can_delete_users(self):
        """" Returns No_Content(204) selecting user  as admin """
        self.client.force_login(self.admin)

        response = self.client.delete(reverse('user-detail', args=[self.user_2.id]))
        self.assertEqual(204, response.status_code)

        response = self.client.get(reverse('user-detail', args=[self.user_2.id]))
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_user_can_not_delete_other_users(self):
        """" Returns FORBIDDEN(403) deleting user as user """
        self.client.force_login(self.user_1)

        response = self.client.delete(reverse('user-detail', args=[self.user_2.id]))
        self.assertEqual(403, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.delete(reverse('user-detail', args=[self.user_2.id]))

        self.assertEqual(403, response.status_code)
