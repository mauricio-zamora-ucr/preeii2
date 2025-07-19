#!/usr/bin/env python3
"""
Script para regenerar un expediente y probar las mejoras.
"""

import sys
sys.path.append('.')

from src.infrastructure.adapters.excel_writer import ExcelWriter
from src.infrastructure.repositories.file_repository import FileRepository
from src.application.services.expediente_service import ExpedienteService

def regenerar_expediente_prueba():
    """Regenera un expediente para probar las mejoras."""
    
    print("REGENERANDO EXPEDIENTE PARA PROBAR MEJORAS")
    print("=" * 50)
    
    try:
        # Seleccionar expediente
        carne = "C04044"
        archivo_edf = f"./expediente/{carne}.edf"
        archivo_sdf = f"./expediente/{carne}.sdf"
        
        print(f"Procesando expediente: {carne}")
        
        # Crear servicios
        expediente_service = ExpedienteService()
        
        # Procesar expediente
        resultado = expediente_service.procesar_expediente_estudiante(
            ruta_edf=archivo_edf,
            ruta_sdf=archivo_sdf,
            directorio_salida="./salida"
        )
        
        if resultado:
            print("✓ Expediente regenerado exitosamente")
            print("✓ Gráfico simplificado aplicado en 'Análisis por Semestres'")
            print("✓ Estados mejorados en hoja 'Equiparación'")
            print()
            print("Verifique el archivo Excel para ver:")
            print("  • Hoja 'Análisis por Semestres': Un solo gráfico de rendimiento")
            print("  • Hoja 'Equiparación': Estados detallados de cursos")
        else:
            print("✗ Error regenerando expediente")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    regenerar_expediente_prueba()
