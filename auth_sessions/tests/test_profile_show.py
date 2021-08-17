from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from faker import Factory

faker = Factory.create()


class ShowProfileTest(TestCase):
    """
        GET /api/auth/profile
    """
    def setUp(self):
        self.client = APIClient()
        self.show_profile_url = reverse('show_profile')

        self.userData = {
            'email': faker.ascii_safe_email(),
            'password': faker.password(length=12)
        }

        self.user = get_user_model().objects.create_user(**self.userData)

    def test_user_can_see_its_profile(self):
        """" Returns Ok(200) sending valid data  as user """
        self.client.force_login(self.user)

        response = self.client.get(self.show_profile_url)
        data = response.data

        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(200, response.status_code)
        self.client.logout()

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get(self.show_profile_url)

        self.assertEqual(403, response.status_code)
