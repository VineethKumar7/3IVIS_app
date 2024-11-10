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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

@login_required
def chart_view(request):
    context = {
        'chart_data': CHART_DATA
    }
    return render(request, "core/chart.html", context)

