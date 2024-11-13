# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import WeatherData
from django.utils.timezone import datetime
from decimal import Decimal

User = get_user_model()
CHART_DATA = [60, 20, 30, 40, 50]

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        responses={201: "User created successfully", 400: "Validation error"},
    )

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

    @swagger_auto_schema(
        operation_description="Retrieve data for D3 chart",
        responses={200: openapi.Response("Chart data", examples={"chart_data": CHART_DATA})}
    )

    def get(self, request, *args, **kwargs):
        return Response({"chart_data": CHART_DATA}, status=status.HTTP_200_OK)



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("chart-view")  # Redirect to the chart view after successful login
    else:
        form = AuthenticationForm()
    
    return render(request, "registration/login_bootstrap.html", {"form": form})

class WeatherDataRetrievalView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve weather data for D3 chart",
        responses={200: openapi.Response("Chart data", examples={"chart_data": CHART_DATA})}
    )

    def get(self, request, *args, **kwargs):
        # Retrieve September data
        september_data = WeatherData.objects.filter(date__month=9).order_by("date")
        chart_data = [{"date": entry.date.strftime("%Y-%m-%d"), "temperature": entry.temperature, "humidity": entry.humidity} for entry in september_data]
        
        return Response({"chart_data": chart_data}, status=status.HTTP_200_OK)
    

@login_required
def chart_view(request):
    # Retrieve September data from the WeatherData model
    september_data = WeatherData.objects.filter(date__month=9).order_by("date")
    chart_data = [
        {
            "date": entry.date.strftime("%Y-%m-%d"),
            "temperature": float(entry.temperature) if isinstance(entry.temperature, Decimal) else entry.temperature,
            "humidity": float(entry.humidity) if isinstance(entry.humidity, Decimal) else entry.humidity
        }
        for entry in september_data
    ]
    
    print(chart_data)

    context = {
        "chart_data": chart_data  # Pass the data as JSON-compatible dictionary
    }
    
    return render(request, "core/chart.html", context)
