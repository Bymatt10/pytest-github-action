import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.factories import UserFactory, AdminUserFactory, ObserverUserFactory
from organizations.factories import OrganizationFactory

User = get_user_model()


@pytest.mark.django_db
class TestAccountAPI:
    """Tests API CRUD para AccountViewSet"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.admin_user = AdminUserFactory()
        self.client.force_authenticate(user=self.admin_user)
        self.base_url = "/api/v1/accounts/"

    def test_list_accounts(self):
        """Test GET /api/v1/accounts/ - Listar usuarios"""
        # Crear algunos usuarios de prueba
        UserFactory.create_batch(3)
        
        response = self.client.get(self.base_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 4  # 3 + admin_user
        assert "results" in response.data
        assert "count" in response.data

    def test_create_account(self):
        """Test POST /api/v1/accounts/ - Crear usuario"""
        organization = OrganizationFactory()
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpassword123",
            "organization": organization.id,
            "role": "observer"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "newuser"
        assert response.data["email"] == "newuser@example.com"
        assert response.data["role"] == "observer"
        
        # Verificar que se creó en la base de datos
        user = User.objects.get(username="newuser")
        assert user.email == "newuser@example.com"
        assert user.check_password("newpassword123")

    def test_retrieve_account(self):
        """Test GET /api/v1/accounts/{id}/ - Obtener usuario específico"""
        user = UserFactory()
        url = f"{self.base_url}{user.id}/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user.id
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email

    def test_update_account(self):
        """Test PUT /api/v1/accounts/{id}/ - Actualizar usuario completo"""
        user = UserFactory()
        organization = OrganizationFactory()
        url = f"{self.base_url}{user.id}/"
        
        data = {
            "username": user.username,  # Requerido
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "organization": organization.id,
            "role": "admin"
        }
        
        response = self.client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "updated@example.com"
        assert response.data["first_name"] == "Updated"
        assert response.data["role"] == "admin"
        
        # Verificar en base de datos
        user.refresh_from_db()
        assert user.email == "updated@example.com"
        assert user.role == "admin"

    def test_partial_update_account(self):
        """Test PATCH /api/v1/accounts/{id}/ - Actualización parcial"""
        user = UserFactory()
        url = f"{self.base_url}{user.id}/"
        
        data = {
            "first_name": "Patched",
            "role": "admin"
        }
        
        response = self.client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Patched"
        assert response.data["role"] == "admin"
        
        # Verificar en base de datos
        user.refresh_from_db()
        assert user.first_name == "Patched"
        assert user.role == "admin"

    def test_delete_account(self):
        """Test DELETE /api/v1/accounts/{id}/ - Eliminar usuario"""
        user = UserFactory()
        url = f"{self.base_url}{user.id}/"
        
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar eliminación en base de datos
        assert not User.objects.filter(id=user.id).exists()

    def test_filter_accounts_by_role(self):
        """Test filtros - Filtrar por rol"""
        AdminUserFactory.create_batch(2)
        ObserverUserFactory.create_batch(3)
        
        # Filtrar solo admins
        response = self.client.get(f"{self.base_url}?role=admin")
        
        assert response.status_code == status.HTTP_200_OK
        # 2 creados + admin_user del setup = 3
        assert len(response.data["results"]) == 3
        for user in response.data["results"]:
            assert user["role"] == "admin"

    def test_search_accounts(self):
        """Test búsqueda por nombre de usuario"""
        UserFactory(username="searchable_user")
        UserFactory(username="another_user")
        
        response = self.client.get(f"{self.base_url}?search=searchable")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["username"] == "searchable_user"

    def test_ordering_accounts(self):
        """Test ordenamiento"""
        response = self.client.get(f"{self.base_url}?ordering=id")
        
        assert response.status_code == status.HTTP_200_OK
        # Verificar que están ordenados por ID
        ids = [user["id"] for user in response.data["results"]]
        assert ids == sorted(ids)

    def test_pagination_disabled(self):
        """Test paginación deshabilitada"""
        UserFactory.create_batch(5)
        
        response = self.client.get(f"{self.base_url}?paginator=false")
        
        assert response.status_code == status.HTTP_200_OK
        # Sin paginación, debería retornar lista directa
        assert isinstance(response.data, list)

    def test_me_action(self):
        """Test GET /api/v1/accounts/me/ - Obtener usuario actual"""
        url = f"{self.base_url}me/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == self.admin_user.id
        assert response.data["username"] == self.admin_user.username

    def test_contenttypes_action(self):
        """Test GET /api/v1/accounts/contenttypes/ - Obtener content types"""
        url = f"{self.base_url}contenttypes/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0

    def test_groups_action(self):
        """Test GET /api/v1/accounts/groups/ - Obtener grupos"""
        url = f"{self.base_url}groups/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_permissions_action(self):
        """Test GET /api/v1/accounts/permissions/ - Obtener permisos"""
        url = f"{self.base_url}permissions/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0

    def test_create_account_validation_errors(self):
        """Test validaciones en creación"""
        # Datos inválidos - username ya existe
        data = {
            "username": self.admin_user.username,  # Ya existe
            "email": "test@example.com",
            "password": "pass123"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_unauthorized_access(self):
        """Test acceso sin autenticación"""
        client = APIClient()  # Sin autenticar
        
        response = client.get(self.base_url)
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_filter_by_organization(self):
        """Test filtrar por organización"""
        org1 = OrganizationFactory()
        org2 = OrganizationFactory()
        
        UserFactory.create_batch(2, organization=org1)
        UserFactory.create_batch(3, organization=org2)
        
        response = self.client.get(f"{self.base_url}?organization={org1.id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        for user in response.data["results"]:
            assert user["organization"]["id"] == org1.id
