from django.db import models
from django.utils.translation import gettext_lazy as _

LOCATION_TYPE_CHOICES = (
    (
        "country",
        _("country"),
    ),
    ("department", _("department")),
    ("municipality", _("municipality")),
    ("communnity", _("communnity")),
)


class Location(models.Model):
    name = models.CharField(_("name"), max_length=140)
    code = models.CharField(_("code"), max_length=140)
    location_type = models.CharField(
        _("location_type"),
        max_length=140,
        choices=LOCATION_TYPE_CHOICES,
        default="country",
    )
    parent = models.ForeignKey(
        "self", verbose_name=_("parent"), on_delete=models.SET_NULL, null=True
    )

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return self.name
