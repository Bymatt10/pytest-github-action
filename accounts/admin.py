from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from unfold.forms import UserCreationForm, AdminPasswordChangeForm, UserChangeForm

# from .forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.register(ContentType)
admin.site.register(Permission)


class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "organization",
        "is_active",
        "last_login",
        "date_joined",
    )
    list_filter = ("is_active", "organization")
    search_fields = (
        "username",
        "first_name",
        "last_name",
    )
    ordering = ("-id",)

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_fullwidth = True
    readonly_fields = ["last_login", "date_joined"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "organization",
                    "first_name",
                    "last_name",
                    "email",
                    "photo",
                    "phone",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login", "date_joined"),
                "classes": ["tab"],
            },
        ),
    )

    compressed_fields = True
    show_full_result_count = False


admin.site.register(User, CustomUserAdmin)
