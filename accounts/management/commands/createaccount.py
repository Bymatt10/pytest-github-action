from django.core.management.base import BaseCommand

from locations.models import Location
from django.contrib.auth import get_user_model

from organizations.models import Organization

User = get_user_model()


class Command(BaseCommand):
    help = "Create an account"

    def handle(self, *args, **options):
        location = Location.objects.create(
            name="Nicaragua", code="NIC", location_type="country"
        )

        organization = Organization.objects.create(
            name="org test", code="org01", location=location
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

        self.stdout.write("Organization and users created")
