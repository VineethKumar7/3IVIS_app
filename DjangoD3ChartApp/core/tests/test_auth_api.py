# core/tests/test_auth_api.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class AuthenticationAPITests(APITestCase):

    def test_registration_endpoint(self):
        """Test that the registration endpoint successfully creates a new user"""
        url = reverse("register")
        response = self.client.post(url, {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_endpoint(self):
        """Test that the login (token obtain) endpoint returns access and refresh tokens"""
        # Register a user first, as login requires a valid user
        self.client.post(reverse("register"), {"username": "testuser", "password": "testpassword"})
        
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh_endpoint(self):
        """Test that the token refresh endpoint returns a new access token"""
        # Register a user and obtain tokens first
        registration_response = self.client.post(reverse("register"), {"username": "testuser", "password": "testpassword"})
        refresh_token = registration_response.data["refresh"]

        url = reverse("token_refresh")
        response = self.client.post(url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
