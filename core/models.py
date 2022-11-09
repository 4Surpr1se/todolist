from django.contrib.auth.models import AbstractUser
from django.db import models

from core.managers import UserManager


class User(AbstractUser):
    pass
    new = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    objects = UserManager()

class Eeee(models.Model):  # Че это?
    num = models.IntegerField()

