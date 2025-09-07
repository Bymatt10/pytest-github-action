from django.db import models
from django.utils.translation import gettext_lazy as _

from stations.models import Station


class RainfallHistory(models.Model):
    station = models.ForeignKey(
        Station, verbose_name=_("station"), on_delete=models.PROTECT
    )
    month = models.IntegerField(_("month"), default=0)
    value = models.DecimalField(
        _("value"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("historical")
        verbose_name_plural = _("historical")

    def __str__(self):
        return str(self.month)
