from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory

faker = Factory.create()


class ShowUsersTest(TestCase):
    """
        GET /api/users/:id
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }
        self.user_1 = get_user_model().objects.create_user(**self.user1Data)

        self.user2Data = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }
        self.user_2 = get_user_model().objects.create_user(**self.user2Data)

        self.adminData = {
            'email': faker.ascii_safe_email(),
            'password': faker.pystr_format()
        }
        self.admin = get_user_model().objects.create_user(**self.adminData)
        self.admin.is_staff = True
        self.admin.save()

    def test_admin_can_see_other_user(self):
        """" Returns OK(200) as user """
        self.client.force_login(self.admin)

        response = self.client.get(reverse('user-detail', args=[self.user_1.id]))
        data = response.data

        self.assertEqual(data['id'], str(self.user_1.id))
        self.assertEqual(data['email'], self.user_1.email)
        self.assertEqual(data['is_staff'], self.user_1.is_staff)

        self.assertEqual(200, response.status_code)
        self.client.logout()

    def test_user_can_not_see_another_user(self):
        """" Returns Forbidden(403) as user """
        self.client.force_login(self.user_1)

        response = self.client.get(reverse('user-detail', args=[self.user_2.id]))
        self.assertEqual(403, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get(reverse('user-detail', args=[self.user_1.id]))

        self.assertEqual(403, response.status_code)
