from django.urls import path

from .views import NotificationsListAPIView     

"""
CLIENT
BASE ENDPOINT /api/notifications/
"""

urlpatterns = [

    # notifications. 
    path('', NotificationsListAPIView.as_view(), name='notifications'),

]