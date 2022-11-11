from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import UserManager


class UserManager(BaseUserManager):

    def create_user(self, username, first_name="", last_name="", email="", is_superuser=False, is_staff=False, password=None):
        # if not email:
        #     raise ValueError('Users must have an email address')
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            is_superuser=is_superuser,
            is_staff=is_staff
        )
        user.is_active = True

        user.set_password(password)
        user.save(using=self._db)

        return user

    # def reset_password(self, password, old_password, username):  # TODO user.password_changed???
    #     # print(username)
    #     user = self.get(id=3)
    #     print(user)
    #     if self.model.check_password(self, old_password):
    #         user.set_password(password)
    #         user.save(using=self._db)
    #         return user
    #
    #     else:
    #         return None
    def create_superuser(self, username, first_name='', last_name='', email='', password=None):
        """
        функция для создания суперпользователя — с ее помощью мы создаем админинстратора
        это можно сделать с помощью команды createsuperuser
        """
        # TODO проверить надежность такой работы в сравнении с UserManager мб normalize_mail понадобится

        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_superuser=True,
            is_staff=True
        )

        user.save(using=self._db)
        return user



