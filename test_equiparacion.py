#!/usr/bin/env python3
"""
Script de prueba para validar la funcionalidad de equiparación.
"""

import sys
sys.path.append('.')

from src.infrastructure.adapters.equiparacion_analyzer import EquiparacionAnalyzer

def test_equiparacion():
    """Prueba la funcionalidad de equiparación con un archivo de ejemplo."""
    
    # Seleccionar un archivo de prueba
    archivo_prueba = './salida/C04044-BRENDA JIMENEZ MIRANDA.xlsx'
    
    print("PRUEBA DE ANÁLISIS DE EQUIPARACIÓN")
    print("=" * 50)
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
            print("Verifique el archivo Excel para ver los resultados del análisis.")
        else:
            print("✗ Error durante el análisis")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    test_equiparacion()
