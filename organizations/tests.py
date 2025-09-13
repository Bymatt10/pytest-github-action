import pytest

from organizations.models import Organization
from organizations.factories import OrganizationFactory
from locations.factories import LocationFactory


@pytest.mark.django_db
class TestOrganizationCRUD:
    """Tests CRUD para el modelo Organization"""

    def test_create_organization(self):
        """Test crear una organización"""
        organization = OrganizationFactory()

        assert organization.id is not None
        assert organization.name is not None
        assert len(organization.name) > 10  # Nombres realistas son más largos
        assert organization.code.startswith("ORG-")
        assert organization.phone.startswith("+505")
        assert organization.address is not None
        assert organization.location is not None
        assert organization.created is not None
        assert organization.modified is not None

    def test_create_organization_minimal_fields(self):
        """Test crear organización con campos mínimos requeridos"""
        location = LocationFactory()
        organization = Organization.objects.create(
            name="Test Organization",
            code="TST001",
            phone="+505-2-2345678",
            location=location
        )

        assert organization.id is not None
        assert organization.name == "Test Organization"
        assert organization.code == "TST001"
        assert organization.phone == "+505-2-2345678"
        assert organization.address is None  # Campo opcional
        assert organization.location == location

    def test_read_organization(self):
        """Test leer una organización"""
        organization = OrganizationFactory()
        retrieved_organization = Organization.objects.get(id=organization.id)

        assert retrieved_organization.id == organization.id
        assert retrieved_organization.name == organization.name
        assert retrieved_organization.code == organization.code
        assert retrieved_organization.phone == organization.phone
        assert retrieved_organization.address == organization.address
        assert retrieved_organization.location == organization.location

    def test_update_organization(self):
        """Test actualizar una organización"""
        organization = OrganizationFactory()
        original_name = organization.name
        original_modified = organization.modified

        # Actualizar la organización
        organization.name = "Updated Organization Name"
        organization.code = "UPD001"
        organization.phone = "+505-8-7654321"
        organization.address = "Updated Address"
        organization.save()

        # Verificar la actualización
        updated_organization = Organization.objects.get(id=organization.id)
        assert updated_organization.name == "Updated Organization Name"
        assert updated_organization.name != original_name
        assert updated_organization.code == "UPD001"
        assert updated_organization.phone == "+505-8-7654321"
        assert updated_organization.address == "Updated Address"
        assert updated_organization.modified > original_modified

    def test_delete_organization(self):
        """Test eliminar una organización"""
        organization = OrganizationFactory()
        organization_id = organization.id

        # Eliminar la organización
        organization.delete()

        # Verificar eliminación
        with pytest.raises(Organization.DoesNotExist):
            Organization.objects.get(id=organization_id)

    def test_organization_str_method(self):
        """Test método __str__ de la organización"""
        organization = OrganizationFactory(name="Test Organization Name")
        assert str(organization) == "Test Organization Name"

    def test_organization_with_location_relationship(self):
        """Test relación con Location"""
        location = LocationFactory()
        organization = OrganizationFactory(location=location)

        assert organization.location == location
        assert organization.location.id == location.id

    def test_organization_default_values(self):
        """Test valores por defecto del modelo"""
        location = LocationFactory()
        organization = Organization.objects.create(
            name="Basic Organization",
            code="BAS001",
            phone="+505-2-2000000",
            location=location
        )

        assert organization.address is None
        assert organization.created is not None
        assert organization.modified is not None
