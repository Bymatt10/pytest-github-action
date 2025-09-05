import factory
from factory.django import DjangoModelFactory

from histories.models import RainfallHistory
from stations.factories import StationFactory


class RainfallHistoryFactory(DjangoModelFactory):
    class Meta:
        model = RainfallHistory

    station = factory.SubFactory(StationFactory)
    month = factory.Faker("random_int", min=1, max=12)
    value = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
