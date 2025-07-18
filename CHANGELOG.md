# Changelog - PreEII

## [2.1.0] - 2025-07-18

### ✅ Corregido
- **Problema crítico de codificación**: Resuelto el error `'utf-8' codec can't decode byte 0xd1 in position 32: invalid continuation byte`
  - Implementado manejo automático de múltiples codificaciones (utf-8, latin-1, cp1252, iso-8859-1)
  - Los archivos existentes ahora se leen correctamente sin importar su codificación original
  - Los nuevos archivos se guardan en latin-1 para máxima compatibilidad

- **Error de web scraping**: Corregido el problema "too many values to unpack (expected 4)" en la opción 1
  - Modificado el procesamiento para manejar listas de estudiantes de longitud variable
  - El sistema ahora es más robusto contra cambios en el formato de datos del sitio web

### ✨ Agregado
- **Opción 4: Regenerar archivos Excel**: Nueva funcionalidad para regenerar archivos Excel desde expedientes existentes
  - Permite regenerar todos los archivos sin necesidad de descargar nuevamente
  - Útil para aplicar mejoras en el formato Excel a expedientes ya descargados
  - Incluye barra de progreso y manejo de errores

### 🔧 Mejorado
- **Archivos Excel con 3 hojas**:
  - **Hoja 1: "Malla Curricular"** - Formato visual de mapa por semestres (formato original)
  - **Hoja 2: "Expediente Detallado"** - Vista tabular organizada por semestres
  - **Hoja 3: "Historial Completo"** - Todos los registros académicos con estadísticas

- **Manejo de errores**: Mejorado el manejo de errores en lectura de archivos
- **Compatibilidad**: Mejor compatibilidad entre sistemas operativos (Windows/macOS/Linux)

### 🧪 Probado
- ✅ Web scraping funciona correctamente (39 estudiantes procesados sin errores)
- ✅ Lectura de archivos con múltiples codificaciones
- ✅ Regeneración de archivos Excel (40 expedientes procesados exitosamente)
- ✅ Todas las pruebas de validación pasan (5/5)

---

## [2.0.0] - 2025-07-17

### ✨ Refactorización Completa
- **Arquitectura hexagonal**: Separación clara en capas (domain/application/infrastructure/presentation)
- **Type hints**: Implementación completa de tipado estático en Python
- **Dataclasses**: Uso de dataclasses para entidades del dominio
- **SOLID**: Aplicación de principios SOLID en el diseño
- **Servicios de aplicación**: Lógica de negocio bien encapsulada
- **Repositorios**: Patrón Repository para manejo de datos
- **Adaptadores**: Patrón Adapter para componentes externos

### 🗂️ Estructura del Proyecto
```
src/
├── domain/entities/          # Entidades del negocio
├── application/services/     # Servicios de aplicación  
├── infrastructure/          
│   ├── adapters/            # Adaptadores externos
│   └── repositories/        # Repositorios de datos
├── presentation/console/     # Interfaz de usuario
└── shared/config/           # Configuración compartida
```

### 📦 Dependencias
- xlsxwriter: Generación de archivos Excel
- requests: Cliente HTTP para web scraping
- termcolor: Colores en consola
- pyperclip: Manejo del portapapeles
- urllib3: Utilidades HTTP

---

## [1.x] - Versiones Anteriores

### Características Históricas
- Script original en Python 2
- Plantillas de Excel estáticas
- Procesamiento manual uno por uno
- Interfaz de consola básica
