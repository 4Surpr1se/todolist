from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, first_name="", last_name="", email="",
                    is_superuser=False, is_staff=False):

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

    def create_superuser(self, username, password, first_name='', last_name='', email=''):
        """
        функция для создания суперпользователя — с ее помощью мы создаем админинстратора
        это можно сделать с помощью команды createsuperuser
        """

        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_superuser=True,
            is_staff=True
        )

        return user
