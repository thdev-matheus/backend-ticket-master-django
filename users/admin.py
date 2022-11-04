from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUser(UserAdmin):
    readonly_fields = (
        "date_joined",
        "last_login",
    )

    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("email", "department")},
        ),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
        ("Dates", {"fields": ("updated_at", "date_joined", "last_login")}),
    )


admin.site.register(User, CustomUser)
