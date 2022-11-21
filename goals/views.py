from django.db import transaction
from django.db.models import QuerySet
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
    """
    get_queryset method is overwritten for provide only board categories the user is a member of
    and some ordering, search_fields, filters
    """

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

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.filter(board__participants__user=self.request.user,
                                           is_deleted=False)  # TODO возсожно надо удалить цель(Удаление цели = архивирование цели (кнопки «Удалить цель» нет).)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    GET returns same queryset as GoalCategoryListView:
    get_queryset method is overwritten for provide only board categories the user is a member of,

    PUT and DELETE also checks user role in provided Board
    """
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        if self.request.method in ['PUT', 'DELETE']:
            return GoalCategory.objects.filter(board__participants__user=self.request.user,
                                               board__participants__role__in=[BoardParticipant.Role.owner,
                                                                              BoardParticipant.Role.writer],
                                               is_deleted=False)
        return GoalCategory.objects.filter(board__participants__user=self.request.user,
                                           is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        instance.is_deleted = True
        instance.save()
        # map(lambda x: setattr(x, 'is_deleted', True), Goal.objects.get(category=instance))
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated, ]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    """
    get_queryset same as GoalCategoryListView, except for searching it through category field:

    get_queryset method is overwritten for provide only board categories the user is a member of
    and some ordering, search_fields, filters
    """
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

    def get_queryset(self) -> QuerySet:
        return Goal.objects.filter(category__board__participants__user=self.request.user, is_deleted=False)


class GoalView(RetrieveUpdateDestroyAPIView):
    """
    GET returns same queryset as GoalListView:
    get_queryset method is overwritten for provide only board categories the user is a member of,

    PUT and DELETE also checks user role in provided Board

    perform_destroy is overwritten to not delete goal from db but just archive it by setting is_deleted flag to True
    """
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        if self.request.method in ['PUT', 'DELETE']:
            return Goal.objects.filter(category__board__participants__user=self.request.user,
                                       category__board__participants__role__in=[BoardParticipant.Role.owner,
                                                                                BoardParticipant.Role.writer],
                                       is_deleted=False)
        return Goal.objects.filter(category__board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> Goal:
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated, ]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    """
    get_queryset method is overwritten for provide only board category goals the user is a member of
    and some ordering, search_fields, filters
    """
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

    def get_queryset(self) -> QuerySet:
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """
    get_queryset is overwritten so that users can only delete and update their own comments
    GET method still gives comments of other users only if the user is a Board participant
    """
    model = Goal
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        if self.request.method in ['PUT', 'DELETE']:
            return GoalComment.objects.filter(user=self.request.user)
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class BoardView(RetrieveUpdateDestroyAPIView):
    """
    get_queryset method is overwritten for provide only boards the user is a member of
    perform_destroy doesn't delete the board, it archives the board and its categories
    """
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self) -> QuerySet:
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> Board:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardListView(ListAPIView):
    """
    get_queryset method is overwritten for provide only boards the user is a member of
    """
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    permission_classes = [BoardPermissions]
    pagination_class = LimitOffsetPagination
    ordering_fields = ["title"]
    ordering = ["title"]

    #  Почему встроенная в BoardPermissions проверка аутентефикации не проходит

    def get_queryset(self) -> QuerySet:
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardCreateView(CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated, BoardPermissions]
