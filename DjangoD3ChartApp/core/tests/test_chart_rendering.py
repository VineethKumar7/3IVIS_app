from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

class ChartRenderingTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.login_url = reverse("login")  # Update with the correct login URL name
        self.chart_url = reverse("chart-view")  # Update with the actual URL name for the chart page

    def test_d3_chart_rendering_on_login(self):
        """Test that the D3 chart page is displayed after successful login"""
        
        # Log in the user
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword"
        })

        # Check login success and redirect to chart view
        self.assertEqual(login_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(login_response, self.chart_url)
        
        # Access the chart page
        chart_response = self.client.get(self.chart_url)
        self.assertEqual(chart_response.status_code, status.HTTP_200_OK)
        
        # Check if the response contains the placeholder for the D3 chart
        self.assertContains(chart_response, '<div id="chart-container">')