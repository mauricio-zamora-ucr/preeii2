# Changelog - PreEII

## [2.2.1] - 2025-07-19

### 🔧 Corregido
- **Hoja "Cursos Pendientes"**: Solucionado problema donde requisitos y correquisitos aparecían como "N/A"
  - Corregida lectura de requisitos desde `config.py` 
  - Los cursos como II0703, II0602, II0603 ahora muestran correctamente sus requisitos
  - Cada requisito y correquisito se muestra individualmente con su estado
  - Mejorada visualización con códigos de color: ✓ (cumplido), ✗ (pendiente), ⚠️ (en matrícula)

### ✨ Mejorado
- **Análisis detallado de requisitos**: Cada requisito se evalúa por separado
- **Interfaz más clara**: Estado visual mejorado para identificación rápida
- **Resumen por curso**: Estadísticas de cursos matriculables vs bloqueados

---

## [2.2.0] - 2025-07-19

### ✨ Agregado - Nuevas Hojas de Análisis en Excel
- **4 nuevas hojas especializadas** para análisis académico avanzado:

#### 📈 **Hoja "Análisis por Semestres"**
- Estadísticas cronológicas por período académico (2024-1, 2024-2, etc.)
- Métricas de cursos: matriculados, aprobados, reprobados, en matrícula, retiros
- Métricas de créditos: totales por categoría de estado
- **Gráficos de línea automáticos**: evolución de cursos y créditos por tiempo
- Porcentaje de rendimiento por período

#### 📊 **Hoja "Progreso del Plan"**  
- Estado de avance por semestre del plan de estudios
- Desglose: cursos aprobados, reprobados, en matrícula, pendientes
- Porcentaje de progreso por semestre del plan
- Estado general: COMPLETADO, EN PROGRESO, PARCIAL, PENDIENTE
- Códigos de color para identificación rápida

#### ✅ **Hoja "Cursos Pendientes"**
- Lista de cursos que faltan por aprobar
- **Análisis automático de requisitos y correquisitos**
- Verificación si cumple requisitos (✓ Cumplido / ⏳ Pendiente)
- Indicador claro: "SÍ" o "NO" puede matricular cada curso
- Integración con configuración real de requisitos del plan

#### ⚠️ **Hoja "Cursos Reprobados"**
- Historial completo de cursos con problemas académicos
- Cronología de todos los intentos (reprobados y retiros)
- Detalles: período, año, grupo, estado, nota por intento  
- **Alertas automáticas** para cursos con 3+ intentos
- Observaciones y recomendaciones por intento

### 🔧 Mejorado
- **Integración con configuración**: Los requisitos se obtienen del archivo `config.py`
- **Gráficos automáticos**: Visualización de tendencias sin intervención manual
- **Códigos de color**: Identificación rápida del estado académico
- **Fallback inteligente**: Requisitos comunes si no están en configuración

### 🎯 Beneficios para Profesores
- **Análisis integral**: 7 perspectivas diferentes del expediente estudiantil
- **Guía de matrícula**: Identificación inmediata de cursos matriculables
- **Detección temprana**: Estudiantes con patrones de reprobación
- **Ahorro de tiempo**: Información procesada y lista para tomar decisiones

---

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
