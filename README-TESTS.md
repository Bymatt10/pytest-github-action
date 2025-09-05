# 🧪 Guía de Tests - ROCC API

## 📋 Resumen General

Este proyecto cuenta con una suite completa de tests usando **pytest** para Django, con **70 tests** que cubren todos los modelos principales y sus operaciones CRUD. Los tests están organizados por módulos con factories separados para mantener el orden y la consistencia.

## 🏗️ Estructura de Tests

```
rocc-api/
├── accounts/
│   ├── factories.py     # UserFactory, AdminUserFactory, ObserverUserFactory
│   └── tests.py         # 19 tests para autenticación y usuarios
├── histories/
│   ├── factories.py     # RainfallHistoryFactory
│   └── tests.py         # 14 tests para historiales de lluvia
├── locations/
│   ├── factories.py     # LocationFactory
│   └── tests.py         # 13 tests para ubicaciones geográficas
├── organizations/
│   ├── factories.py     # OrganizationFactory
│   └── tests.py         # 8 tests para organizaciones
└── stations/
    ├── factories.py     # StationFactory, EquipmentStationFactory, RainfallStationFactory
    └── tests.py         # 16 tests para estaciones meteorológicas
```

## 🚀 Ejecutar Tests

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar tests con salida detallada
```bash
pytest -v
```

### Ejecutar tests de un módulo específico
```bash
pytest accounts/tests.py -v
pytest locations/tests.py -v
pytest stations/tests.py -v
```

### Ejecutar con cobertura
```bash
pytest --cov=. --cov-report=html
```

## 📊 Estadísticas Actuales

- **Total de tests:** 70
- **Éxito:** 100% (70/70 pasando)
- **Cobertura:** 73% del código total
- **Tiempo de ejecución:** ~3.3 segundos

## 🧪 Descripción por Módulo

### 🔐 **Accounts (19 tests)**
**Propósito:** Tests para el sistema de autenticación y gestión de usuarios

**Modelos testeados:** `User` (hereda de AbstractUser)

**Tests incluyen:**
- ✅ Creación de usuarios (normales, admin, observadores)
- ✅ Autenticación con contraseñas personalizadas
- ✅ Gestión de roles (admin/observer)
- ✅ Integración con Firebase UID (único y nullable)
- ✅ Relaciones con organizaciones (constraint PROTECT)
- ✅ Validación de campos obligatorios y opcionales
- ✅ Creación de superusuarios

**Factory destacado:**
```python
UserFactory()  # Usuario básico
AdminUserFactory()  # Usuario administrador
ObserverUserFactory()  # Usuario observador
```

### 🌧️ **Histories (14 tests)**
**Propósito:** Tests para historiales mensuales de precipitación

**Modelos testeados:** `RainfallHistory`

**Tests incluyen:**
- ✅ CRUD completo de historiales
- ✅ Relación con estaciones (constraint PROTECT)
- ✅ Validación de precisión decimal (10 dígitos, 2 decimales)
- ✅ Rangos válidos para meses (1-12)
- ✅ Múltiples historiales por estación
- ✅ Valores grandes y casos límite
- ✅ Valores por defecto (mes=0, value=null)

**Factory destacado:**
```python
RainfallHistoryFactory(
    station=StationFactory(),
    month=6,  # Mes entre 1-12
    value=Decimal("125.75")
)
```

### 🌍 **Locations (13 tests)**
**Propósito:** Tests para ubicaciones geográficas jerárquicas

**Modelos testeados:** `Location`

**Tests incluyen:**
- ✅ CRUD completo de ubicaciones
- ✅ Jerarquías padre-hijo (país→departamento→municipio→comunidad)
- ✅ Tipos de ubicación válidos
- ✅ Constraint SET_NULL (hijos quedan huérfanos al eliminar padre)
- ✅ Datos contextualizados para Nicaragua
- ✅ Validación de campos opcionales

**Tipos soportados:**
- `country` (País)
- `department` (Departamento)  
- `municipality` (Municipio)
- `communnity` (Comunidad)

### 🏢 **Organizations (8 tests)**
**Propósito:** Tests para organizaciones meteorológicas

**Modelos testeados:** `Organization`

**Tests incluyen:**
- ✅ CRUD completo de organizaciones
- ✅ Relación con ubicaciones
- ✅ Datos realistas de instituciones nicaragüenses
- ✅ Validación de teléfonos (+505 formato)
- ✅ Direcciones contextualizadas

**Ejemplos de organizaciones:**
- Instituto Nicaragüense de Estudios Territoriales
- Servicio Nacional de Meteorología de Nicaragua
- Centro de Investigaciones Hídricas de Nicaragua

### 🌡️ **Stations (16 tests)**
**Propósito:** Tests para estaciones meteorológicas y sus equipos

**Modelos testeados:** `Station`, `EquipmentStation`, `RainfallStation`

