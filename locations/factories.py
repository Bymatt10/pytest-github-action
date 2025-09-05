import factory
from factory.django import DjangoModelFactory

from locations.models import Location, LOCATION_TYPE_CHOICES


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Faker(
        "random_element",
        elements=(
            "Nicaragua",
            "Managua",
            "León",
            "Granada",
            "Masaya",
            "Chinandega",
            "Estelí",
            "Matagalpa",
            "Jinotega",
            "Nueva Segovia",
            "Madriz",
            "Boaco",
            "Chontales",
            "Río San Juan",
            "Rivas",
            "Carazo",
            "RACCS",
            "RACCN",
        )
    )
    
    code = factory.Sequence(lambda n: f"LOC-{n:04d}")
    
    location_type = factory.Faker(
        "random_element", 
        elements=[choice[0] for choice in LOCATION_TYPE_CHOICES]
    )
    
    parent = None  # Por defecto sin padre, se puede sobrescribir en tests específicos