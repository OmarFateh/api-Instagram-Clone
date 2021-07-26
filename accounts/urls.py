from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (UserRegisterAPIView, UserLogoutAPIView, PassowordChangeAPIView, PasswordResetEmailAPIView,
                        PasswordResetTokenCheckAPIView, PasswordResetFormAPIView)


"""
CLIENT
BASE ENDPOINT /api/users/
"""

urlpatterns = [
    
    # Authentication
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    # Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Password
    path('password/change/', PassowordChangeAPIView.as_view(), name='password-change'),
    path('password/reset/', PasswordResetEmailAPIView.as_view(), name='password-reset'),
    path('password/reset/<uidb64>/<token>/', PasswordResetTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password/reset/complete/', PasswordResetFormAPIView.as_view(), name='password-reset-complete'),

]