from django.core.management.base import BaseCommand

from locations.models import Location
from django.contrib.auth import get_user_model

from organizations.models import Organization
from stations.models import Station

User = get_user_model()


class Command(BaseCommand):
    help = "Create an account"

    def handle(self, *args, **options):
        location = Location.objects.create(
            name="default", code="def01", location_type="country"
        )
        location2 =Location.objects.create(
            name="default2", code="def02", location_type="country"
        )

        organization = Organization.objects.create(
            name="default", code="org01", location=location
        )
        organization2 =Organization.objects.create(
            name="default2", code="org02", location=location2
        )

        Station.objects.create(
            name="default", code="sta01", organization=organization
        )
        Station.objects.create(
            name="default2", code="sta02", organization=organization2
        )

        User.objects.create_superuser(
            "admin",
            "admin@local.com",
            "endurance",
            first_name="admin",
            last_name="admin",
            organization=organization,
            role="admin",
        )

        # User.objects.create_user(
        #     "coach",
        #     "coach@afit.com",
        #     "demodemo25",
        #     first_name="coach",
        #     last_name="demo",
        #     company=model,
        #     role="coach",
        # )

        self.stdout.write("user admin created")
