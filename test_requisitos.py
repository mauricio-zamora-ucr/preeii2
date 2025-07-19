#!/usr/bin/env python3
"""
Script para verificar que los requisitos se leen correctamente
"""

from src.infrastructure.adapters.excel_writer import ExcelWriter

def test_requisitos():
    print("🔍 Probando lectura de requisitos y correquisitos...")
    
    excel_writer = ExcelWriter()
    
    # Probar algunos cursos específicos mencionados
    cursos_test = ['II0703', 'II0602', 'II0603', 'II0704', 'MA1002', 'FS0210']
    
    for sigla in cursos_test:
        requisitos = excel_writer._obtener_requisitos_curso(sigla)
        correquisitos = excel_writer._obtener_correquisitos_curso(sigla)
        
        print(f"\n📚 {sigla}:")
        print(f"   Requisitos: {requisitos if requisitos else 'N/A'}")
        print(f"   Correquisitos: {correquisitos if correquisitos else 'N/A'}")

def test_excel_con_requisitos():
    print("\n🧪 Probando generación de Excel con requisitos corregidos...")
    
    from src.infrastructure.repositories.file_repository import FileRepository
    from src.application.services.expediente_service import ExpedienteService
    
    file_repo = FileRepository()
    expediente_service = ExpedienteService()
    
    archivos_expedientes = file_repo.listar_archivos_expedientes()
    
    if not archivos_expedientes:
        print("❌ No se encontraron expedientes para probar.")
        return
    
    # Probar con el primer archivo
    archivo = archivos_expedientes[0]
    carne = archivo.replace('.edf', '')
    
    try:
        # Leer información del estudiante
        carne_info, nombre = file_repo.leer_informacion_estudiante(carne)
        
        # Leer historial
        historial = file_repo.leer_historial(carne)
        
        # Procesar expediente
        expediente = expediente_service.procesar_expediente_estudiante(
            carne, nombre, historial
        )
        
        # Generar archivo Excel de prueba
        excel_writer = ExcelWriter()
        nombre_archivo = f'TEST-REQUISITOS-{expediente.carne}.xlsx'
        ruta_salida = file_repo.obtener_ruta_salida(nombre_archivo)
        
        print(f"📝 Generando Excel de prueba: {nombre_archivo}")
        excel_writer.generar_expediente(expediente, str(ruta_salida))
        
        print("✅ Excel generado exitosamente!")
        print(f"📁 Ubicación: {ruta_salida}")
        print("🔍 Revise la hoja 'Cursos Pendientes' para verificar requisitos")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_requisitos()
    test_excel_con_requisitos()
