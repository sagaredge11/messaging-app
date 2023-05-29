from django.test import TestCase

# Create your tests here.
# Import necessary libraries and modules
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from . import consumers
from .models import Message

class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_successful_authentication(self):
        client = APIClient()
        response = client.post('/api/login/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_invalid_credentials(self):
        client = APIClient()
        response = client.post('/api/login/', {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.data)

    def test_unauthorized_access(self):
        client = APIClient()
        response = client.get('/api/messages/')
        self.assertEqual(response.status_code, 401)


class WebSocketTest(TestCase):
    async def test_send_message(self):
        user = await database_sync_to_async(User.objects.create_user)('testuser', 'testpass')
        token = await database_sync_to_async(Token.objects.create)(user=user)
        communicator = WebsocketCommunicator(consumers, '/ws/chat/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({'message': 'Hello, World!'})
        response = await communicator.receive_json_from()

        self.assertEqual(response['message'], 'Hello, World!')

        await communicator.disconnect()

class APITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

    def test_get_messages(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.get('/api/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.data)

    def test_create_message(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post('/api/messages/', {'content': 'Hello, World!'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.data)
        self.assertEqual(Message.objects.count(), 1)

