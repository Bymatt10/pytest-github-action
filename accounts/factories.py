import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

from organizations.factories import OrganizationFactory
from accounts.models import ROLE_CHOICES

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    
    phone = factory.Faker(
        "random_element",
        elements=(
            "+505-2-2234567",
            "+505-2-2445678",
            "+505-8-8234567",
            "+505-8-7345678",
            "+505-5-5234567",
            "+505-7-7456789",
            "+505-2-2334455",
            "+505-2-2567890",
        )
    )
    
    organization = factory.SubFactory(OrganizationFactory)
    
    role = factory.Faker(
        "random_element", 
        elements=[choice[0] for choice in ROLE_CHOICES]
    )
    
    firebase_uid = factory.Faker("uuid4")
    
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        """Set a default password for the user."""
        if not create:
            return
        
        password = extracted if extracted else "testpass123"
        obj.set_password(password)
        obj.save()


class AdminUserFactory(UserFactory):
    """Factory for admin users"""
    role = "admin"
    is_staff = True
    is_superuser = True


class ObserverUserFactory(UserFactory):
    """Factory for observer users"""
    role = "observer"
