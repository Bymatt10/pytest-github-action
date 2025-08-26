from django.db import models

from stations.models import Station


class RainfallHistory(models.Model):
    station = models.ForeignKey(Station, on_delete=models.PROTECT)
    month = models.IntegerField(default=0)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.month
