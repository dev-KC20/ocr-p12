import base.constants as cts
from django.contrib import admin
from django.contrib.admin.models import ADDITION, LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Employee


class CustomEmployeeAdmin(UserAdmin):
    fieldsets = (
        ("Personal informations", {"fields": ("username", "password", "first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("department",)}),
        ("Date informations", {"fields": ("date_created", "date_updated", "last_login")}),
    )
    readonly_fields = ("date_created", "date_updated", "last_login")
    list_display = ("username", "first_name", "last_name", "email", "department")
    list_filter = ("department", "is_active")


admin.site.register(Employee, CustomEmployeeAdmin)
admin.site.unregister(Group)
admin.site.site_header = cts.ADMIN_SITE_HEADER
admin.site.site_title = cts.ADMIN_SITE_TITLE
admin.site.index_title = cts.ADMIN_SITE_INDEX_TITLE
LogEntry.objects.filter(action_flag=ADDITION)
