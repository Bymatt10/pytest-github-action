import pytest
from django.test import TestCase
from decimal import Decimal
from datetime import date

from stations.models import Station, EquipmentStation, RainfallStation
from stations.factories import (
    LocationFactory, 
    OrganizationFactory, 
    StationFactory, 
    EquipmentStationFactory, 
    RainfallStationFactory
)


@pytest.mark.django_db
class TestStationCRUD:
    """Tests CRUD para el modelo Station"""
    
    def test_create_station(self):
        """Test crear una estación"""
        organization = OrganizationFactory()
        station = StationFactory(organization=organization)
        
        assert station.id is not None
        assert station.name.startswith("Station")
        assert station.code.startswith("STA")
        assert station.organization == organization
        assert station.created is not None
        assert station.modified is not None
    
    def test_create_station_minimal_fields(self):
        """Test crear estación con campos mínimos requeridos"""
        organization = OrganizationFactory()
        station = Station.objects.create(
            name="Test Station",
            code="TST001",
            organization=organization
        )
        
        assert station.id is not None
        assert station.name == "Test Station"
        assert station.code == "TST001"
        assert station.latitude is None
        assert station.longitude is None
        assert station.address is None
        assert station.organization == organization
    
    def test_read_station(self):
        """Test leer una estación"""
        station = StationFactory()
        retrieved_station = Station.objects.get(id=station.id)
        
        assert retrieved_station.id == station.id
        assert retrieved_station.name == station.name
        assert retrieved_station.code == station.code
        assert retrieved_station.organization == station.organization
    
    def test_update_station(self):
        """Test actualizar una estación"""
        station = StationFactory()
        original_name = station.name
        original_modified = station.modified
        
        # Actualizar la estación
        station.name = "Updated Station Name"
        station.latitude = "-17.393"
        station.longitude = "-66.157"
        station.address = "Updated Address"
        station.save()
        
        # Verificar la actualización
        updated_station = Station.objects.get(id=station.id)
        assert updated_station.name == "Updated Station Name"
        assert updated_station.name != original_name
        assert updated_station.latitude == "-17.393"
        assert updated_station.longitude == "-66.157"
        assert updated_station.address == "Updated Address"
        assert updated_station.modified > original_modified
    
    def test_delete_station(self):
        """Test eliminar una estación"""
        station = StationFactory()
        station_id = station.id
        
        # Eliminar la estación
        station.delete()
        
        # Verificar eliminación
        with pytest.raises(Station.DoesNotExist):
            Station.objects.get(id=station_id)


@pytest.mark.django_db
class TestEquipmentStationCRUD:
    """Tests CRUD para el modelo EquipmentStation"""
    
    def test_create_equipment_station(self):
        """Test crear un equipo de estación"""
        station = StationFactory()
        equipment = EquipmentStationFactory(station=station)
        
        assert equipment.id is not None
        assert equipment.name.startswith("Equipment")
        assert equipment.code.startswith("EQP")
        assert equipment.station == station
        assert equipment.created is not None
        assert equipment.modified is not None
    
    def test_create_equipment_minimal_fields(self):
        """Test crear equipo con campos mínimos"""
        station = StationFactory()
        equipment = EquipmentStation.objects.create(
            name="Test Equipment",
            code="EQP001",
            station=station
        )
        
        assert equipment.id is not None
        assert equipment.name == "Test Equipment"
        assert equipment.code == "EQP001"
        assert equipment.brand is None
        assert equipment.model is None
        assert equipment.station == station
    
    def test_read_equipment_station(self):
        """Test leer un equipo de estación"""
        equipment = EquipmentStationFactory()
        retrieved_equipment = EquipmentStation.objects.get(id=equipment.id)
        
        assert retrieved_equipment.id == equipment.id
        assert retrieved_equipment.name == equipment.name
        assert retrieved_equipment.code == equipment.code
        assert retrieved_equipment.station == equipment.station
    
    def test_update_equipment_station(self):
        """Test actualizar un equipo de estación"""
        equipment = EquipmentStationFactory()
        original_name = equipment.name
        
        # Actualizar el equipo
        equipment.name = "Updated Equipment"
        equipment.brand = "Updated Brand"
        equipment.model = "Updated Model"
        equipment.save()
        
        # Verificar la actualización
        updated_equipment = EquipmentStation.objects.get(id=equipment.id)
        assert updated_equipment.name == "Updated Equipment"
        assert updated_equipment.name != original_name
        assert updated_equipment.brand == "Updated Brand"
        assert updated_equipment.model == "Updated Model"
    
    def test_delete_equipment_station(self):
        """Test eliminar un equipo de estación"""
        equipment = EquipmentStationFactory()
        equipment_id = equipment.id
        
        # Eliminar el equipo
        equipment.delete()
        
        # Verificar eliminación
        with pytest.raises(EquipmentStation.DoesNotExist):
            EquipmentStation.objects.get(id=equipment_id)


