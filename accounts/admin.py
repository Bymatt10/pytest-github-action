from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

# from .forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.register(ContentType)
admin.site.register(Permission)


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
