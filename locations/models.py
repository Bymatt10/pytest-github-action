from django.db import models

LOCATION_TYPE_CHOICES = (
    ("country", "País"),
    ("department", "Departamento"),
    ("municipality", "Municipio"),
    ("communnity", "Comunidad"),
)


class Location(models.Model):
    name = models.CharField(max_length=140)
    code = models.CharField(max_length=140)
    location_type = models.CharField(
        max_length=140, choices=LOCATION_TYPE_CHOICES, default="country"
    )
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
