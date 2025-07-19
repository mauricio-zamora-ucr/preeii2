#!/usr/bin/env python3
"""
Script para crear un archivo Excel de prueba con cursos de química aprobados.
"""

import sys
sys.path.append('.')

import xlsxwriter
from pathlib import Path

def crear_expediente_prueba():
    """Crea un expediente de prueba con cursos de química aprobados."""
    
    archivo_prueba = './salida/TEST-EQUIPARACION-CON-QUIMICA.xlsx'
    
    print("CREANDO EXPEDIENTE DE PRUEBA CON CURSOS DE QUÍMICA")
    print("=" * 60)
    print(f"Archivo: {archivo_prueba}")
    print()
    
    # Crear archivo Excel
    workbook = xlsxwriter.Workbook(archivo_prueba)
    
    # Crear hoja de historial académico
    worksheet = workbook.add_worksheet('Historial Académico')
    
    # Formatos
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'align': 'center'
    })
    
    # Encabezados
    headers = ['Código', 'Nombre del Curso', 'Créditos', 'Nota', 'Resultado']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    # Datos de cursos (incluyendo química aprobada)
    cursos_data = [
        ['MA0125', 'Precálculo', 4, 8.5, 'APR'],
        ['QU0100', 'Química General I', 4, 7.8, 'APR'],
        ['QU0102', 'Laboratorio de Química General I', 1, 8.2, 'APR'],
        ['QU0101', 'Química General II', 4, 7.3, 'APR'],
        ['QU0103', 'Laboratorio de Química General II', 1, 7.9, 'APR'],
        ['MA0151', 'Cálculo I', 4, 8.1, 'APR'],
        ['FI0151', 'Física General I', 4, 7.6, 'APR'],
        ['FI0153', 'Laboratorio de Física General I', 1, 8.0, 'APR']
    ]
    
    # Escribir datos
    for row, curso in enumerate(cursos_data, 1):
        for col, valor in enumerate(curso):
            worksheet.write(row, col, valor)
    
    # Ajustar ancho de columnas
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 35)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 8)
    worksheet.set_column('E:E', 12)
    
    workbook.close()
    
    print("✓ Expediente de prueba creado exitosamente")
    print()
    print("Cursos incluidos:")
    for curso in cursos_data:
        print(f"  • {curso[0]} - {curso[1]} (Nota: {curso[3]})")

if __name__ == "__main__":
    crear_expediente_prueba()
