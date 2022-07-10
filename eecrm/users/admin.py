# import the logging library
import logging
from datetime import datetime
from django.contrib import admin
from django.contrib.admin.models import LogEntry

# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

import base.constants as cts
from .forms import CustomUserCreationForm
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    model = User
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "department",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    fieldsets = (
        ("Identity", {"fields": ("username", "password", "first_name", "last_name", "email")}),
        (
            "Roles",
            {
                "fields": (
                    "department",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            },
        ),
        ("Dates", {"fields": ("date_created", "date_updated", "last_login")}),
    )
    readonly_fields = ("date_created", "date_updated", "last_login")
    list_filter = ("department", "is_active")

    def has_view_or_change_permission(self, request, obj=None):
        # # # let superuser be superuser == have full access as well as managment
        if request.user.is_superuser:
            return True
        # # get the request user department
        user_employee = User.objects.get(id=request.user.id)
        user_role = user_employee.department
        # get User model permissions
        content_type = ContentType.objects.get_for_model(User)
        user_model_permission = Permission.objects.filter(content_type=content_type)
        # # authorise section
        if user_role == "M":
            # To add permissions
            for perm in user_model_permission:
                user_employee.user_permissions.add(perm)
                logger.info(
                    f"[{datetime.now()}]: Admin site {user_employee} had {perm} checked by {request.user.username}"
                )
            return True

        return False

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        logger.info(f"[{datetime.now()}]: User.Create|Update {obj.username} by {request.user.username}")
        super().save_model(request, obj, form, change)


# admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.site_header = cts.ADMIN_SITE_HEADER
admin.site.site_title = cts.ADMIN_SITE_TITLE
admin.site.index_title = cts.ADMIN_SITE_INDEX_TITLE
admin.site.site_url = None
if False:
    print_perm()


# LogEntry settings (c) malikalbeik @/blog/monitoring-user-actions-with-logentry-in-django-ad
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"
    # to filter the results
    list_filter = ["user", "content_type", "action_flag"]
    # when searching the user will be able to search in both object_repr and change_message
    search_fields = ["object_repr", "change_message"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "action_flag",
    ]
    # only superuser can read the history
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        # return request.user.is_superuser
        return True
