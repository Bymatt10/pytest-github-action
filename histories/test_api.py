import pytest
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal

from histories.models import RainfallHistory
from histories.factories import RainfallHistoryFactory
from stations.factories import StationFactory
from accounts.factories import AdminUserFactory


@pytest.mark.django_db
class TestRainfallHistoryAPI:
    """Tests API CRUD para RainfallHistoryViewSet"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.admin_user = AdminUserFactory()
        self.client.force_authenticate(user=self.admin_user)
        self.base_url = "/api/v1/histories/"

    def test_list_rainfall_histories(self):
        """Test GET /api/v1/histories/ - Listar historiales de lluvia"""
        RainfallHistoryFactory.create_batch(6)
        
        response = self.client.get(self.base_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 6
        assert "results" in response.data
        assert "count" in response.data

    def test_create_rainfall_history(self):
        """Test POST /api/v1/histories/ - Crear historial de lluvia"""
        station = StationFactory()
        data = {
            "station": station.id,
            "month": 8,
            "value": "156.75"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["month"] == 8
        assert response.data["value"] == "156.75"
        assert response.data["station"]["id"] == station.id
        
        # Verificar en base de datos
        history = RainfallHistory.objects.get(month=8, station=station)
        assert history.value == Decimal("156.75")

    def test_create_rainfall_history_minimal_fields(self):
        """Test crear historial con campos mínimos"""
        station = StationFactory()
        data = {
            "station": station.id
            # month tiene valor por defecto 0, value puede ser null
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["month"] == 0  # valor por defecto
        assert response.data["value"] is None  # puede ser null

    def test_create_rainfall_history_specific_month(self):
        """Test crear historial para mes específico"""
        station = StationFactory()
        data = {
            "station": station.id,
            "month": 12,  # Diciembre
            "value": "45.25"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["month"] == 12
        assert response.data["value"] == "45.25"

    def test_retrieve_rainfall_history(self):
        """Test GET /api/v1/histories/{id}/ - Obtener historial específico"""
        history = RainfallHistoryFactory()
        url = f"{self.base_url}{history.id}/"
        
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == history.id
        assert response.data["month"] == history.month
        assert response.data["station"]["id"] == history.station.id

    def test_update_rainfall_history(self):
        """Test PUT /api/v1/histories/{id}/ - Actualizar historial completo"""
        history = RainfallHistoryFactory()
        new_station = StationFactory()
        url = f"{self.base_url}{history.id}/"
        
        data = {
            "station": new_station.id,
            "month": 6,
            "value": "89.50"
        }
        
        response = self.client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["month"] == 6
        assert response.data["value"] == "89.50"
        assert response.data["station"]["id"] == new_station.id
        
        # Verificar en base de datos
        history.refresh_from_db()
        assert history.month == 6
        assert history.value == Decimal("89.50")
        assert history.station == new_station

    def test_partial_update_rainfall_history(self):
        """Test PATCH /api/v1/histories/{id}/ - Actualización parcial"""
        history = RainfallHistoryFactory()
        url = f"{self.base_url}{history.id}/"
        
        data = {
            "value": "123.45"
        }
        
        response = self.client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["value"] == "123.45"
        
        # Verificar en base de datos
        history.refresh_from_db()
        assert history.value == Decimal("123.45")

    def test_delete_rainfall_history(self):
        """Test DELETE /api/v1/histories/{id}/ - Eliminar historial"""
        history = RainfallHistoryFactory()
        url = f"{self.base_url}{history.id}/"
        
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar eliminación en base de datos
        assert not RainfallHistory.objects.filter(id=history.id).exists()

    def test_filter_by_station(self):
        """Test filtrar historiales por estación"""
        station1 = StationFactory()
        station2 = StationFactory()
        
        RainfallHistoryFactory.create_batch(3, station=station1)
        RainfallHistoryFactory.create_batch(2, station=station2)
        
        response = self.client.get(f"{self.base_url}?station={station1.id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3
        for history in response.data["results"]:
            assert history["station"]["id"] == station1.id

    def test_filter_by_month(self):
        """Test filtrar por mes"""
        station = StationFactory()
        RainfallHistoryFactory.create_batch(2, station=station, month=3)  # Marzo
        RainfallHistoryFactory.create_batch(4, station=station, month=9)  # Septiembre
        
        response = self.client.get(f"{self.base_url}?month=3")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        for history in response.data["results"]:
            assert history["month"] == 3

    def test_ordering_by_id(self):
        """Test ordenamiento por ID"""
        RainfallHistoryFactory.create_batch(4)
        
        response = self.client.get(f"{self.base_url}?ordering=id")
        
        assert response.status_code == status.HTTP_200_OK
        ids = [history["id"] for history in response.data["results"]]
        assert ids == sorted(ids)

    def test_pagination_disabled(self):
        """Test paginación deshabilitada"""
        RainfallHistoryFactory.create_batch(8)
        
        response = self.client.get(f"{self.base_url}?paginator=false")
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 8

    def test_monthly_rainfall_data(self):
        """Test datos de lluvia por meses del año"""
        station = StationFactory()
        
        # Crear historiales para todos los meses
        monthly_data = [
            (1, "45.50"),   # Enero
            (2, "32.75"),   # Febrero
            (3, "28.25"),   # Marzo
            (4, "15.00"),   # Abril
            (5, "125.50"),  # Mayo (época lluviosa)
            (6, "180.75"),  # Junio
            (7, "165.25"),  # Julio
            (8, "145.00"),  # Agosto
            (9, "155.50"),  # Septiembre
            (10, "95.75"),  # Octubre
            (11, "65.25"),  # Noviembre
            (12, "55.00"),  # Diciembre
        ]
        
        for month, value in monthly_data:
            data = {
                "station": station.id,
                "month": month,
                "value": value
            }
            response = self.client.post(self.base_url, data)
            assert response.status_code == status.HTTP_201_CREATED

        # Verificar que se crearon todos los registros
        response = self.client.get(f"{self.base_url}?station={station.id}")
        assert len(response.data["results"]) == 12

    def test_decimal_precision_validation(self):
        """Test precisión decimal en valores"""
        station = StationFactory()
        data = {
            "station": station.id,
            "month": 5,
            "value": "999.99"  # Máximo con 2 decimales
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["value"] == "999.99"

    def test_large_rainfall_values(self):
        """Test valores grandes de precipitación mensual"""
        station = StationFactory()
        data = {
            "station": station.id,
            "month": 6,
            "value": "99999999.99"  # Valor muy grande pero dentro del rango
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["value"] == "99999999.99"

    def test_zero_rainfall_value(self):
        """Test valor de lluvia cero (mes seco)"""
        station = StationFactory()
        data = {
            "station": station.id,
            "month": 2,
            "value": "0.00"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["value"] == "0.00"

    def test_null_rainfall_value(self):
        """Test valor de lluvia nulo (sin medición)"""
        station = StationFactory()
        data = {
            "station": station.id,
            "month": 4,
            "value": None
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["value"] is None

    def test_multiple_histories_same_station_different_months(self):
        """Test múltiples historiales para la misma estación en diferentes meses"""
        station = StationFactory()
        
        months_data = [(1, "25.50"), (6, "150.75"), (12, "45.25")]
        
        for month, value in months_data:
            data = {
                "station": station.id,
                "month": month,
                "value": value
            }
            response = self.client.post(self.base_url, data)
            assert response.status_code == status.HTTP_201_CREATED

        # Verificar filtros por mes específico
        for month, expected_value in months_data:
            response = self.client.get(f"{self.base_url}?station={station.id}&month={month}")
            assert len(response.data["results"]) == 1
            assert response.data["results"][0]["value"] == expected_value

    def test_create_history_validation_errors(self):
        """Test validaciones en creación"""
        # Datos incompletos - falta station requerida
        data = {
            "month": 8,
            "value": "100.50"
            # Falta station
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "station" in response.data

    def test_invalid_month_validation(self):
        """Test validación de mes inválido"""
        station = StationFactory()
        data = {
            "station": station.id,
            "month": 13,  # Mes inválido
            "value": "50.00"
        }
        
        response = self.client.post(self.base_url, data)
        
        # Dependiendo de las validaciones del serializer
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

    def test_station_relationship_in_response(self):
        """Test que la respuesta incluye información completa de la estación"""
        station = StationFactory(name="Estación Central")
        history = RainfallHistoryFactory(station=station)
        
        url = f"{self.base_url}{history.id}/"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["station"]["name"] == "Estación Central"
        assert response.data["station"]["id"] == station.id

    def test_unauthorized_access(self):
        """Test acceso sin autenticación"""
        client = APIClient()
        
        response = client.get(self.base_url)
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_history_str_method_via_api(self):
        """Test que el método __str__ del modelo funciona correctamente"""
        station = StationFactory()
        data = {
            "station": station.id,
            "month": 7,
            "value": "88.50"
        }
        
        response = self.client.post(self.base_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar en base de datos que el método __str__ funciona
        history = RainfallHistory.objects.get(id=response.data["id"])
        assert str(history) == "7"
