from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse

import base.constants as cts
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):

    add_form = [CustomUserCreationForm, CustomUserChangeForm]

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
    list_filter = ("department", "is_active")


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.site_header = cts.ADMIN_SITE_HEADER
admin.site.site_title = cts.ADMIN_SITE_TITLE
admin.site.index_title = cts.ADMIN_SITE_INDEX_TITLE
# LogEntry.objects.filter(action_flag=ADDITION)
