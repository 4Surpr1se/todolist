from django.contrib.auth.models import AbstractUser

from core.managers import UserManager


class User(AbstractUser):
    """creating new User model inherited from AbstractUser,
     redefining objects"""

    def __str__(self):
        return self.username

    objects = UserManager()
