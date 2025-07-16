"""
Adaptador para generar archivos Excel
"""
import xlsxwriter
from typing import Dict
from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from ...domain.entities.expediente import Expediente


class ExcelWriter:
    """
    Adaptador para generar archivos Excel con información de expedientes.
    """

    def __init__(self):
        """Inicializa el escritor de Excel."""
        pass

    def generar_expediente(self, expediente: Expediente, ruta_archivo: str) -> None:
        """
        Genera un archivo Excel con la información del expediente.
        
        Args:
            expediente: Expediente del estudiante
            ruta_archivo: Ruta donde guardar el archivo Excel
        """
        workbook = xlsxwriter.Workbook(ruta_archivo)
        worksheet = workbook.add_worksheet('malla')
        worksheet.hide_gridlines(2)

        # Generar formatos
        formatos = self._generar_formatos(workbook)
        
        # Escribir encabezado
        fila, columna = self._escribir_encabezado_expediente(
            expediente, workbook, worksheet, 0, 0, formatos
        )
        
        # Escribir contenido del expediente
        self._escribir_expediente(expediente, workbook, worksheet, fila, columna, formatos)
        
        workbook.close()

    def _generar_formatos(self, workbook: Workbook) -> Dict[str, Format]:
        """
        Genera los formatos de celda para el archivo Excel.
        
        Args:
            workbook: Libro de Excel
        
        Returns:
            Diccionario con los formatos disponibles
        """
        formatos = {}
        
        # Formato para encabezados
        formatos['encabezado'] = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#D7E4BC',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        # Formato para información del estudiante
        formatos['info_estudiante'] = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'bg_color': '#F2F2F2',
            'border': 1
        })
        
        # Formato para cursos aprobados
        formatos['curso_aprobado'] = workbook.add_format({
            'bg_color': '#C6EFCE',
            'border': 1,
            'font_size': 10
        })
        
        # Formato para cursos matriculados
        formatos['curso_matriculado'] = workbook.add_format({
            'bg_color': '#FFEB9C',
            'border': 1,
            'font_size': 10
        })
        
        # Formato para cursos reprobados
        formatos['curso_reprobado'] = workbook.add_format({
            'bg_color': '#FFC7CE',
            'border': 1,
            'font_size': 10
        })
        
        # Formato para cursos sin datos
        formatos['curso_sin_datos'] = workbook.add_format({
            'bg_color': '#F2F2F2',
            'border': 1,
            'font_size': 10
        })
        
        # Formato para números
        formatos['numero'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'font_size': 10
        })
        
        # Formato para texto centrado
        formatos['texto_centrado'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'font_size': 10
        })
        
        return formatos

    def _escribir_encabezado_expediente(
        self, 
        expediente: Expediente, 
        workbook: Workbook, 
        worksheet: Worksheet, 
        fila_inicial: int, 
        columna_inicial: int, 
        formatos: Dict[str, Format]
    ) -> tuple[int, int]:
        """
        Escribe el encabezado del expediente en el archivo Excel.
        
        Args:
            expediente: Expediente del estudiante
            workbook: Libro de Excel
            worksheet: Hoja de trabajo
            fila_inicial: Fila inicial para escribir
            columna_inicial: Columna inicial para escribir
            formatos: Diccionario de formatos
        
        Returns:
            Tupla con (fila_siguiente, columna_siguiente)
        """
        fila = fila_inicial
        
        # Título principal
        worksheet.merge_range(fila, 0, fila, 7, 'EXPEDIENTE ACADÉMICO', formatos['encabezado'])
        fila += 1
        
        # Información del estudiante
        worksheet.write(fila, 0, 'Carné:', formatos['info_estudiante'])
        worksheet.write(fila, 1, expediente.carne, formatos['info_estudiante'])
        worksheet.write(fila, 3, 'Nombre:', formatos['info_estudiante'])
        worksheet.merge_range(fila, 4, fila, 7, expediente.nombre, formatos['info_estudiante'])
        fila += 2
        
        # Encabezados de columnas
        encabezados = ['Semestre', 'Sigla', 'Curso', 'Créditos', 'Estado', 'Nota', 'Año', 'Período']
        for i, encabezado in enumerate(encabezados):
            worksheet.write(fila, i, encabezado, formatos['encabezado'])
        
        return fila + 1, columna_inicial

    def _escribir_expediente(
        self, 
        expediente: Expediente, 
        workbook: Workbook, 
        worksheet: Worksheet, 
        fila_inicial: int, 
        columna_inicial: int, 
        formatos: Dict[str, Format]
    ) -> None:
        """
        Escribe el contenido del expediente en el archivo Excel.
        
        Args:
            expediente: Expediente del estudiante
            workbook: Libro de Excel
            worksheet: Hoja de trabajo
            fila_inicial: Fila inicial para escribir
            columna_inicial: Columna inicial para escribir
            formatos: Diccionario de formatos
        """
        fila = fila_inicial
        
        # Iterar por semestres ordenados
        for numero_semestre in sorted(expediente.semestres.keys()):
            semestre = expediente.semestres[numero_semestre]
            
            for curso in semestre.cursos:
                # Determinar formato según estado
                formato_curso = self._obtener_formato_curso(curso.get_estado_actual(), formatos)
                
                # Escribir datos del curso
                worksheet.write(fila, 0, numero_semestre, formato_curso)
                worksheet.write(fila, 1, curso.sigla, formato_curso)
                worksheet.write(fila, 2, curso.nombre, formato_curso)
                worksheet.write(fila, 3, curso.creditos, formato_curso)
                worksheet.write(fila, 4, curso.get_estado_actual(), formato_curso)
                worksheet.write(fila, 5, curso.get_nota_actual(), formato_curso)
                worksheet.write(fila, 6, curso.get_anno_actual() or '', formato_curso)
                worksheet.write(fila, 7, curso.get_periodo_actual() or '', formato_curso)
                
                fila += 1
        
        # Ajustar ancho de columnas
        worksheet.set_column(0, 0, 10)  # Semestre
        worksheet.set_column(1, 1, 12)  # Sigla
        worksheet.set_column(2, 2, 50)  # Curso
        worksheet.set_column(3, 3, 10)  # Créditos
        worksheet.set_column(4, 4, 15)  # Estado
        worksheet.set_column(5, 5, 8)   # Nota
        worksheet.set_column(6, 6, 8)   # Año
        worksheet.set_column(7, 7, 10)  # Período

    def _obtener_formato_curso(self, estado: str, formatos: Dict[str, Format]) -> Format:
        """
        Obtiene el formato apropiado según el estado del curso.
        
        Args:
            estado: Estado del curso
            formatos: Diccionario de formatos disponibles
        
        Returns:
            Formato correspondiente al estado
        """
        if estado in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO']:
            return formatos['curso_aprobado']
        elif estado == 'MATRICULADO':
            return formatos['curso_matriculado']
        elif estado == 'REPROBADO':
            return formatos['curso_reprobado']
        else:
            return formatos['curso_sin_datos']
