from django.db import transaction
from rest_framework import serializers

from core.models import User
from core.serializers import ProfileInfoSerializer
from goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    If BoardParticipant.Role is the owner or writer it creates the category
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"

    def create(self, validated_data: dict) -> GoalCategory:
        user = validated_data.get("user")
        board = validated_data.get("board")
        if BoardParticipant.objects.filter(user=user, board=board,
                                           role__in=[BoardParticipant.Role.owner,
                                                     BoardParticipant.Role.writer]):
            category = GoalCategory.objects.create(**validated_data)
            return category
        else:
            raise serializers.ValidationError({"board": "PERMISSION DENIED! You dont have enough rights to create"
                                                        " category in board with this id"}, code=403)


class GoalCategorySerializer(serializers.ModelSerializer):
    """
    Default serializer with serialized user field
    """
    user = ProfileInfoSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


class GoalCreateSerializer(serializers.ModelSerializer):
    """
    If BoardParticipant.Role is owner or writer of Goal.category
    and Goal.category.is_deleted is False, it creates goal
    else raises ValidationError
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"

    @staticmethod
    def validate_category(value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        return value

    def create(self, validated_data: dict) -> Goal:
        user = validated_data.get("user")
        category = validated_data.get("category")
        board = GoalCategory.objects.get(pk=category.id).board

        if BoardParticipant.objects.filter(user=user, board=board,
                                           role__in=[BoardParticipant.Role.owner,
                                                     BoardParticipant.Role.writer]):
            goal = Goal.objects.create(**validated_data)
            return goal

        else:
            raise serializers.ValidationError({"category": "PERMISSION DENIED! You dont have enough rights to create"
                                                           " goal in category with this id"}, code=403)


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """
    If BoardParticipant.Role is owner or writer of Comment.goal.category it creates goal
    else raises ValidationError
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data: dict) -> GoalComment:  # TODO переделать это нормально и во вьюшках queryset тоже
        user = validated_data.get("user")
        goal = validated_data.get("goal")

        category = Goal.objects.get(pk=goal.id).category
        board = GoalCategory.objects.get(pk=category.id).board

        if BoardParticipant.objects.filter(user=user, board=board,
                                           role__in=[BoardParticipant.Role.owner,
                                                     BoardParticipant.Role.writer]):
            comment = GoalComment.objects.create(**validated_data)
            return comment
        else:
            raise serializers.ValidationError({"goal": "PERMISSION DENIED! You dont have enough rights to create"
                                                       " comment in goal with this id"}, code=403)


class GoalCommentSerializer(serializers.ModelSerializer):
    """Default serializer with serialized user field"""
    user = ProfileInfoSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")


class BoardCreateSerializer(serializers.ModelSerializer):
    """Creates Board obj and BoardParticipant obj with given user, board and Role.owner"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"

    def create(self, validated_data: dict) -> Board:
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    """
    Default serializer with user saving by user.username
    and checking if the role belongs to BoardParticipant.Role check
    """
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    """
    The custom update method makes possible to add new users to an existing board
    """
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance: Board, validated_data: dict) -> Board:
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()
        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
