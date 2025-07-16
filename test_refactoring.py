"""
Pruebas básicas para validar el funcionamiento del sistema refactorizado
"""
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Prueba que los imports principales funcionen correctamente."""
    try:
        from src.domain.entities import Curso, CursoCarrera, Expediente, Semestre, Historial
        from src.application.services.expediente_service import ExpedienteService
        from src.infrastructure.repositories.file_repository import FileRepository
        from src.shared.config.settings import DETALLE_CURSOS
        print("✅ Todos los imports funcionan correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error en imports: {e}")
        return False

def test_entidades():
    """Prueba la creación de entidades básicas."""
    try:
        from src.domain.entities import Curso, Historial
        
        # Crear curso
        curso = Curso(
            sigla="MA1001",
            nombre="CÁLCULO I",
            creditos=3
        )
        assert curso.sigla == "MA1001"
        assert curso.creditos == 3
        
        # Crear historial
        historial = Historial(
            sigla="MA1001",
            sigla_normalizada="MA1001",
            nombre="CÁLCULO I",
            grupo=1,
            periodo=1,
            anno=2023,
            estado="APROBADO",
            nota="8.5"
        )
        assert historial.sigla == "MA1001"
        assert historial.anno == 2023
        
        print("✅ Creación de entidades exitosa")
        return True
    except Exception as e:
        print(f"❌ Error en entidades: {e}")
        return False

def test_expediente_service():
    """Prueba el servicio de expediente."""
    try:
        from src.application.services.expediente_service import ExpedienteService
        
        # Cargar cursos de carrera
        sigla_cursos, semestre_cursos, expediente = ExpedienteService.cargar_cursos_carrera()
        
        assert len(sigla_cursos) > 0
        assert len(semestre_cursos) > 0
        assert expediente is not None
        
        print(f"✅ Servicio de expediente funciona - {len(sigla_cursos)} cursos cargados")
        return True
    except Exception as e:
        print(f"❌ Error en servicio de expediente: {e}")
        return False

def test_file_repository():
    """Prueba el repositorio de archivos."""
    try:
        from src.infrastructure.repositories.file_repository import FileRepository
        
        file_repo = FileRepository()
        assert file_repo is not None
        
        # Verificar que los directorios se pueden crear
        file_repo._asegurar_directorio(file_repo.directorio_expedientes)
        
        print("✅ Repositorio de archivos funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en repositorio de archivos: {e}")
        return False

if __name__ == "__main__":
    print("Ejecutando pruebas básicas del sistema refactorizado...\n")
    
    pruebas = [
        test_imports,
        test_entidades,
        test_expediente_service,
        test_file_repository
    ]
    
    resultados = []
    for prueba in pruebas:
        resultado = prueba()
        resultados.append(resultado)
        print()
    
    exitosas = sum(resultados)
    total = len(resultados)
    
    print(f"Resumen: {exitosas}/{total} pruebas exitosas")
    
    if exitosas == total:
        print("🎉 Todas las pruebas pasaron exitosamente!")
        sys.exit(0)
    else:
        print("⚠️  Algunas pruebas fallaron")
        sys.exit(1)
