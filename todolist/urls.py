"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework import routers
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core.views import LocationViewSet, AuthenticationCreateAPI, UserRetrieveUpdateDestroyAPIView, PasswordReset  # , UserAPIView

router = routers.SimpleRouter(trailing_slash=False)
router.register('core/signup', LocationViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('location/', UserAPIView.as_view())
    path('core/login', AuthenticationCreateAPI.as_view()),
    # path('core/login/', LoginView.as_view()),
    path('core/profile', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('core/update_password', PasswordReset.as_view()),
    path("goals/", include("goals.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + router.urls
