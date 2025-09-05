import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.factories import UserFactory, AdminUserFactory, ObserverUserFactory
from organizations.factories import OrganizationFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserCRUD:
    """Tests CRUD para el modelo User"""

    def test_create_user(self):
        """Test crear un usuario"""
        user = UserFactory()

        assert user.id is not None
        assert user.username.startswith("user")
        assert "@" in user.email
        assert user.first_name is not None
        assert user.last_name is not None
        assert user.organization is not None
        assert user.role in ["admin", "observer"]
        assert user.is_active is True
        assert user.modified is not None
        assert user.check_password("testpass123")

    def test_create_user_minimal_fields(self):
        """Test crear usuario con campos mínimos requeridos"""
        organization = OrganizationFactory()
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            organization=organization
        )

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.organization == organization
        assert user.role == "observer"  # valor por defecto
        assert user.phone is None
        assert user.firebase_uid is None
        assert user.check_password("testpass123")

    def test_create_admin_user(self):
        """Test crear usuario administrador"""
        admin_user = AdminUserFactory()

        assert admin_user.role == "admin"
        assert admin_user.is_admin is True
        assert admin_user.is_staff is True

    def test_create_observer_user(self):
        """Test crear usuario observador"""
        observer_user = ObserverUserFactory()

        assert observer_user.role == "observer"
        assert observer_user.is_admin is False
        assert observer_user.is_staff is False

    def test_create_user_with_custom_password(self):
        """Test crear usuario con contraseña personalizada"""
        user = UserFactory(password="custompass456")

        assert user.check_password("custompass456")
        assert not user.check_password("testpass123")

    def test_read_user(self):
        """Test leer un usuario"""
        user = UserFactory()
        retrieved_user = User.objects.get(id=user.id)

        assert retrieved_user.id == user.id
        assert retrieved_user.username == user.username
        assert retrieved_user.email == user.email
        assert retrieved_user.organization == user.organization
        assert retrieved_user.role == user.role

    def test_update_user(self):
        """Test actualizar un usuario"""
        user = UserFactory()
        original_username = user.username
        original_modified = user.modified

        # Actualizar el usuario
        user.username = "updated_user"
        user.first_name = "Updated"
        user.last_name = "Name"
        user.phone = "+505-8-9999999"
        user.role = "admin"
        user.save()

        # Verificar la actualización
        updated_user = User.objects.get(id=user.id)
        assert updated_user.username == "updated_user"
        assert updated_user.username != original_username
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.phone == "+505-8-9999999"
        assert updated_user.role == "admin"
        assert updated_user.modified > original_modified

    def test_update_user_password(self):
        """Test actualizar contraseña de usuario"""
        user = UserFactory()
        
        # Cambiar contraseña
        user.set_password("newpassword123")
        user.save()

        # Verificar nueva contraseña
        updated_user = User.objects.get(id=user.id)
        assert updated_user.check_password("newpassword123")
        assert not updated_user.check_password("testpass123")

    def test_delete_user(self):
        """Test eliminar un usuario"""
        user = UserFactory()
        user_id = user.id

        # Eliminar el usuario
        user.delete()

        # Verificar eliminación
        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=user_id)

    def test_user_str_method(self):
        """Test método __str__ del modelo"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            organization=OrganizationFactory()
        )

        assert str(user) == "testuser"

    def test_user_is_admin_property(self):
        """Test propiedad is_admin"""
        admin_user = UserFactory(role="admin")
        observer_user = UserFactory(role="observer")

        assert admin_user.is_admin is True
        assert observer_user.is_admin is False

    def test_user_role_choices(self):
        """Test que los roles están dentro de las opciones válidas"""
        valid_roles = ["admin", "observer"]
        
        for role in valid_roles:
            user = UserFactory(role=role)
            assert user.role == role

    def test_user_organization_relationship(self):
        """Test relación con organización"""
        organization = OrganizationFactory()
        user = UserFactory(organization=organization)

        assert user.organization == organization
        assert user.organization.name is not None

    def test_user_firebase_uid_unique(self):
        """Test que firebase_uid es único"""
        firebase_uid = "unique_firebase_uid_123"
        user1 = UserFactory(firebase_uid=firebase_uid)
        
        # Intentar crear otro usuario con el mismo firebase_uid
        with pytest.raises(IntegrityError):
            UserFactory(firebase_uid=firebase_uid)

    def test_user_firebase_uid_nullable(self):
        """Test que firebase_uid puede ser nulo"""
        user1 = UserFactory(firebase_uid=None)
        user2 = UserFactory(firebase_uid=None)
        
        assert user1.firebase_uid is None
        assert user2.firebase_uid is None
        # Ambos pueden tener firebase_uid nulo sin conflicto

    def test_user_default_values(self):
        """Test valores por defecto del modelo"""
        organization = OrganizationFactory()
        user = User.objects.create_user(
            username="defaultuser",
            email="default@example.com",
            password="testpass123",
            organization=organization
        )

        assert user.role == "observer"  # valor por defecto
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.phone is None
        assert user.firebase_uid is None

    def test_user_organization_protect_constraint(self):
        """Test que no se puede eliminar organización si tiene usuarios"""
        organization = OrganizationFactory()
        user = UserFactory(organization=organization)
        
        # Intentar eliminar la organización debería fallar por PROTECT
        with pytest.raises(Exception):  # ProtectedError en Django
            organization.delete()
        
        # Verificar que tanto el usuario como la organización siguen existiendo
        assert User.objects.filter(id=user.id).exists()
        assert organization.__class__.objects.filter(id=organization.id).exists()

    def test_create_superuser_equivalent(self):
        """Test crear usuario con privilegios de superusuario"""
        organization = OrganizationFactory()
        superuser = User.objects.create_superuser(
            username="superuser",
            email="super@example.com",
            password="superpass123",
            organization=organization
        )

        assert superuser.is_superuser is True
        assert superuser.is_staff is True
        assert superuser.is_active is True
        assert superuser.organization == organization

    def test_user_email_field(self):
        """Test campo de email"""
        user = UserFactory(email="test.email@example.com")
        
        assert user.email == "test.email@example.com"
        assert "@" in user.email
        
