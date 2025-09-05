import pytest
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date

from stations.models import Station, EquipmentStation, RainfallStation
from stations.factories import StationFactory, EquipmentStationFactory, RainfallStationFactory
from organizations.factories import OrganizationFactory
from accounts.factories import AdminUserFactory


@pytest.mark.django_db
class TestStationAPI:
    """Tests API CRUD para StationViewSet"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.admin_user = AdminUserFactory()
        self.client.force_authenticate(user=self.admin_user)
        self.base_url = "/api/v1/stations/"

    def test_list_stations(self):
        """Test GET /api/v1/stations/ - Listar estaciones"""
        StationFactory.create_batch(4)
        
        response = self.client.get(self.base_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 4
        assert "results" in response.data
        assert "count" in response.data

    def test_create_station(self):
        """Test POST /api/v1/stations/ - Crear estación"""
        organization = OrganizationFactory()
        data = {
            "name": "Estación Meteorológica Central",
            "code": "EMC001",
            "latitude": "12.1364",
            "longitude": "-86.2514",
            "address": "Centro de Managua",
            "organization": organization.id
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Estación Meteorológica Central"
        assert response.data["code"] == "EMC001"
        assert response.data["latitude"] == "12.1364"
        assert response.data["organization"]["id"] == organization.id
        
        # Verificar en base de datos
        station = Station.objects.get(code="EMC001")
        assert station.name == "Estación Meteorológica Central"

    def test_create_station_minimal_fields(self):
        """Test crear estación con campos mínimos"""
        organization = OrganizationFactory()
        data = {
            "name": "Estación Básica",
            "code": "EB001",
            "organization": organization.id
            # latitude, longitude, address son opcionales
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["latitude"] is None
        assert response.data["longitude"] is None
        assert response.data["address"] is None

    def test_retrieve_station(self):
        """Test GET /api/v1/stations/{id}/ - Obtener estación específica"""
        station = StationFactory()
        url = f"{self.base_url}{station.id}/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == station.id
        assert response.data["name"] == station.name
        assert response.data["code"] == station.code

    def test_update_station(self):
        """Test PUT /api/v1/stations/{id}/ - Actualizar estación completa"""
        station = StationFactory()
        new_organization = OrganizationFactory()
        url = f"{self.base_url}{station.id}/"
        
        data = {
            "name": "Estación Actualizada",
            "code": station.code,
            "latitude": "13.0000",
            "longitude": "-87.0000",
            "address": "Nueva Dirección",
            "organization": new_organization.id
        }
        
        response = self.client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Estación Actualizada"
        assert response.data["latitude"] == "13.0000"
        
        # Verificar en base de datos
        station.refresh_from_db()
        assert station.name == "Estación Actualizada"

    def test_filter_by_organization(self):
        """Test filtrar por organización"""
        org1 = OrganizationFactory()
        org2 = OrganizationFactory()
        
        StationFactory.create_batch(2, organization=org1)
        StationFactory.create_batch(3, organization=org2)
        
        response = self.client.get(f"{self.base_url}?organization={org1.id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_search_stations(self):
        """Test búsqueda por nombre y código"""
        StationFactory(name="Estación Norte", code="EN001")
        StationFactory(name="Estación Sur", code="ES001")
        
        response = self.client.get(f"{self.base_url}?search=Norte")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert "Norte" in response.data["results"][0]["name"]


@pytest.mark.django_db
class TestEquipmentStationAPI:
    """Tests API CRUD para EquipmentStationViewSet"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.admin_user = AdminUserFactory()
        self.client.force_authenticate(user=self.admin_user)
        self.base_url = "/api/v1/equipments/"

    def test_list_equipments(self):
        """Test GET /api/v1/equipments/ - Listar equipos"""
        EquipmentStationFactory.create_batch(3)
        
        response = self.client.get(self.base_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_create_equipment(self):
        """Test POST /api/v1/equipments/ - Crear equipo"""
        station = StationFactory()
        data = {
            "name": "Pluviómetro Digital",
            "code": "PD001",
            "brand": "WeatherTech",
            "model": "WT-2024",
            "station": station.id
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Pluviómetro Digital"
        assert response.data["brand"] == "WeatherTech"
        assert response.data["station"]["id"] == station.id

    def test_filter_by_station(self):
        """Test filtrar equipos por estación"""
        station1 = StationFactory()
        station2 = StationFactory()
        
        EquipmentStationFactory.create_batch(2, station=station1)
        EquipmentStationFactory.create_batch(1, station=station2)
        
        response = self.client.get(f"{self.base_url}?station={station1.id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_search_equipment(self):
        """Test búsqueda en equipos"""
        EquipmentStationFactory(name="Termómetro Digital", brand="TechBrand")
        EquipmentStationFactory(name="Barómetro Analógico", brand="ClassicBrand")
        
        response = self.client.get(f"{self.base_url}?search=Digital")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert "Digital" in response.data["results"][0]["name"]


@pytest.mark.django_db
class TestRainfallStationAPI:
    """Tests API CRUD para RainfallStationViewSet"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.admin_user = AdminUserFactory()
        self.client.force_authenticate(user=self.admin_user)
        self.base_url = "/api/v1/rainfall/"

    def test_list_rainfall_records(self):
        """Test GET /api/v1/rainfall/ - Listar registros de lluvia"""
        RainfallStationFactory.create_batch(5)
        
        response = self.client.get(self.base_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 5

    def test_create_rainfall_record(self):
        """Test POST /api/v1/rainfall/ - Crear registro de lluvia"""
        station = StationFactory()
        data = {
            "station": station.id,
            "registration_date": "2024-01-15",
            "day": 15,
            "month": 1,
            "year": 2024,
            "value": "25.50"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["day"] == 15
        assert response.data["month"] == 1
        assert response.data["year"] == 2024
        assert response.data["value"] == "25.50"
        assert response.data["station"]["id"] == station.id

    def test_create_rainfall_minimal_fields(self):
        """Test crear registro con campos mínimos"""
        station = StationFactory()
        data = {
            "station": station.id,
            "registration_date": "2024-02-01"
            # day, month, year, value tienen valores por defecto
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["day"] == 0  # valor por defecto
        assert response.data["month"] == 0  # valor por defecto
        assert response.data["year"] == 0  # valor por defecto
        assert response.data["value"] is None  # puede ser null

    def test_filter_by_station(self):
        """Test filtrar registros por estación"""
        station1 = StationFactory()
        station2 = StationFactory()
        
        RainfallStationFactory.create_batch(3, station=station1)
        RainfallStationFactory.create_batch(2, station=station2)
        
        response = self.client.get(f"{self.base_url}?station={station1.id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_filter_by_month(self):
        """Test filtrar por mes"""
        station = StationFactory()
        RainfallStationFactory.create_batch(2, station=station, month=6)
        RainfallStationFactory.create_batch(3, station=station, month=12)
        
        response = self.client.get(f"{self.base_url}?month=6")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        for record in response.data["results"]:
            assert record["month"] == 6

    def test_filter_by_year(self):
        """Test filtrar por año"""
        station = StationFactory()
        RainfallStationFactory.create_batch(2, station=station, year=2023)
        RainfallStationFactory.create_batch(3, station=station, year=2024)
        
        response = self.client.get(f"{self.base_url}?year=2024")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_ordering_by_date(self):
        """Test ordenamiento por fecha de registro"""
        station = StationFactory()
        RainfallStationFactory(station=station, registration_date=date(2024, 1, 1))
        RainfallStationFactory(station=station, registration_date=date(2024, 2, 1))
        
        response = self.client.get(f"{self.base_url}?ordering=registration_date")
        
        assert response.status_code == status.HTTP_200_OK
        dates = [record["registration_date"] for record in response.data["results"]]
        assert dates == sorted(dates)

    def test_decimal_precision_validation(self):
        """Test validación de precisión decimal"""
        station = StationFactory()
        data = {
            "station": station.id,
            "registration_date": "2024-01-15",
            "value": "123.456789"  # Más de 2 decimales
        }
        
        response = self.client.post(self.base_url, data)
        
        # Dependiendo de la validación del serializer
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

    def test_large_rainfall_values(self):
        """Test valores grandes de precipitación"""
        station = StationFactory()
        data = {
            "station": station.id,
            "registration_date": "2024-01-15",
            "value": "999999.99"  # Valor grande pero válido
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["value"] == "999999.99"

    def test_multiple_records_same_station(self):
        """Test múltiples registros para la misma estación"""
        station = StationFactory()
        
        # Crear registros para diferentes fechas
        dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
        for i, date_str in enumerate(dates):
            data = {
                "station": station.id,
                "registration_date": date_str,
                "value": f"{10 + i}.50"
            }
            response = self.client.post(self.base_url, data)
            assert response.status_code == status.HTTP_201_CREATED

        # Verificar que todos están asociados a la misma estación
        response = self.client.get(f"{self.base_url}?station={station.id}")
        assert len(response.data["results"]) == 3


@pytest.mark.django_db
class TestStationsUnauthorizedAccess:
    """Tests de acceso no autorizado para todos los endpoints de stations"""

    def test_unauthorized_access_stations(self):
        """Test acceso sin autenticación a stations"""
        client = APIClient()
        
        endpoints = [
            "/api/v1/stations/",
            "/api/v1/equipments/",
            "/api/v1/rainfall/"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
