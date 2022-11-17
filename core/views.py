from typing import Union

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, \
    UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from .filters import LocationDateFilter
from .serializers import UserGetSerializer, UserCreateSerializer, ProfileInfoSerializer, ResetPasswordSerializer

from core.models import User


class LocationViewSet(ModelViewSet):  # TODO НАЙТИ СПОСОБ СДЕЛАТЬ ЭТО КРАСИВЕЕ
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    filter_backends = [
        DjangoFilterBackend, ]
    filterset_class = LocationDateFilter

    # def get_queryset(self) -> QuerySet:
    #     """if action is a list handles query params"""
    #     if self.action == 'list':
    #         queryset = User.objects.all()
    #         if username := self.request.GET.get('username'):
    #             queryset = queryset.filter(username=username)
    #         if email := self.request.GET.get('email'):
    #             queryset = queryset.filter(email=email)
    #         if last_name := self.request.GET.get('last_name'):
    #             queryset = queryset.filter(last_name=last_name)
    #         if first_name := self.request.GET.get('first_name'):
    #             queryset = queryset.filter(first_name=first_name)
    #         if is_filters := self.request.GET.get('is_filters'):
    #             is_filters = is_filters.split(', ')
    #             if 'is_superuser' in is_filters:
    #                 queryset = queryset.filter(is_superuser=True)
    #             if 'is_staff' in is_filters:
    #                 queryset = queryset.filter(is_staff=True)
    #             if 'is_active' in is_filters:
    #                 queryset = queryset.filter(is_active=True)
    #
    #         return queryset
    #     else:
    #         return super().get_queryset()

    def get_serializer_class(self) -> Union[type[UserCreateSerializer], type[UserGetSerializer]]:  # TODO Норм тайпинг?
        """serializer depending on the method"""
        if self.action == 'create':
            return UserCreateSerializer
        else:
            return UserGetSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AuthenticationCreateAPI(CreateAPIView, DestroyAPIView):
    # TODO Разобраться в этой еб*тор*и получше
    """implementing user authentication/login system"""

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # a = JsonResponse(UserGetSerializer(user).data, safe=False)
            # a['X-CSRFToken'] = get_token(request)
            # print(a)
            # return a
            return JsonResponse(UserGetSerializer(user).data, safe=False)

        else:
            raise exceptions.NotAuthenticated  # TODO правильный экспешион?

    def destroy(self, request: Request, *args, **kwargs) -> JsonResponse:
        if isinstance(request.user, AnonymousUser):
            return JsonResponse({'status': 'failed'}, status=401, safe=False)
        logout(request)
        return JsonResponse({'status': 'succeed'}, status=200, safe=False)


class PasswordReset(UpdateAPIView):
    """redefining get_object method to get user.id from session token
    (django by default tries to find pk in web path)"""
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def get_object(self) -> User:
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)

        return obj


# TODO Как я эту **** обошел? Создал кастом класс, который не чекает csrf, но надо нормально понять что он делает и вернуть его обратно
# TODO Убрать destroy из той вьюшки где он не нужен
class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """ implementing user logout view
     and redefining get_object method to get user.id from session token
     (same as we did in PasswordReset view)"""
    queryset = User.objects.all()
    serializer_class = ProfileInfoSerializer
    permission_classes = [IsAuthenticated, ]

    def destroy(self, request: Request, *args, **kwargs) -> JsonResponse:
        if isinstance(request.user, AnonymousUser):
            return JsonResponse({'status': 'failed'}, status=401, safe=False)
        logout(request)
        return JsonResponse({'status': 'succeed'}, status=200, safe=False)

    def get_object(self) -> User:
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)

        return obj
