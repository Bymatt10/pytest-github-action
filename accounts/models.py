from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser

from organizations.models import Organization

ROLE_CHOICES = (
    (
        "admin",
        _("admin"),
    ),
    ("observer", _("observer")),
)


class User(AbstractUser):
    photo = models.ImageField(_("photo"), upload_to="users/", blank=True, null=True)
    phone = models.CharField(_("phone"), max_length=140, null=True, blank=True)

    organization = models.ForeignKey(
        Organization, verbose_name=_("organization"), on_delete=models.PROTECT
    )

    role = models.CharField(
        _("role"), max_length=140, choices=ROLE_CHOICES, default="observer"
    )

    firebase_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)

    # created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == "admin"
