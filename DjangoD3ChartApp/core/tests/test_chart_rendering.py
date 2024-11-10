# core/tests/test_chart_rendering.py
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class ChartRenderingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="testpassword")
        self.login_url = reverse("login")  # Login URL
        self.chart_url = reverse("chart-view")  # URL for the chart page

    def test_d3_chart_rendering_on_login(self):
        """Test that the D3 chart page is displayed after successful login"""
        
        # Log in the user with a `next` parameter to redirect to the chart view
        login_response = self.client.post(self.login_url + '?next=' + self.chart_url, {
            "username": "testuser@example.com",
            "password": "testpassword"
        })

        # Check login success and that it redirects to chart view
        self.assertEqual(login_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(login_response, self.chart_url)
        
        # Access the chart page
        chart_response = self.client.get(self.chart_url)
        self.assertEqual(chart_response.status_code, status.HTTP_200_OK)
        
        # Check if the response contains the placeholder for the D3 chart
        self.assertContains(chart_response, '<div id="chart-container">')
