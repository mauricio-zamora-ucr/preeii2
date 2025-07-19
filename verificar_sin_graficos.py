#!/usr/bin/env python3
"""
Script para verificar que no hay gráficos en la hoja Análisis por Semestres.
"""

import openpyxl

def verificar_sin_graficos():
    """Verifica que la hoja Análisis por Semestres no tenga gráficos."""
    
    archivo = './salida/C04044-BRENDA JIMENEZ MIRANDA.xlsx'
    
    try:
        workbook = openpyxl.load_workbook(archivo)
        sheet = workbook['Análisis por Semestres']

        print('VERIFICACIÓN DE HOJA ANÁLISIS POR SEMESTRES:')
        print('=' * 50)

        # Verificar si hay gráficos
        charts = list(sheet._charts)
        if charts:
            print(f'⚠️  Se encontraron {len(charts)} gráfico(s)')
            for i, chart in enumerate(charts):
                print(f'   Gráfico {i+1}: {type(chart).__name__}')
        else:
            print('✅ No se encontraron gráficos - CORRECTO')

        print()
        print('CONTENIDO DE LA HOJA:')
        print('-' * 25)

        # Mostrar algunas celdas para confirmar que hay contenido
        for row_num in range(1, 11):
            for col_num in range(1, 6):
                cell_value = sheet.cell(row=row_num, column=col_num).value
                if cell_value:
                    print(f'Fila {row_num}, Columna {col_num}: {cell_value}')
                    break
            else:
                continue
            break

        workbook.close()
        
        print()
        print('✅ Verificación completada')
        
    except Exception as e:
        print(f'✗ Error: {str(e)}')

if __name__ == "__main__":
    verificar_sin_graficos()
