from django.contrib import admin
from unfold.admin import ModelAdmin

from organizations.models import Organization

@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ("name", "code", "location", "created")
    ordering = ["-id"]
    search_fields = ("name",)
    list_filter = ("location", )
    compressed_fields = True
