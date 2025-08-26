from django.db import models

from locations.models import Location


class Organization(models.Model):
    name = models.CharField(max_length=140)
    code = models.CharField(max_length=140)
    phone = models.CharField(max_length=140)
    address = models.TextField(null=True, blank=True)

    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
