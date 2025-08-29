import factory
from factory.django import DjangoModelFactory

from locations.factories import LocationFactory
from organizations.models import Organization


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"Organization {n}")
    code = factory.Sequence(lambda n: f"ORG{n:03d}")
    phone = factory.Sequence(lambda n: f"+591{n:08d}")
    address = factory.Faker("address")
    location = factory.SubFactory(LocationFactory)
