from django.contrib import admin

from core.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'last_login')
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(User, UserAdmin)
