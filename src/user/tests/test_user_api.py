from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:new_user')
TOKEN_URL = reverse('user:token')


class NewUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_new_user(self):
        """Create new user with valid email"""
        payload = {
            'email': 'testuser@email.com',
            'password': 'NewUserPass',
            'name': 'The Mute Bishop'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_duplicate_user(self):
        """test create new user when user already exists fail"""
        payload = {
            'email': 'testuser@email.com',
            'password': 'NewUserPass',
            'name': 'The Mute Bishop'
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test password must be more that or equal to 8 charecters"""
        payload = {
            'email': 'testuser@email.com',
            'password': 'NewPass',
            'name': 'The Mute Bishop'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user)

    def test_create_token(self):
        """test new token is created for user"""
        payload = {
            'email': 'testuser@email.com',
            'password': 'NewUserPass',
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def create_token_invalid_user(self):
        """token is not created for invalid user credentials"""
        get_user_model().objects.create_user(email='testuser@email.com',
                                             password='NewUserPass',
                                             name='The Mute Bishop'
                                             )
        payload = {
            'email': 'testuser@email.com',
            'password': 'NewUserPass44',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_token_no_user(self):
        """token is not created for no user credentials"""
        payload = {
            'email': 'testuser@email.com',
            'password': 'NewUserPass44',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_token_missing_filed(self):
        """email and password required"""
        payload = {
            'email': 'testuser',
            'password': 'NewUserPass44',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
