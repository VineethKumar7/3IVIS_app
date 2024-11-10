from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, DataRetrievalView, chart_view
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/data/', DataRetrievalView.as_view(), name='data-retrieve'),
    path('chart/', chart_view, name='chart-view'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
]