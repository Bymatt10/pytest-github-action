import factory
from factory.django import DjangoModelFactory

from locations.models import Location


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Sequence(lambda n: f"Location {n}")
    code = factory.Sequence(lambda n: f"LOC{n:03d}")
    location_type = "municipality"
    parent = None
