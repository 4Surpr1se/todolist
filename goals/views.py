from django.db import transaction
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter, GoalCommentFilter, GoalCategoryFilter
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from goals.permissions import BoardPermissions
from goals.serializer import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    GoalCommentSerializer, GoalCommentCreateSerializer, BoardSerializer, BoardCreateSerializer, BoardListSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated, ]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalCategoryFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user,
                                           is_deleted=False)  # TODO возсожно надо удалить цель(Удаление цели = архивирование цели (кнопки «Удалить цель» нет).)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.method in ['PUT', 'DELETE']:
            return GoalCategory.objects.filter(board__participants__user=self.request.user,
                                               board__participants__role__in=[BoardParticipant.Role.owner,
                                                                              BoardParticipant.Role.writer],
                                               is_deleted=False)
        return GoalCategory.objects.filter(board__participants__user=self.request.user,
                                           is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated, ]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user, is_deleted=False)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.method in ['PUT', 'DELETE']:
            return Goal.objects.filter(category__board__participants__user=self.request.user,
                                       category__board__participants__role__in=[BoardParticipant.Role.owner,
                                                                                BoardParticipant.Role.writer],
                                       is_deleted=False)
        return Goal.objects.filter(category__board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated, ]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = GoalCommentFilter
    ordering_fields = ["created"]
    ordering = ["created"]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.method in ['PUT', 'DELETE']:
            return GoalComment.objects.filter(user=self.request.user)
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardListView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    permission_classes = [BoardPermissions]
    pagination_class = LimitOffsetPagination
    ordering_fields = ["title"]
    ordering = ["title"]

    #  Почему встроенная в BoardPermissions проверка аутентефикации не проходит

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardCreateView(CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [BoardPermissions]
    # pagination_class = LimitOffsetPagination
    # # filter_backends = [
    # #     DjangoFilterBackend,
    # #     filters.OrderingFilter,
    # # ]
    # # filterset_class = GoalCommentFilter
    # ordering_fields = ["title"]
    # ordering = ["title"]
