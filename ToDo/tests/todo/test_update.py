from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ToDo.models.Todo import Todo


class UpdateToDoTest(TestCase):
    """
        PUT /api/todos/:id
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

        self.user_1_item = Todo.objects.create(name="User1_item1", owner=self.user_1)
        self.user2Data = {
            'username': 'test_user2',
            'email': 'test_user2@example.com',
            'password': 'testing_password_123'
        }
        self.user_2 = User.objects.create_user(self.user2Data['username'], self.user2Data['email'],
                                               self.user2Data['password'])
        self.user_2_item = Todo.objects.create(name="User2_item1", owner=self.user_2)

        self.adminData = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'testing_password_123'
        }
        self.admin = User.objects.create_user(self.adminData['username'], self.adminData['email'],
                                              self.adminData['password'])
        self.admin.is_staff = True
        self.admin.save()
        self.admin_item = Todo.objects.create(name="admin_item1", owner=self.admin)

    def test_user_can_update_its_item(self):
        """" Returns Ok(200) updating to-do item  as admin """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_item = {
            'name': 'User2_item1',
            'completed': True
        }

        response = self.client.put('/api/todos/{}/'.format(self.user_1_item.id), payload_item)
        data = response.data

        self.assertEqual(data['id'], str(self.user_1_item.id))
        self.assertEqual(data['name'], str(payload_item['name']))
        self.assertEqual(data['owner']['id'], self.user_1.id)
        self.assertEqual(data['completed'], payload_item['completed'])
        self.assertEqual(200, response.status_code)

    def test_admin_can_update_all_item(self):
        """" Returns Ok(200) updating to-do item  as admin """
        payload_user = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        payload_item = {
            'name': 'User2_item1',
            'owner_id': self.user_2.id,
            'completed': True
        }

        response = self.client.put('/api/todos/{}/'.format(self.user_1_item.id), payload_item)
        data = response.data

        self.assertEqual(data['id'], str(self.user_1_item.id))
        self.assertEqual(data['name'], str(payload_item['name']))
        self.assertEqual(data['owner']['id'], self.user_2.id)
        self.assertEqual(data['completed'], payload_item['completed'])
        self.assertEqual(200, response.status_code)

    def test_user_can_not_update_other_users_item(self):
        """" Returns Not_Found(404) updating to-do item of another user as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }

        response = self.client.post('/api/login', payload_user)
        self.assertEqual(200, response.status_code)

        response = self.client.put('/api/todos/{}/'.format(self.user_2_item.id))
        self.assertEqual(404, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.put('/api/todos/{}/'.format(self.user_1_item.id))

        self.assertEqual(403, response.status_code)
