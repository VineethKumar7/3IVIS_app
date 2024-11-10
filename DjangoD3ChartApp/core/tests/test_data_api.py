from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class DataRetrievalAPITests(APITestCase):

    def setUp(self):
        # Create a user and get an authentication token
        self.user = User.objects.create_user(email="testuser@example.com", password="testpassword")
        self.url = reverse("data-retrieve")  
        self.access_token = self.get_access_token()

    def get_access_token(self):
        # Helper function to get a JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_data_retrieval_without_authentication(self):
        """Test that data retrieval without authentication returns 401 Unauthorized"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_data_retrieval_with_authentication(self):
        """Test that data retrieval with authentication returns 200 OK and expected data"""
        # Add the access token to the authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect specific data structure (e.g., a 'chart_data' field)
        self.assertIn("chart_data", response.data)
        self.assertIsInstance(response.data["chart_data"], list) 
