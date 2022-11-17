from django.urls import path
from rest_framework import routers

from core.views import AuthenticationCreateAPI, UserRetrieveUpdateDestroyAPIView, PasswordReset, LocationViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('signup', LocationViewSet)


urlpatterns = [
    path('login', AuthenticationCreateAPI.as_view()),
    path('profile', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('update_password', PasswordReset.as_view()),
] + router.urls
