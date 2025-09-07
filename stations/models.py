from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from organizations.models import Organization


class Station(models.Model):
    name = models.CharField(_("name"), max_length=140)
    code = models.CharField(_("code"), max_length=140)

    latitude = models.CharField(_("latitude"), max_length=140, null=True, blank=True)
    longitude = models.CharField(_("longitude"), max_length=140, null=True, blank=True)
    address = models.TextField(_("address"), null=True, blank=True)

    organization = models.ForeignKey(
        Organization, verbose_name=_("organization"), on_delete=models.PROTECT
    )

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("station")
        verbose_name_plural = _("stations")

    def __str__(self):
        return self.name


class EquipmentStation(models.Model):
    name = models.CharField(_("name"), max_length=140)
    code = models.CharField(_("code"), max_length=140)
    brand = models.CharField(_("brand"), max_length=140, null=True, blank=True)
    model = models.CharField(_("model"), max_length=140, null=True, blank=True)

    station = models.ForeignKey(
        Station, verbose_name=_("station"), on_delete=models.PROTECT
    )

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("equipment")
        verbose_name_plural = _("equipments")

    def __str__(self):
        return self.name


class RainfallStation(models.Model):
    station = models.ForeignKey(
        Station, verbose_name=_("station"), on_delete=models.PROTECT
    )
    registration_date = models.DateField(
        _("registration_date"),
    )

    day = models.IntegerField(_("day"), default=0)
    month = models.IntegerField(_("month"), default=0)
    year = models.IntegerField(_("year"), default=0)
    value = models.DecimalField(
        _("value"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("rainfall")
        verbose_name_plural = _("rainfalls")

    def __str__(self):
        return self.station.name

    def save(self, *args, **kwargs):
        self.day = self.registration_date.day
        self.month = self.registration_date.month
        self.year = self.registration_date.year

        super().save(*args, **kwargs)
