from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User

# from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("photo", "organization", "role", "phone")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("photo", "organization", "role", "phone")}),
    )

    # form = CustomUserChangeForm
    # add_form = CustomUserCreationForm

    # Optionally, customize list_display, list_filter, etc.
    # list_display = ('username', 'email', 'your_custom_field1', 'is_staff')


admin.site.register(User, CustomUserAdmin)
