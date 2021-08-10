from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from to_do.models.Todo import Todo


class ShowToDoTest(TestCase):
    """
        GET /api/todos/:id
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user_1 = get_user_model().objects.create_user(self.user1Data['email'],
                                                           self.user1Data['password'])
        self.user_1_item = Todo.objects.create(name="User1_item1", owner=self.user_1)

        self.user2Data = {
            'email': 'test_user2@example.com',
            'password': 'testing_password_123'
        }
        self.user_2 = get_user_model().objects.create_user(self.user2Data['email'],
                                                           self.user2Data['password'])
        self.user_2_item = Todo.objects.create(name="User2_item1", owner=self.user_2)

        self.adminData = {
            'email': 'admin@example.com',
            'password': 'testing_password_123'
        }
        self.admin = get_user_model().objects.create_user(self.adminData['email'],
                                                          self.adminData['password'])
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name="admin_item1", owner=self.admin)

    def test_user_can_see_only_his_item(self):
        """" Returns Ok(200) selecting own to-do item  as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }
        response = self.client.post('/api/auth/login', payload_user)

        self.assertEqual(200, response.status_code)
        response = self.client.get('/api/todos/{}/'.format(self.user_1_item.id))
        data = response.data

        self.assertEqual(data['id'], str(self.user_1_item.id))
        self.assertEqual(data['name'], str(self.user_1_item.name))
        self.assertEqual(data['owner']['id'], str(self.user_1_item.owner.id))
        self.assertEqual(200, response.status_code)

    def test_admin_can_see_all_item(self):
        """" Returns Ok(200) selecting to-do item  as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post('/api/auth/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/todos/{}/'.format(self.user_1_item.id))
        data = response.data

        self.assertEqual(data['id'], str(self.user_1_item.id))
        self.assertEqual(data['name'], str(self.user_1_item.name))
        self.assertEqual(data['owner']['id'], str(self.user_1_item.owner.id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/todos/{}/'.format(self.user_2_item.id))
        data = response.data
        self.assertEqual(data['id'], str(self.user_2_item.id))
        self.assertEqual(data['name'], str(self.user_2_item.name))
        self.assertEqual(data['owner']['id'], str(self.user_2_item.owner.id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/todos/{}/'.format(self.admin_item.id))
        data = response.data
        self.assertEqual(data['id'], str(self.admin_item.id))
        self.assertEqual(data['name'], str(self.admin_item.name))
        self.assertEqual(data['owner']['id'], str(self.admin_item.owner.id))
        self.assertEqual(200, response.status_code)

    def test_user_can_not_see_other_users_item(self):
        """" Returns Not_Found(404) selecting to-do item of another user as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/auth/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/todos/{}/'.format(self.user_2_item.id))
        self.assertEqual(404, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get('/api/todos/{}/'.format(self.user_1_item.id))

        self.assertEqual(403, response.status_code)
