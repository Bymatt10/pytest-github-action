from django.db import models

from django.contrib.auth.models import AbstractUser

from organizations.models import Organization

ROLE_CHOICES = (
    ("admin", "Admin"),
    ("observer", "Observador"),
)


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/", blank=True, null=True)
    phone = models.CharField(max_length=140, null=True, blank=True)

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    role = models.CharField(max_length=140, choices=ROLE_CHOICES, default="observer")

    firebase_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)

    # created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == "admin"
