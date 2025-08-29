import factory
from factory.django import DjangoModelFactory

from organizations.factories import OrganizationFactory
from stations.models import Station, EquipmentStation, RainfallStation


class StationFactory(DjangoModelFactory):
    class Meta:
        model = Station

    name = factory.Sequence(lambda n: f"Station {n}")
    code = factory.Sequence(lambda n: f"STA{n:03d}")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    address = factory.Faker("address")
    organization = factory.SubFactory(OrganizationFactory)


class EquipmentStationFactory(DjangoModelFactory):
    class Meta:
        model = EquipmentStation

    name = factory.Sequence(lambda n: f"Equipment {n}")
    code = factory.Sequence(lambda n: f"EQP{n:03d}")
    brand = factory.Faker("company")
    model = factory.Faker("word")
    station = factory.SubFactory(StationFactory)


class RainfallStationFactory(DjangoModelFactory):
    class Meta:
        model = RainfallStation

    station = factory.SubFactory(StationFactory)
    registration_date = factory.Faker("date_object")
    day = factory.Faker("random_int", min=1, max=31)
    month = factory.Faker("random_int", min=1, max=12)
    year = factory.Faker("random_int", min=2020, max=2024)
    value = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
