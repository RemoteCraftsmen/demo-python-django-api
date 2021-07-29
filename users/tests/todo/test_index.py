from django.test import TestCase
from rest_framework.test import APIClient
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ToDo.models.Todo import Todo


class IndexToDoTest(TestCase):
    """
        GET /api/todos
    """
    def setUp(self):
        self.client = APIClient()

        self.user1Data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'testing_password_123'
        }

        self.user_1 = get_user_model().objects.create_user(self.user1Data['username'], self.user1Data['email'],
                                               self.user1Data['password'])

        self.user_1_items = [
            Todo.objects.create(name="User1_item1", owner=self.user_1),
            Todo.objects.create(name="User1_item2", owner=self.user_1),
            Todo.objects.create(name="User1_item3", owner=self.user_1)
        ]

        self.user2Data = {
            'username': 'test_user2',
            'email': 'test_user2@example.com',
            'password': 'testing_password_123'
        }

        self.user_2 = get_user_model().objects.create_user(self.user2Data['username'], self.user2Data['email'],
                                               self.user2Data['password'])

        self.user_2_items = [
            Todo.objects.create(name="User2_item1", owner=self.user_2),
            Todo.objects.create(name="User2_item2", owner=self.user_2)
        ]

        self.adminData = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'testing_password_123'
        }

        self.admin = get_user_model().objects.create_user(self.adminData['username'], self.adminData['email'],
                                              self.adminData['password'])
        self.admin.is_staff = True
        self.admin.save()

        self.admin_items = [
            Todo.objects.create(name="admin_item1", owner=self.admin),
            Todo.objects.create(name="admin_item2", owner=self.admin)
        ]

    def test_user1_can_see_only_his_items(self):
        """" Returns Ok(200) as user """
        payload_user = {
            'email': self.user1Data['email'],
            'password': self.user1Data['password']
        }
        response = self.client.post('/api/login', payload_user)

        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/todos/')
        data = response.data
        self.assertIn('next', data)
        self.assertIn('previous', data)

        count = data['count']
        self.assertEqual(len(self.user_1_items), count)

        results = data['results']
        self.assertEqual(len(self.user_1_items), len(results))

        for todo_item in self.user_1_items:
            self.assertTrue(any(item['id'] == str(todo_item.id) for item in results))
            self.assertTrue(any(item['name'] == str(todo_item.name) for item in results))
            self.assertTrue(all(str(item['owner']['id']) == str(todo_item.owner.id) for item in results))

        for todo_item in self.user_2_items:
            self.assertFalse(any(item['id'] == str(todo_item.id) for item in results))
            self.assertFalse(any(str(item['owner']['id']) == str(todo_item.owner.id) for item in results))

        for todo_item in self.admin_items:
            self.assertFalse(any(item['id'] == str(todo_item.id) for item in results))
            self.assertFalse(any(str(item['owner']['id']) == str(todo_item.owner.id) for item in results))

        self.assertEqual(200, response.status_code)

    def test_admin_can_see_only_all_items(self):
        """" Returns Ok(200) as admin """
        payload_admin = {
            'email': self.adminData['email'],
            'password': self.adminData['password']
        }
        response = self.client.post('/api/login', payload_admin)

        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/todos/')
        data = response.data
        self.assertIn('next', data)
        self.assertIn('previous', data)

        results = data['results']
        all_items = self.user_1_items + self.user_2_items + self.admin_items
        count = data['count']
        self.assertEqual(len(all_items), count)

        self.assertEqual(len(all_items), len(results))

        for todo_item in all_items:
            self.assertTrue(any(item['id'] == str(todo_item.id) for item in results))
            self.assertTrue(any(item['name'] == str(todo_item.name) for item in results))

        self.assertEqual(200, response.status_code)

    def test_not_logged_in(self):
        """" Returns Forbidden(403) as not logged in """
        response = self.client.get('/api/todos/')

        self.assertEqual(403, response.status_code)
