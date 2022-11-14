from django.contrib.auth.models import AbstractUser
from django.db import models

from core.managers import UserManager


class User(AbstractUser):
    """creating new User model inherited from AbstractUser,
     redefining objects"""
    pass
    new = models.BooleanField(default=False)# TODO зачем здесь это поле?

    def __str__(self):
        return self.username

    objects = UserManager()


class Eeee(models.Model):  # Че это?
    num = models.IntegerField()  # TODO убрать это

