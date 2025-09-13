from django.contrib import admin
from unfold.admin import ModelAdmin

from locations.models import Location

@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ("name", "code", "created")
    ordering = ["-id"]
    search_fields = ("name",)
    compressed_fields = True
