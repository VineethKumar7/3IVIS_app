from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self):
        # Create a user for testing authentication
        self.user = User.objects.create_user(email="testuser@example.com", password="testpassword")
        self.login_url = reverse("token_obtain_pair")  # The URL for JWT token authentication

    def test_login_with_valid_credentials(self):
        # Attempt login with valid credentials
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        # Expect 200 OK and check for "access" and "refresh" keys in the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # JWT access token should be present
        self.assertIn("refresh", response.data)  # JWT refresh token should be present

    def test_login_with_invalid_credentials(self):
        # Attempt login with invalid credentials
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",
            "password": "wrongpassword"
        })
        # Expect 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
