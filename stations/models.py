from django.db import models

from organizations.models import Organization


class Station(models.Model):
    name = models.CharField(max_length=140)
    code = models.CharField(max_length=140)

    latitude = models.CharField(max_length=140, null=True, blank=True)
    longitude = models.CharField(max_length=140, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EquipmentStation(models.Model):
    name = models.CharField(max_length=140)
    code = models.CharField(max_length=140)
    brand = models.CharField(max_length=140, null=True, blank=True)
    model = models.CharField(max_length=140, null=True, blank=True)

    station = models.ForeignKey(Station, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RainfallStation(models.Model):
    station = models.ForeignKey(Station, on_delete=models.PROTECT)
    registration_date = models.DateField()

    day = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.station.name
