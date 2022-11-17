from rest_framework import serializers
import django.contrib.auth.password_validation as validators

from core.models import User


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    """creating new write_only variable for password confirmation
     and validating password by default django password validators"""
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('password_repeat', 'password', 'username', 'first_name', 'last_name', 'email')
        extra_kwargs = {'first_name': {'required': False},
                        'last_name': {'required': False},
                        'email': {'required': False}}

    @staticmethod
    def validate_password(data: str) -> str:
        validators.validate_password(password=data, user=User)
        return data

    def create(self, validated_data: dict) -> User:
        if validated_data['password'] != validated_data['password_repeat']:
            raise serializers.ValidationError({"password": "passwords do not match"})
        else:
            validated_data.pop('password_repeat')
            user = User.objects.create_user(**validated_data)
            return user


class ProfileInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class ResetPasswordSerializer(serializers.ModelSerializer):
    """if old_password is correct and new_password validates successfully reseting user password,
    else raises error"""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'password')

    @staticmethod
    def validate_new_password(data: str) -> str:
        validators.validate_password(password=data, user=User)

        return data

    def update(self, instance: User, validated_data: dict) -> User:
        if instance.check_password(validated_data['old_password']):
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({"old_password": "Password is uncorrected"}, code=403)
