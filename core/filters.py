from django_filters import rest_framework

from core.models import User


class LocationDateFilter(rest_framework.FilterSet):

    class Meta:
        model = User
        fields = ['username', 'email',
                  'last_name', 'first_name',
                  'is_superuser', 'is_staff',
                  'is_active']
