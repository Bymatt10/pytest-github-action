from django.db import models

from locations.models import Location
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    name = models.CharField(_("name"), max_length=140)
    code = models.CharField(_("code"), max_length=140)
    phone = models.CharField(_("phone"), max_length=140, null=True, blank=True)
    address = models.TextField(_("address"), null=True, blank=True)

    location = models.ForeignKey(
        Location, verbose_name=_("location"), on_delete=models.PROTECT
    )

    created = models.DateTimeField(_("address"), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __str__(self):
        return self.name
