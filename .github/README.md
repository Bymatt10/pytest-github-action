# GitHub Actions para Tests

Este proyecto incluye configuración de GitHub Actions para ejecutar automáticamente los tests de pytest.

## Workflows Configurados

### 1. Tests Completos (`test.yml`)
- **Cuándo se ejecuta**: En push y pull requests a las ramas `main` y `develop`
- **Qué hace**: 
  - Ejecuta tests en múltiples versiones de Python (3.10, 3.11, 3.12)
  - Instala dependencias y ejecuta migraciones
  - Ejecuta todos los tests con cobertura
  - Sube reportes de cobertura a Codecov

### 2. Tests Rápidos (`quick-test.yml`)
- **Cuándo se ejecuta**: 
  - Manualmente desde la interfaz de GitHub
  - En push cuando se modifican archivos Python
- **Qué hace**:
  - Ejecuta solo en Python 3.11
  - Ejecuta solo tests unitarios (excluye tests lentos e integración)
  - Más rápido para validaciones rápidas

## Configuración Automática

Los workflows están configurados para:
- ✅ Usar caché para dependencias (más rápido)
- ✅ Configurar variables de entorno necesarias
- ✅ Ejecutar migraciones de Django
- ✅ Usar la configuración de pytest del proyecto (pytest.ini)
- ✅ Generar reportes de cobertura

## Marcadores de Tests

El proyecto usa marcadores de pytest que puedes usar localmente:

```bash
# Ejecutar solo tests unitarios
pytest -m "unit"

# Ejecutar solo tests de integración  
pytest -m "integration"

# Excluir tests lentos
pytest -m "not slow"

# Combinar marcadores
pytest -m "not slow and not integration"
```

## Variables de Entorno

Los workflows configuran automáticamente:
- `SECRET_KEY`: Clave secreta para tests
- `DEBUG`: True para entorno de testing
- `DATABASE`: sqlite para usar base de datos en memoria

## Ejecución Manual

Puedes ejecutar el workflow "Quick Tests" manualmente:
1. Ve a la pestaña "Actions" en GitHub
2. Selecciona "Quick Tests"
3. Haz clic en "Run workflow"

## Cobertura de Código

Los reportes de cobertura se generan automáticamente y se pueden ver en:
- Artifacts de GitHub Actions (archivos HTML y XML)
- Codecov (si está configurado)

## Troubleshooting

Si los tests fallan:
1. Verifica que todas las dependencias estén en `requirements.txt`
2. Asegúrate de que los tests pasen localmente con `pytest`
3. Revisa los logs en la pestaña "Actions" de GitHub
