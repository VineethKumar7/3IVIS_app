# core/views.py
import random
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
from random import randint
from nvd3 import discreteBarChart

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
    xdata = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"]
    ydata = [randint(10, 50) for _ in range(5)]
    
    chart = discreteBarChart(name='barChart', height=400, width=600)
    chart.add_serie(y=ydata, x=xdata)

    context = {
        'chart': chart,
    }

    return render(request, 'core/chart.html', context)
