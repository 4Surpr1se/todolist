from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):
    """created: using auto_now_add renders the field un-editable in the admin
     that's why more preferred way is define it by our own
     updated: using whenever any changes with object happens"""

    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Board(DatesModelMixin):
    """Board model"""

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title


class GoalCategory(DatesModelMixin):
    """GoalCategory model"""

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT,
                              related_name="categories")

    def __str__(self):
        return self.title


class Status(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(DatesModelMixin):
    """Goal model with choices fields status and priority"""

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, null=True)
    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.CharField(verbose_name="Описание", max_length=255)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    due_date = models.DateField(verbose_name="Дедлайн", blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )

    def __str__(self):
        return self.title


class GoalComment(DatesModelMixin):

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Название", default='Описание')

    def __str__(self):
        return self.text


class BoardParticipant(DatesModelMixin):
    """model for OneToOne relation between Board and User
     with CRUD permissions for Board model"""
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )
