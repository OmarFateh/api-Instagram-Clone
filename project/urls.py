"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title = "Fatehgram API",
        default_version = "V1",
        description = "Test Description",
        terms_of_service = "https://www.fatehgram.com/policies/terms/",
        contact = openapi.Contact(email="contact@fatehgram.local"),
        license = openapi.License(name="Test License"),
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Swagger 
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # API Endpoints
    path('api/items/', include(('item.urls', 'item'), namespace='item-api')),
    path('api/users/', include(('accounts.urls', 'accounts'), namespace='users-api')),
    path('api/profiles/', include(('profiles.urls', 'profiles'), namespace='profiles-api')),
    path('api/home/', include(('home.urls', 'home'), namespace='home-api')),
    path('api/explore/', include(('explore.urls', 'explore'), namespace='explore-api')),
    path('api/notifications/', include(('notifications.urls', 'notifications'), namespace='notifications-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)