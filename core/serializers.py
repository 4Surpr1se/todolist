from rest_framework import serializers, exceptions
import django.contrib.auth.password_validation as validators

from core.models import User


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField() # TODO совпадают ли валидаторы модели и сериализатора?(тут, например, надо установить max_length) чтобы не было, например, что в модели max_length = 12, а тут max_length = 100

    class Meta:
        model = User
        fields = ('password_repeat', 'password', 'username', 'first_name', 'last_name', 'email')
        extra_kwargs = {'first_name': {'required': False},
                        'last_name': {'required': False},
                        'email': {'required': False}}

    password_repeat = serializers.CharField(write_only=True)

    # def validate_username(self, data): # Похоже через validate_ + имя поля можно валидировать что-угодно
    #     a = 1
    #     return 33

    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return data

    # super().create()

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password_repeat']:
            raise serializers.ValidationError({"password": "passwords do not match"})
        else:
            validated_data.pop('password_repeat')
            user = User.objects.create_user(**validated_data)
            # user = super().create(validated_data)
            # user.set_password(validated_data['password'])  # Метод получше?
            # user.save()
            return user


class Serializerer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class ResetPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(read_only=True)

    # super().required
    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'password')

    # super().is_valid()
    def validate_new_password(self, data):
        validators.validate_password(password=data, user=User)
        print(1)
        return data

    def update(self, instance, validated_data):
        # if validated_data['old_password'] in s
        print(validated_data['old_password'])
        print(instance.is_active)
        if instance.check_password(validated_data['old_password']):
            instance.set_password(validated_data['new_password'])
            instance.save()
            print(instance.password)
            return instance

        else:
            # return serializers.ValidationError({"old_password": "password is uncorrected"})
            print(100)
            raise serializers.ValidationError({"old_password": "password is uncorrected"})
