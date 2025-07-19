#!/usr/bin/env python3
"""
Script de prueba para validar el análisis positivo de equiparación.
"""

import sys
sys.path.append('.')

from src.infrastructure.adapters.equiparacion_analyzer import EquiparacionAnalyzer

def test_equiparacion_positiva():
    """Prueba la funcionalidad de equiparación con un expediente que tiene química aprobada."""
    
    # Archivo con cursos de química aprobados
    archivo_prueba = './salida/TEST-EQUIPARACION-CON-QUIMICA.xlsx'
    
    print("PRUEBA DE ANÁLISIS DE EQUIPARACIÓN - CASO POSITIVO")
    print("=" * 60)
    print(f"Archivo de prueba: {archivo_prueba}")
    print()
    
    try:
        # Crear analizador
        analyzer = EquiparacionAnalyzer()
        
        # Realizar análisis
        resultado = analyzer.analizar_expediente(archivo_prueba)
        
        if resultado:
            print("✓ Análisis completado exitosamente")
            print("✓ Se agregó la hoja 'Equiparación' al archivo Excel")
            print()
            print("Este expediente debería mostrar:")
            print("  • Química General Intensiva I: ✓ COMPLETA")
            print("  • Química General Intensiva II: ✓ COMPLETA") 
            print("  • Precálculo: ✓ APROBADO")
            print("  • Equivalencias identificadas")
            print("  • Recomendaciones positivas")
        else:
            print("✗ Error durante el análisis")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_equiparacion_positiva()
