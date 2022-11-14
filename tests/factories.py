import factory
from factory import PostGenerationMethodCall

from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_username"
    password = "test_password"
    first_name = 'test_first_name'
    last_name = 'test_last_name'

