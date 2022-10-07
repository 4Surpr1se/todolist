from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q, F

from .serializers import UserGetSerializer

# Create your views here.
from django.views import View
# from django.views.generic import

from core.models import User


class LocationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer


class UserAPIView(ListAPIView):
    serializer_class = UserGetSerializer

    def get_queryset(self): #TODO ДОДЕЛАТЬ ЧЕРЕЗ Dict
        # queryset = User.objects.all().filter()
        # # if username := self.request.GET.get('name'):
        # #     for k, v in self.request.GET.items():
        # #         print(k, v)
        #
        # #
        # #     return queryset
        # if query := self.request.GET:
        #     a = dict((query))
        #     print(type(a))
        #     print(a)
        #
        #     queryset = queryset.filter(dict(query))
        queryset = User.objects.all()
        if username := self.request.GET.get('username'):
            queryset = queryset.filter(username=username)
        if email := self.request.GET.get('email'):
            queryset = queryset.filter(email=email)
        if last_name := self.request.GET.get('last_name'):
            queryset = queryset.filter(last_name=last_name)
        if first_name := self.request.GET.get('first_name'):
            queryset = queryset.filter(first_name=first_name)
        if is_filters := self.request.GET.get('is_filters'):
            is_filters = is_filters.split(', ')
            if 'is_superuser' in is_filters:
                queryset = queryset.filter(is_superuser=True)
            if 'is_staff' in is_filters:
                queryset = queryset.filter(is_staff=True)
            if 'is_active' in is_filters:
                queryset = queryset.filter(is_active=True)

        return queryset
