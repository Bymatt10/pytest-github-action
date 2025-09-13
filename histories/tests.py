import pytest
from decimal import Decimal

from histories.models import RainfallHistory
from histories.factories import RainfallHistoryFactory
from stations.factories import StationFactory


@pytest.mark.django_db
class TestRainfallHistoryCRUD:
    """Tests CRUD para el modelo RainfallHistory"""

    def test_create_rainfall_history(self):
        """Test crear un historial de lluvia"""
        history = RainfallHistoryFactory()

        assert history.id is not None
        assert history.station is not None
        assert isinstance(history.month, int)
        assert 1 <= history.month <= 12
        assert history.value is not None
        assert isinstance(history.value, Decimal)
        assert history.created is not None
        assert history.modified is not None

    def test_create_rainfall_history_minimal_fields(self):
        """Test crear historial con campos mínimos requeridos"""
        station = StationFactory()
        history = RainfallHistory.objects.create(
            station=station,
            month=6
        )

        assert history.id is not None
        assert history.station == station
        assert history.month == 6
        assert history.value is None  # campo opcional

    def test_create_rainfall_history_with_specific_values(self):
        """Test crear historial con valores específicos"""
        station = StationFactory()
        history = RainfallHistory.objects.create(
            station=station,
            month=8,
            value=Decimal("125.75")
        )

        assert history.station == station
        assert history.month == 8
        assert history.value == Decimal("125.75")

    def test_read_rainfall_history(self):
        """Test leer un historial de lluvia"""
        history = RainfallHistoryFactory()
        retrieved_history = RainfallHistory.objects.get(id=history.id)

        assert retrieved_history.id == history.id
        assert retrieved_history.station == history.station
        assert retrieved_history.month == history.month
        assert retrieved_history.value == history.value

    def test_update_rainfall_history(self):
        """Test actualizar un historial de lluvia"""
        history = RainfallHistoryFactory()
        original_month = history.month
        original_value = history.value
        original_modified = history.modified

        # Actualizar el historial
        history.month = 12
        history.value = Decimal("200.50")
        history.save()

        # Verificar la actualización
        updated_history = RainfallHistory.objects.get(id=history.id)
        assert updated_history.month == 12
        assert updated_history.month != original_month
        assert updated_history.value == Decimal("200.50")
        assert updated_history.value != original_value
        assert updated_history.modified > original_modified

    def test_delete_rainfall_history(self):
        """Test eliminar un historial de lluvia"""
        history = RainfallHistoryFactory()
        history_id = history.id

        # Eliminar el historial
        history.delete()

        # Verificar eliminación
        with pytest.raises(RainfallHistory.DoesNotExist):
            RainfallHistory.objects.get(id=history_id)

    def test_rainfall_history_str_method(self):
        """Test método __str__ del modelo"""
        history = RainfallHistory.objects.create(
            station=StationFactory(),
            month=7
        )

        # Nota: El método __str__ retorna el mes como entero, 
        # pero str() lo convierte a string
        assert str(history) == "7"

    def test_rainfall_history_station_relationship(self):
        """Test relación con Station"""
        station = StationFactory()
        history = RainfallHistoryFactory(station=station)

        assert history.station == station
        assert history.station.name is not None
        assert history.station.code is not None

    def test_rainfall_history_month_range(self):
        """Test valores válidos para el mes"""
        station = StationFactory()
        
        # Probar diferentes meses válidos
        for month in range(1, 13):
            history = RainfallHistory.objects.create(
                station=station,
                month=month,
                value=Decimal("50.00")
            )
            assert history.month == month

    def test_rainfall_history_decimal_precision(self):
        """Test precisión decimal del campo value"""
        station = StationFactory()
        history = RainfallHistory.objects.create(
            station=station,
            month=5,
            value=Decimal("123.45")
        )

        assert history.value == Decimal("123.45")
        # Verificar que mantiene la precisión de 2 decimales
        assert str(history.value) == "123.45"

    def test_rainfall_history_default_values(self):
        """Test valores por defecto del modelo"""
        station = StationFactory()
        history = RainfallHistory.objects.create(
            station=station
        )

        assert history.month == 0  # valor por defecto
        assert history.value is None  # puede ser nulo

    def test_rainfall_history_station_protect_constraint(self):
        """Test que no se puede eliminar station si tiene historiales"""
        station = StationFactory()
        history = RainfallHistoryFactory(station=station)
        
        # Intentar eliminar la estación debería fallar por PROTECT
        with pytest.raises(Exception):  # ProtectedError en Django
            station.delete()
        
        # Verificar que tanto el historial como la estación siguen existiendo
        assert RainfallHistory.objects.filter(id=history.id).exists()
        assert station.__class__.objects.filter(id=station.id).exists()

    def test_multiple_histories_same_station(self):
        """Test múltiples historiales para la misma estación"""
        station = StationFactory()
        history1 = RainfallHistoryFactory(station=station, month=1)
        history2 = RainfallHistoryFactory(station=station, month=2)
        history3 = RainfallHistoryFactory(station=station, month=3)

        # Verificar que todos los historiales están asociados a la misma estación
        assert history1.station == station
        assert history2.station == station
        assert history3.station == station
        
        # Verificar que son registros diferentes
        assert history1.id != history2.id != history3.id

    def test_rainfall_history_large_values(self):
        """Test valores grandes en el campo value"""
        station = StationFactory()
        large_value = Decimal("99999999.99")  # Valor máximo para max_digits=10, decimal_places=2
        
        history = RainfallHistory.objects.create(
            station=station,
            month=11,
            value=large_value
        )

        assert history.value == large_value
