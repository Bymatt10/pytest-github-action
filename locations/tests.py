import pytest

from locations.models import Location
from locations.factories import LocationFactory


@pytest.mark.django_db
class TestLocationCRUD:
    """Tests CRUD para el modelo Location"""

    def test_create_location(self):
        """Test crear una ubicación"""
        location = LocationFactory()

        assert location.id is not None
        assert location.name is not None
        assert location.code.startswith("LOC-")
        assert location.location_type in ["country", "department", "municipality", "communnity"]
        assert location.parent is None
        assert location.created is not None
        assert location.modified is not None

    def test_create_location_minimal_fields(self):
        """Test crear ubicación con campos mínimos requeridos"""
        location = Location.objects.create(
            name="Test Location",
            code="TST001"
        )

        assert location.id is not None
        assert location.name == "Test Location"
        assert location.code == "TST001"
        assert location.location_type == "country"  # valor por defecto
        assert location.parent is None

    def test_create_location_with_parent(self):
        """Test crear ubicación con ubicación padre"""
        parent_location = LocationFactory(location_type="country")
        child_location = LocationFactory(
            location_type="department",
            parent=parent_location
        )

        assert child_location.parent == parent_location
        assert child_location.location_type == "department"

    def test_create_location_specific_type(self):
        """Test crear ubicación con tipo específico"""
        location = Location.objects.create(
            name="Managua",
            code="MGA001",
            location_type="department"
        )

        assert location.location_type == "department"
        assert location.name == "Managua"

    def test_read_location(self):
        """Test leer una ubicación"""
        location = LocationFactory()
        retrieved_location = Location.objects.get(id=location.id)

        assert retrieved_location.id == location.id
        assert retrieved_location.name == location.name
        assert retrieved_location.code == location.code
        assert retrieved_location.location_type == location.location_type
        assert retrieved_location.parent == location.parent

    def test_update_location(self):
        """Test actualizar una ubicación"""
        location = LocationFactory()
        original_name = location.name
        original_modified = location.modified

        # Actualizar la ubicación
        location.name = "Updated Location Name"
        location.code = "UPD001"
        location.location_type = "municipality"
        location.save()

        # Verificar la actualización
        updated_location = Location.objects.get(id=location.id)
        assert updated_location.name == "Updated Location Name"
        assert updated_location.name != original_name
        assert updated_location.code == "UPD001"
        assert updated_location.location_type == "municipality"
        assert updated_location.modified > original_modified

    def test_update_location_parent(self):
        """Test actualizar la ubicación padre"""
        parent_location = LocationFactory(location_type="country")
        child_location = LocationFactory(location_type="department")
        
        # Inicialmente sin padre
        assert child_location.parent is None
        
        # Asignar padre
        child_location.parent = parent_location
        child_location.save()
        
        # Verificar la actualización
        updated_location = Location.objects.get(id=child_location.id)
        assert updated_location.parent == parent_location

    def test_delete_location(self):
        """Test eliminar una ubicación"""
        location = LocationFactory()
        location_id = location.id

        # Eliminar la ubicación
        location.delete()

        # Verificar eliminación
        with pytest.raises(Location.DoesNotExist):
            Location.objects.get(id=location_id)

    def test_delete_parent_location_with_children(self):
        """Test eliminar ubicación padre que tiene hijos (SET_NULL)"""
        parent_location = LocationFactory(location_type="country")
        child_location = LocationFactory(
            location_type="department",
            parent=parent_location
        )
        child_id = child_location.id

        # Eliminar el padre
        parent_location.delete()

        # Verificar que el hijo sigue existiendo pero sin padre
        child_after_deletion = Location.objects.get(id=child_id)
        assert child_after_deletion.parent is None

    def test_location_str_method(self):
        """Test método __str__ del modelo"""
        location = Location.objects.create(
            name="Test Location",
            code="TST001"
        )

        assert str(location) == "Test Location"

    def test_location_type_choices(self):
        """Test que los tipos de ubicación están dentro de las opciones válidas"""
        valid_types = ["country", "department", "municipality", "communnity"]
        
        for location_type in valid_types:
            location = Location.objects.create(
                name=f"Test {location_type}",
                code=f"TST{location_type[:3].upper()}",
                location_type=location_type
            )
            assert location.location_type == location_type

    def test_location_hierarchy(self):
        """Test jerarquía de ubicaciones"""
        # Crear jerarquía: País -> Departamento -> Municipio -> Comunidad
        country = LocationFactory(
            name="Nicaragua",
            location_type="country",
            parent=None
        )
        
        department = LocationFactory(
            name="Managua",
            location_type="department",
            parent=country
        )
        
        municipality = LocationFactory(
            name="Managua Centro",
            location_type="municipality",
            parent=department
        )
        
        community = LocationFactory(
            name="Barrio Martha Quezada",
            location_type="communnity",
            parent=municipality
        )

        # Verificar jerarquía
        assert community.parent == municipality
        assert municipality.parent == department
        assert department.parent == country
        assert country.parent is None

    def test_location_default_values(self):
        """Test valores por defecto del modelo"""
        location = Location.objects.create(
            name="Test Default",
            code="DEFAULT001"
        )

        assert location.location_type == "country"  # valor por defecto
        assert location.parent is None