**Tests incluyen:**
- ✅ CRUD para estaciones meteorológicas
- ✅ CRUD para equipos de estación
- ✅ CRUD para registros diarios de lluvia
- ✅ Relaciones entre estación-organización
- ✅ Coordenadas geográficas (latitud/longitud)
- ✅ Validación de códigos únicos
- ✅ Valores decimales para precipitación

## 🎯 Patrones de Testing

### Estructura Consistente
Todos los módulos siguen el mismo patrón:

```python
@pytest.mark.django_db
class TestModelCRUD:
    """Tests CRUD para el modelo Model"""
    
    def test_create_model(self):
        """Test crear un modelo"""
        
    def test_read_model(self):
        """Test leer un modelo"""
        
    def test_update_model(self):
        """Test actualizar un modelo"""
        
    def test_delete_model(self):
        """Test eliminar un modelo"""
```

### Factories Separados
Cada módulo tiene su propio archivo `factories.py`:

```python
class ModelFactory(DjangoModelFactory):
    class Meta:
        model = Model
    
    field1 = factory.Faker("provider")
    field2 = factory.Sequence(lambda n: f"prefix{n}")
    relation = factory.SubFactory(RelatedFactory)
```

### Tests de Relaciones
Se validan constraints de base de datos:

```python
# PROTECT constraint
with pytest.raises(Exception):
    parent.delete()  # Falla si tiene hijos

# SET_NULL constraint  
parent.delete()
assert child.parent is None  # Se actualiza a NULL
```

## 🛠️ Configuración

### Dependencias
- `pytest-django` - Integración Django con pytest
- `factory-boy` - Generación de datos de prueba
- `faker` - Datos realistas falsos

### Configuración pytest.ini
```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = config.settings
addopts = --tb=short --strict-markers --disable-warnings
testpaths = .
python_files = tests.py test_*.py *_tests.py
```

## 🎨 Datos de Prueba

### Contextualización Nicaragua
Los factories generan datos realistas para el contexto nicaragüense:

- **Teléfonos:** Formato +505-X-XXXXXXX
- **Ubicaciones:** Managua, León, Granada, Estelí, etc.
- **Direcciones:** Referencias típicas nicaragüenses
- **Organizaciones:** Instituciones gubernamentales reales

### Ejemplos de Datos Generados
```python
# Ubicaciones
"Managua", "León", "Granada", "Chinandega"

# Teléfonos  
"+505-2-2234567", "+505-8-8234567"

# Direcciones
"Km 12 Carretera Norte, Managua"
"Del Hospital Militar 3c al Norte"
"Rotonda El Güegüense 200m al Sur"
```

## 📈 Cobertura de Tests

### Por Módulo
- **accounts/models.py:** 100%
- **histories/models.py:** 100% 
- **locations/models.py:** 100%
- **organizations/models.py:** 100%
- **stations/models.py:** 91%

### Áreas Cubiertas
- ✅ Operaciones CRUD completas
- ✅ Validaciones de modelo
- ✅ Relaciones entre entidades
- ✅ Constraints de base de datos
- ✅ Valores por defecto
- ✅ Casos límite y edge cases
- ✅ Métodos personalizados (`__str__`, propiedades)

## 🔧 Comandos Útiles

```bash
# Ejecutar tests con coverage
pytest --cov=. --cov-report=html

# Ejecutar solo tests que fallaron
pytest --lf

# Ejecutar tests en paralelo
pytest -n auto

# Ejecutar tests con salida detallada y sin warnings
pytest -v --disable-warnings

# Ejecutar tests de un modelo específico
pytest -k "TestUserCRUD" -v

# Ver reporte de coverage en terminal
pytest --cov=. --cov-report=term-missing
```

## 🚨 Solución de Problemas

### Error: "Database not found"
```bash
python manage.py migrate
pytest
```

### Error: "Factory dependencies"
Verificar que los factories importados existan:
```python
from organizations.factories import OrganizationFactory
```

### Error: "Constraint violations"
Los tests validan constraints reales de BD. Si fallan, revisar:
- Relaciones ForeignKey
- Campos únicos
- Validaciones de modelo

## 📝 Mejores Prácticas

1. **Un test, una responsabilidad** - Cada test valida un comportamiento específico
2. **Nombres descriptivos** - `test_create_user_with_custom_password`
3. **Factories sobre fixtures** - Más flexibles y reutilizables
4. **Datos realistas** - Contextualizados para el dominio
5. **Tests de constraints** - Validar reglas de negocio en BD
6. **Documentación en español** - Consistente con el proyecto

---

## 🎉 Estado Actual

✅ **Proyecto completamente testeado**  
✅ **70 tests pasando al 100%**  
✅ **Factories organizados y reutilizables**  
✅ **Cobertura del 73% del código**  
✅ **Documentación completa en español**  
✅ **Datos contextualizados para Nicaragua**  

El proyecto está listo para desarrollo y despliegue con confianza en la calidad del código.
