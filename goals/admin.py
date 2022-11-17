from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated")
    search_fields = ("title", )


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("text", "created", "updated")
    search_fields = ("text", )


class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated")
    search_fields = ("title", )
    readonly_fields = ('id',)


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "board")
    search_fields = ("board", )


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
