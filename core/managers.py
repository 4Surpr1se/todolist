from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, first_name="", last_name="", email="", password=None):
        # if not email:
        #     raise ValueError('Users must have an email address')
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
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



