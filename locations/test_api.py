import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from locations.models import Location
from locations.factories import LocationFactory
from accounts.factories import AdminUserFactory


@pytest.mark.django_db
class TestLocationAPI:
    """Tests API CRUD para LocationViewSet"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.admin_user = AdminUserFactory()
        self.client.force_authenticate(user=self.admin_user)
        self.base_url = "/api/v1/locations/"

    def test_list_locations(self):
        """Test GET /api/v1/locations/ - Listar ubicaciones"""
        LocationFactory.create_batch(5)
        
        response = self.client.get(self.base_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 5
        assert "results" in response.data
        assert "count" in response.data

    def test_create_location(self):
        """Test POST /api/v1/locations/ - Crear ubicación"""
        data = {
            "name": "Nueva Ubicación",
            "code": "NUB001",
            "location_type": "department"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Nueva Ubicación"
        assert response.data["code"] == "NUB001"
        assert response.data["location_type"] == "department"
        
        # Verificar en base de datos
        location = Location.objects.get(code="NUB001")
        assert location.name == "Nueva Ubicación"

    def test_create_location_with_parent(self):
        """Test crear ubicación con padre"""
        parent = LocationFactory(location_type="country")
        data = {
            "name": "Departamento Hijo",
            "code": "DEP001",
            "location_type": "department",
            "parent": parent.id
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["parent"]["id"] == parent.id
        
        # Verificar en base de datos
        location = Location.objects.get(code="DEP001")
        assert location.parent == parent

    def test_retrieve_location(self):
        """Test GET /api/v1/locations/{id}/ - Obtener ubicación específica"""
        location = LocationFactory()
        url = f"{self.base_url}{location.id}/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == location.id
        assert response.data["name"] == location.name
        assert response.data["code"] == location.code

    def test_update_location(self):
        """Test PUT /api/v1/locations/{id}/ - Actualizar ubicación completa"""
        location = LocationFactory()
        url = f"{self.base_url}{location.id}/"
        
        data = {
            "name": "Ubicación Actualizada",
            "code": location.code,  # Mantener código
            "location_type": "municipality"
        }
        
        response = self.client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Ubicación Actualizada"
        assert response.data["location_type"] == "municipality"
        
        # Verificar en base de datos
        location.refresh_from_db()
        assert location.name == "Ubicación Actualizada"
        assert location.location_type == "municipality"

    def test_partial_update_location(self):
        """Test PATCH /api/v1/locations/{id}/ - Actualización parcial"""
        location = LocationFactory()
        url = f"{self.base_url}{location.id}/"
        
        data = {
            "name": "Nombre Parcial"
        }
        
        response = self.client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Nombre Parcial"
        
        # Verificar en base de datos
        location.refresh_from_db()
        assert location.name == "Nombre Parcial"

    def test_delete_location(self):
        """Test DELETE /api/v1/locations/{id}/ - Eliminar ubicación"""
        location = LocationFactory()
        url = f"{self.base_url}{location.id}/"
        
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar eliminación en base de datos
        assert not Location.objects.filter(id=location.id).exists()

    def test_delete_location_with_children(self):
        """Test eliminar ubicación padre (debería actualizar hijos a parent=null)"""
        parent = LocationFactory(location_type="country")
        child = LocationFactory(location_type="department", parent=parent)
        url = f"{self.base_url}{parent.id}/"
        
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que el hijo queda huérfano
        child.refresh_from_db()
        assert child.parent is None

    def test_filter_by_location_type(self):
        """Test filtrar por tipo de ubicación"""
        LocationFactory.create_batch(2, location_type="country")
        LocationFactory.create_batch(3, location_type="department")
        
        response = self.client.get(f"{self.base_url}?location_type=country")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        for location in response.data["results"]:
            assert location["location_type"] == "country"

    def test_search_locations(self):
        """Test búsqueda por nombre"""
        LocationFactory(name="Managua Centro")
        LocationFactory(name="León Norte")
        
        response = self.client.get(f"{self.base_url}?search=Managua")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert "Managua" in response.data["results"][0]["name"]

    def test_ordering_locations(self):
        """Test ordenamiento por ID"""
        LocationFactory.create_batch(3)
        
        response = self.client.get(f"{self.base_url}?ordering=id")
        
        assert response.status_code == status.HTTP_200_OK
        ids = [loc["id"] for loc in response.data["results"]]
        assert ids == sorted(ids)

    def test_pagination_disabled(self):
        """Test paginación deshabilitada"""
        LocationFactory.create_batch(5)
        
        response = self.client.get(f"{self.base_url}?paginator=false")
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 5

    def test_location_hierarchy_in_response(self):
        """Test que la respuesta incluye información de jerarquía"""
        parent = LocationFactory(name="Nicaragua", location_type="country")
        child = LocationFactory(name="Managua", location_type="department", parent=parent)
        
        url = f"{self.base_url}{child.id}/"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["parent"]["name"] == "Nicaragua"
        assert response.data["parent"]["id"] == parent.id

    def test_create_location_validation_errors(self):
        """Test validaciones en creación"""
        # Crear ubicación con tipo inválido
        data = {
            "name": "Test Location",
            "code": "TST001",
            "location_type": "invalid_type"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "location_type" in response.data

    def test_create_location_missing_required_fields(self):
        """Test campos requeridos"""
        data = {
            "location_type": "country"
            # Faltan name y code
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert "code" in response.data

    def test_location_types_choices(self):
        """Test todos los tipos de ubicación válidos"""
        valid_types = ["country", "department", "municipality", "communnity"]
        
        for location_type in valid_types:
            data = {
                "name": f"Test {location_type}",
                "code": f"T{location_type[:3].upper()}",
                "location_type": location_type
            }
            
            response = self.client.post(self.base_url, data)
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data["location_type"] == location_type

    def test_unauthorized_access(self):
        """Test acceso sin autenticación"""
        client = APIClient()
        
        response = client.get(self.base_url)
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_nested_hierarchy_creation(self):
        """Test creación de jerarquía completa"""
        # País
        country_data = {
            "name": "Nicaragua",
            "code": "NIC001",
            "location_type": "country"
        }
        country_response = self.client.post(self.base_url, country_data)
        country_id = country_response.data["id"]
        
        # Departamento
        dept_data = {
            "name": "Managua",
            "code": "MGA001",
            "location_type": "department",
            "parent": country_id
        }
        dept_response = self.client.post(self.base_url, dept_data)
        dept_id = dept_response.data["id"]
        
        # Municipio
        muni_data = {
            "name": "Managua Centro",
            "code": "MGC001",
            "location_type": "municipality",
            "parent": dept_id
        }
        muni_response = self.client.post(self.base_url, muni_data)
        
        assert country_response.status_code == status.HTTP_201_CREATED
        assert dept_response.status_code == status.HTTP_201_CREATED
        assert muni_response.status_code == status.HTTP_201_CREATED
        
        # Verificar jerarquía
        assert muni_response.data["parent"]["id"] == dept_id
        assert dept_response.data["parent"]["id"] == country_id