@pytest.mark.django_db
class TestRainfallStationCRUD:
    """Tests CRUD para el modelo RainfallStation"""
    
    def test_create_rainfall_station(self):
        """Test crear un registro de lluvia"""
        station = StationFactory()
        rainfall = RainfallStationFactory(station=station)
        
        assert rainfall.id is not None
        assert rainfall.station == station
        assert rainfall.registration_date is not None
        assert isinstance(rainfall.day, int)
        assert isinstance(rainfall.month, int)
        assert isinstance(rainfall.year, int)
        assert rainfall.created is not None
        assert rainfall.modified is not None
    
    def test_create_rainfall_with_specific_values(self):
        """Test crear registro de lluvia con valores específicos"""
        station = StationFactory()
        rainfall = RainfallStation.objects.create(
            station=station,
            registration_date=date(2024, 1, 15),
            day=15,
            month=1,
            year=2024,
            value=Decimal('25.50')
        )
        
        assert rainfall.station == station
        assert rainfall.registration_date == date(2024, 1, 15)
        assert rainfall.day == 15
        assert rainfall.month == 1
        assert rainfall.year == 2024
        assert rainfall.value == Decimal('25.50')
    
    def test_read_rainfall_station(self):
        """Test leer un registro de lluvia"""
        rainfall = RainfallStationFactory()
        retrieved_rainfall = RainfallStation.objects.get(id=rainfall.id)
        
        assert retrieved_rainfall.id == rainfall.id
        assert retrieved_rainfall.station == rainfall.station
        assert retrieved_rainfall.registration_date == rainfall.registration_date
        assert retrieved_rainfall.day == rainfall.day
        assert retrieved_rainfall.month == rainfall.month
        assert retrieved_rainfall.year == rainfall.year
    
    def test_update_rainfall_station(self):
        """Test actualizar un registro de lluvia"""
        rainfall = RainfallStationFactory()
        original_value = rainfall.value
        
        # Actualizar el registro de lluvia
        rainfall.value = Decimal('50.75')
        rainfall.day = 20
        rainfall.month = 6
        rainfall.year = 2023
        rainfall.save()
        
        # Verificar la actualización
        updated_rainfall = RainfallStation.objects.get(id=rainfall.id)
        assert updated_rainfall.value == Decimal('50.75')
        assert updated_rainfall.value != original_value
        assert updated_rainfall.day == 20
        assert updated_rainfall.month == 6
        assert updated_rainfall.year == 2023
    
    def test_delete_rainfall_station(self):
        """Test eliminar un registro de lluvia"""
        rainfall = RainfallStationFactory()
        rainfall_id = rainfall.id
        
        # Eliminar el registro de lluvia
        rainfall.delete()
        
        # Verificar eliminación
        with pytest.raises(RainfallStation.DoesNotExist):
            RainfallStation.objects.get(id=rainfall_id)
    
    def test_rainfall_default_values(self):
        """Test valores por defecto del modelo"""
        station = StationFactory()
        rainfall = RainfallStation.objects.create(
            station=station,
            registration_date=date.today()
        )
        
        assert rainfall.day == 0
        assert rainfall.month == 0
        assert rainfall.year == 0
        assert rainfall.value is None
