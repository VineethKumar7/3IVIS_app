# core/views.py
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django_nvd3.templatetags.nvd3_tags import lineChart

User = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DataRetrievalView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        # Example data for a D3 chart 
        chart_data = [10, 20, 30, 40, 50] 
        return Response({"chart_data": chart_data}, status=status.HTTP_200_OK)

@login_required
def chart_view(request):
    return render(request, "core/chart.html")

@login_required
def nvd3_chart_view(request):
    # Sample data for the chart
    chart_data = {
        'x': list(range(1, 6)),  # x-axis labels
        'y': [random.randint(10, 50) for _ in range(5)]  # y-axis data
    }

    # Chart settings
    chart_type = "discreteBarChart"  # NVD3 chart type
    chart_container = "barChart_container"  # Chart container ID
    chart_data_series = [{
        'values': [{'x': x, 'y': y} for x, y in zip(chart_data['x'], chart_data['y'])],
        'key': 'Sample Data'
    }]
    
    context = {
        'chart_type': chart_type,
        'chart_container': chart_container,
        'chart_data_series': chart_data_series,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        }
    }
    return render(request, 'core/chart-nvd3.html', context)