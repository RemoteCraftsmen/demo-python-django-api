from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Factory
faker = Factory.create()


class IndexUsersTest(TestCase):
    """
        GET /api/users
    """
    def setUp(self):
        self.client = APIClient()
        self.user_list_url = reverse('user-list')

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

        self.users = [self.user_1, self.user_2, self.admin]

    def test_admin_can_see_users(self):
        """" Returns OK(200) as Admin """
        self.client.force_login(self.admin)

        response = self.client.get(self.user_list_url)
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
        self.client.logout()

    def test_user_can_not_see_users(self):
        """" Returns Forbidden(403) as user """
        self.client.force_login(self.user_1)

        response = self.client.get(self.user_list_url)
        self.assertEqual(403, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get(self.user_list_url)

        self.assertEqual(403, response.status_code)
