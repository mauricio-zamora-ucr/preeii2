#!/usr/bin/env python3
"""
Script para probar la opción 4 del menú (regenerar Excel) sin interacción
"""

from src.presentation.console.menu_controller import MenuController
from src.infrastructure.repositories.file_repository import FileRepository
from src.application.services.expediente_service import ExpedienteService
from src.infrastructure.adapters.excel_writer import ExcelWriter

def test_regenerar_excel():
    print("🔧 Probando regeneración de archivos Excel...")
    
    file_repo = FileRepository()
    expediente_service = ExpedienteService()
    
    archivos_expedientes = file_repo.listar_archivos_expedientes()
    
    if not archivos_expedientes:
        print("❌ No se encontraron expedientes para procesar.")
        return
    
    print(f"📁 Se encontraron {len(archivos_expedientes)} expedientes para procesar.")
    
    # Procesar solo los primeros 3 archivos para la prueba
    archivos_prueba = archivos_expedientes[:3]
    print(f"🧪 Probando con {len(archivos_prueba)} archivos...")
    
    exitosos = 0
    errores = 0
    
    for i, archivo in enumerate(archivos_prueba, 1):
        try:
            # Leer información del estudiante
            carne = archivo.replace('.edf', '')
            carne_info, nombre = file_repo.leer_informacion_estudiante(carne)
            
            # Leer historial
            historial = file_repo.leer_historial(carne)
            
            # Procesar expediente
            expediente = expediente_service.procesar_expediente_estudiante(
                carne, nombre, historial
            )
            
            # Generar archivo Excel
            excel_writer = ExcelWriter()
            nombre_archivo = f'{expediente.carne}-{expediente.nombre.upper()}.xlsx'
            ruta_salida = file_repo.obtener_ruta_salida(nombre_archivo)
            excel_writer.generar_expediente(expediente, str(ruta_salida))
            
            print(f"[{i:2d}/{len(archivos_prueba)}] ✅ {carne} - {nombre[:30]}")
            exitosos += 1
            
        except Exception as e:
            print(f"[{i:2d}/{len(archivos_prueba)}] ❌ Error en {archivo}: {str(e)}")
            errores += 1
    
    print(f"\n📊 Resultados:")
    print(f"✅ Exitosos: {exitosos}")
    print(f"❌ Errores: {errores}")
    
    if errores == 0:
        print("🎉 ¡Regeneración de Excel completada exitosamente!")
        print("📝 Los archivos contienen 3 hojas:")
        print("   • Malla Curricular: Vista de mapa por semestres")
        print("   • Expediente Detallado: Vista tabular por semestres") 
        print("   • Historial Completo: Todos los registros académicos")
    else:
        print("⚠️  Algunos archivos tuvieron problemas durante la regeneración.")

if __name__ == "__main__":
    test_regenerar_excel()
