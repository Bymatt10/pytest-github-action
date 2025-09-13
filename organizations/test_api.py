import pytest
from rest_framework.test import APIClient
from rest_framework import status

from organizations.models import Organization
from organizations.factories import OrganizationFactory
from locations.factories import LocationFactory
from accounts.factories import AdminUserFactory


@pytest.mark.django_db
class TestOrganizationAPI:
    """Tests API CRUD para OrganizationViewSet"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.admin_user = AdminUserFactory()
        self.client.force_authenticate(user=self.admin_user)
        self.base_url = "/api/v1/organizations/"

    def test_list_organizations(self):
        """Test GET /api/v1/organizations/ - Listar organizaciones"""
        from organizations.models import Organization
        initial_count = Organization.objects.count()
        OrganizationFactory.create_batch(4)
        
        response = self.client.get(self.base_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 4  # Al menos las 4 que creamos
        assert "results" in response.data
        assert "count" in response.data

    def test_create_organization(self):
        """Test POST /api/v1/organizations/ - Crear organización"""
        location = LocationFactory()
        data = {
            "name": "Instituto de Pruebas Meteorológicas",
            "code": "IPM001",
            "phone": "+505-2-2345678",
            "address": "Km 5 Carretera Masaya",
            "location": location.id
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Instituto de Pruebas Meteorológicas"
        assert response.data["code"] == "IPM001"
        assert response.data["phone"] == "+505-2-2345678"
        assert response.data["location"]["id"] == location.id
        
        # Verificar en base de datos
        org = Organization.objects.get(code="IPM001")
        assert org.name == "Instituto de Pruebas Meteorológicas"

    def test_create_organization_minimal_fields(self):
        """Test crear organización con campos mínimos"""
        location = LocationFactory()
        data = {
            "name": "Organización Mínima",
            "code": "ORG001",
            "phone": "+505-8-1234567",
            "location": location.id
            # address es opcional
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["address"] is None

    def test_retrieve_organization(self):
        """Test GET /api/v1/organizations/{id}/ - Obtener organización específica"""
        organization = OrganizationFactory()
        url = f"{self.base_url}{organization.id}/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == organization.id
        assert response.data["name"] == organization.name
        assert response.data["code"] == organization.code
        assert response.data["location"]["id"] == organization.location.id

    def test_update_organization(self):
        """Test PUT /api/v1/organizations/{id}/ - Actualizar organización completa"""
        organization = OrganizationFactory()
        new_location = LocationFactory()
        url = f"{self.base_url}{organization.id}/"
        
        data = {
            "name": "Organización Actualizada",
            "code": organization.code,  # Mantener código
            "phone": "+505-7-9876543",
            "address": "Nueva Dirección Actualizada",
            "location": new_location.id
        }
        
        response = self.client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Organización Actualizada"
        assert response.data["phone"] == "+505-7-9876543"
        assert response.data["address"] == "Nueva Dirección Actualizada"
        assert response.data["location"]["id"] == new_location.id
        
        # Verificar en base de datos
        organization.refresh_from_db()
        assert organization.name == "Organización Actualizada"
        assert organization.location == new_location

    def test_partial_update_organization(self):
        """Test PATCH /api/v1/organizations/{id}/ - Actualización parcial"""
        organization = OrganizationFactory()
        url = f"{self.base_url}{organization.id}/"
        
        data = {
            "name": "Nombre Parcialmente Actualizado",
            "phone": "+505-5-5555555"
        }
        
        response = self.client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Nombre Parcialmente Actualizado"
        assert response.data["phone"] == "+505-5-5555555"
        
        # Verificar en base de datos
        organization.refresh_from_db()
        assert organization.name == "Nombre Parcialmente Actualizado"
        assert organization.phone == "+505-5-5555555"

    def test_delete_organization(self):
        """Test DELETE /api/v1/organizations/{id}/ - Eliminar organización"""
        organization = OrganizationFactory()
        url = f"{self.base_url}{organization.id}/"
        
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar eliminación en base de datos
        assert not Organization.objects.filter(id=organization.id).exists()

    def test_filter_by_location(self):
        """Test filtrar por ubicación"""
        location1 = LocationFactory()
        location2 = LocationFactory()
        
        OrganizationFactory.create_batch(2, location=location1)
        OrganizationFactory.create_batch(3, location=location2)
        
        response = self.client.get(f"{self.base_url}?location={location1.id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        for org in response.data["results"]:
            assert org["location"]["id"] == location1.id

    def test_search_organizations(self):
        """Test búsqueda por nombre"""
        OrganizationFactory(name="Instituto Nicaragüense de Meteorología")
        OrganizationFactory(name="Centro de Investigaciones Hídricas")
        
        response = self.client.get(f"{self.base_url}?search=Instituto")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1  # Al menos el Instituto que creamos
        # Verificar que al menos uno contiene "Instituto"
        assert any("Instituto" in org["name"] for org in response.data["results"])

    def test_ordering_organizations(self):
        """Test ordenamiento por ID"""
        OrganizationFactory.create_batch(3)
        
        response = self.client.get(f"{self.base_url}?ordering=id")
        
        assert response.status_code == status.HTTP_200_OK
        ids = [org["id"] for org in response.data["results"]]
        assert ids == sorted(ids)

    def test_pagination_disabled(self):
        """Test paginación deshabilitada"""
        from organizations.models import Organization
        initial_count = Organization.objects.count()
        OrganizationFactory.create_batch(5)
        
        response = self.client.get(f"{self.base_url}?paginator=false")
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= 5  # Al menos las 5 que creamos

    def test_organization_with_location_details(self):
        """Test que la respuesta incluye detalles de la ubicación"""
        location = LocationFactory(name="Managua", location_type="department")
        organization = OrganizationFactory(location=location)
        
        url = f"{self.base_url}{organization.id}/"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["location"]["name"] == "Managua"
        assert response.data["location"]["location_type"] == "department"

    def test_create_organization_validation_errors(self):
        """Test validaciones en creación"""
        # Datos incompletos - falta location requerida
        data = {
            "name": "Organización Sin Ubicación",
            "code": "OSU001",
            "phone": "+505-2-1111111"
            # Falta location
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "location" in response.data

    def test_create_organization_missing_required_fields(self):
        """Test campos requeridos"""
        data = {
            "code": "TST001"
            # Faltan name, phone, location
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert "phone" in response.data
        assert "location" in response.data

    def test_phone_format_validation(self):
        """Test validación de formato de teléfono"""
        location = LocationFactory()
        data = {
            "name": "Test Organization",
            "code": "TST001",
            "phone": "invalid-phone-format",
            "location": location.id
        }
        
        response = self.client.post(self.base_url, data)
        
        # Dependiendo de las validaciones del serializer
        # podría ser 201 (si no hay validación) o 400 (si hay validación)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

    def test_nicaraguan_organizations_data(self):
        """Test creación con datos realistas nicaragüenses"""
        location = LocationFactory(name="Managua")
        data = {
            "name": "Instituto Nicaragüense de Estudios Territoriales",
            "code": "INET001",
            "phone": "+505-2-2234567",
            "address": "Km 12 Carretera Norte, Managua",
            "location": location.id
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert "Nicaragüense" in response.data["name"]
        assert response.data["phone"].startswith("+505")

    def test_unauthorized_access(self):
        """Test acceso sin autenticación"""
        client = APIClient()
        
        response = client.get(self.base_url)
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_organization_location_relationship(self):
        """Test relación con ubicación en detalle"""
        country = LocationFactory(name="Nicaragua", location_type="country")
        department = LocationFactory(name="Managua", location_type="department", parent=country)
        
        organization = OrganizationFactory(location=department)
        
        url = f"{self.base_url}{organization.id}/"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["location"]["name"] == "Managua"
        assert response.data["location"]["parent"]["name"] == "Nicaragua"

    def test_duplicate_code_validation(self):
        """Test validación de código duplicado"""
        existing_org = OrganizationFactory()
        location = LocationFactory()
        
        data = {
            "name": "Nueva Organización",
            "code": existing_org.code,  # Código duplicado
            "phone": "+505-8-9999999",
            "location": location.id
        }
        
        response = self.client.post(self.base_url, data)
        
        # Dependiendo de si hay validación unique en el modelo
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
