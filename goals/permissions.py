from django.http import HttpRequest
from django.views import View
from rest_framework import permissions

from goals.models import BoardParticipant, Board


class BoardPermissions(permissions.BasePermission):
    """
    if unauthenticated returns False
    if method in ('GET', 'HEAD', 'OPTIONS')
    checking belonging to BoardParticipant, returns True if it does, otherwise False
    If method NOT in ('GET', 'HEAD', 'OPTIONS')
    checking belonging to BoardParticipant AND BoardParticipant.Role == owner
    """
    def has_object_permission(self, request: HttpRequest, view: View, obj: Board) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()
#
