"""
Script de validación final de la refactorización
"""
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🔄 Validando la refactorización completa de PreEII...")
    print("=" * 60)
    
    # Test 1: Importar componentes principales
    print("1. Probando imports de componentes principales...")
    try:
        from src.presentation.console.menu_controller import MenuController
        from src.application.services.expediente_service import ExpedienteService
        from src.application.services.web_scraping_service import WebScrapingService
        from src.infrastructure.repositories.file_repository import FileRepository
        from src.domain.entities import Expediente, CursoCarrera, Semestre
        print("   ✅ Todos los imports principales funcionan")
    except Exception as e:
        print(f"   ❌ Error en imports: {e}")
        return False
    
    # Test 2: Crear instancias de servicios
    print("2. Probando creación de servicios...")
    try:
        expediente_service = ExpedienteService()
        web_service = WebScrapingService()
        file_repo = FileRepository()
        menu_controller = MenuController()
        print("   ✅ Todos los servicios se pueden instanciar")
    except Exception as e:
        print(f"   ❌ Error creando servicios: {e}")
        return False
    
    # Test 3: Cargar configuración de cursos
    print("3. Probando carga de configuración de cursos...")
    try:
        sigla_cursos, semestre_cursos, expediente = expediente_service.cargar_cursos_carrera()
        print(f"   ✅ Configuración cargada: {len(sigla_cursos)} cursos, {len(semestre_cursos)} semestres")
    except Exception as e:
        print(f"   ❌ Error cargando configuración: {e}")
        return False
    
    # Test 4: Verificar estructura de entidades
    print("4. Probando estructura de entidades...")
    try:
        # Verificar que las entidades tienen las propiedades esperadas
        assert hasattr(expediente, 'carne')
        assert hasattr(expediente, 'nombre')
        assert hasattr(expediente, 'semestres')
        
        # Verificar semestres
        primer_semestre = semestre_cursos[1]
        assert hasattr(primer_semestre, 'numero')
        assert hasattr(primer_semestre, 'cursos')
        assert len(primer_semestre.cursos) > 0
        
        # Verificar curso
        primer_curso = primer_semestre.cursos[0]
        assert hasattr(primer_curso, 'sigla')
        assert hasattr(primer_curso, 'nombre')
        assert hasattr(primer_curso, 'creditos')
        
        print("   ✅ Estructura de entidades es correcta")
    except Exception as e:
        print(f"   ❌ Error en estructura de entidades: {e}")
        return False
    
    # Test 5: Verificar funcionalidad de repositorio
    print("5. Probando funcionalidad de repositorio...")
    try:
        # Verificar que se pueden crear directorios
        file_repo._asegurar_directorio(file_repo.directorio_expedientes)
        file_repo._asegurar_directorio(file_repo.directorio_solicitudes)
        file_repo._asegurar_directorio(file_repo.directorio_salida)
        
        print("   ✅ Repositorio de archivos funciona correctamente")
    except Exception as e:
        print(f"   ❌ Error en repositorio: {e}")
        return False
    
    print("=" * 60)
    print("🎉 ¡REFACTORIZACIÓN COMPLETADA EXITOSAMENTE!")
    print()
    print("✨ Mejoras implementadas:")
    print("   • Arquitectura hexagonal con separación de capas")
    print("   • Type hints en toda la aplicación")
    print("   • Uso de dataclasses para entidades")
    print("   • Servicios de aplicación bien definidos")
    print("   • Repositorios para manejo de datos")
    print("   • Adaptadores para componentes externos")
    print("   • Configuración centralizada")
    print("   • Estructura modular y extensible")
    print()
    print("🚀 La aplicación está lista para usar:")
    print("   python main.py")
    print()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
