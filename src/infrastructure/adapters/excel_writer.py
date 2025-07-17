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
        Genera un archivo Excel con la información completa del expediente.
        
        Args:
            expediente: Expediente del estudiante
            ruta_archivo: Ruta donde guardar el archivo Excel
        """
        workbook = xlsxwriter.Workbook(ruta_archivo)
        
        # Generar formatos una vez para todas las hojas
        formatos = self._generar_formatos(workbook)
        
        # Hoja 1: Malla curricular (formato original de mapa)
        self._generar_hoja_malla(workbook, expediente, formatos)
        
        # Hoja 2: Expediente detallado (formato nuevo)
        self._generar_hoja_expediente(workbook, expediente, formatos)
        
        # Hoja 3: Historial completo
        self._generar_hoja_historial(workbook, expediente, formatos)
        
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
            formatos: Diccionario de formatos
            
        Returns:
            Formato a aplicar
        """
        if estado in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO']:
            return formatos['curso_aprobado']
        elif estado == 'REPROBADO':
            return formatos['curso_reprobado']
        elif estado == 'MATRICULADO':
            return formatos['curso_matriculado']
        else:
            return formatos['curso_sin_datos']
    
    def _generar_hoja_malla(self, workbook: Workbook, expediente: Expediente, formatos: Dict[str, Format]) -> None:
        """
        Genera la hoja con el formato de malla curricular (formato de mapa).
        
        Args:
            workbook: Libro de Excel
            expediente: Expediente del estudiante
            formatos: Diccionario de formatos
        """
        worksheet = workbook.add_worksheet('Malla Curricular')
        worksheet.hide_gridlines(2)
        
        # Escribir información del estudiante
        fila = 0
        worksheet.merge_range(fila, 0, fila, 11, 'MALLA CURRICULAR', formatos['encabezado'])
        fila += 1
        
        worksheet.write(fila, 0, 'Carné:', formatos['info_estudiante'])
        worksheet.write(fila, 1, expediente.carne, formatos['info_estudiante'])
        worksheet.write(fila, 4, 'Nombre:', formatos['info_estudiante'])
        worksheet.merge_range(fila, 5, fila, 11, expediente.nombre, formatos['info_estudiante'])
        fila += 2
        
        # Calcular estadísticas
        total_creditos_carrera = sum(
            curso.creditos for semestre in expediente.semestres.values() 
            for curso in semestre.cursos
        )
        creditos_aprobados = sum(
            curso.creditos for semestre in expediente.semestres.values() 
            for curso in semestre.cursos if curso.esta_aprobado()
        )
        
        # Información de progreso
        worksheet.write(fila, 0, 'Total Créditos Carrera:', formatos['info_estudiante'])
        worksheet.write(fila, 1, total_creditos_carrera, formatos['numero'])
        worksheet.write(fila, 4, 'Créditos Aprobados:', formatos['info_estudiante'])
        worksheet.write(fila, 5, creditos_aprobados, formatos['numero'])
        worksheet.write(fila, 7, 'Porcentaje:', formatos['info_estudiante'])
        porcentaje = (creditos_aprobados / total_creditos_carrera * 100) if total_creditos_carrera > 0 else 0
        worksheet.write(fila, 8, f'{porcentaje:.1f}%', formatos['numero'])
        fila += 2
        
        # Crear malla por semestres (formato de mapa)
        semestres_por_fila = 4  # 4 semestres por fila
        semestres_ordenados = sorted(expediente.semestres.keys())
        
        for i in range(0, len(semestres_ordenados), semestres_por_fila):
            fila_actual = fila
            
            # Encabezados de semestres
            for j in range(semestres_por_fila):
                if i + j < len(semestres_ordenados):
                    sem_num = semestres_ordenados[i + j]
                    col_inicio = j * 3
                    worksheet.merge_range(fila_actual, col_inicio, fila_actual, col_inicio + 2, 
                                        f'SEMESTRE {sem_num}', formatos['encabezado'])
            
            fila_actual += 1
            
            # Encontrar el máximo número de cursos en los semestres de esta fila
            max_cursos = 0
            for j in range(semestres_por_fila):
                if i + j < len(semestres_ordenados):
                    sem_num = semestres_ordenados[i + j]
                    max_cursos = max(max_cursos, len(expediente.semestres[sem_num].cursos))
            
            # Escribir cursos
            for k in range(max_cursos):
                for j in range(semestres_por_fila):
                    if i + j < len(semestres_ordenados):
                        sem_num = semestres_ordenados[i + j]
                        semestre = expediente.semestres[sem_num]
                        col_inicio = j * 3
                        
                        if k < len(semestre.cursos):
                            curso = semestre.cursos[k]
                            formato_curso = self._obtener_formato_curso(curso.get_estado_actual(), formatos)
                            
                            # Sigla
                            worksheet.write(fila_actual, col_inicio, curso.sigla, formato_curso)
                            # Nombre (resumido)
                            nombre_corto = curso.nombre[:25] + '...' if len(curso.nombre) > 25 else curso.nombre
                            worksheet.write(fila_actual, col_inicio + 1, nombre_corto, formato_curso)
                            # Créditos
                            worksheet.write(fila_actual, col_inicio + 2, curso.creditos, formato_curso)
                        else:
                            # Celdas vacías
                            for col_offset in range(3):
                                worksheet.write(fila_actual, col_inicio + col_offset, '', formatos['curso_sin_datos'])
                
                fila_actual += 1
            
            fila = fila_actual + 1  # Espacio entre filas de semestres
        
        # Ajustar anchos de columnas
        for i in range(12):
            if i % 3 == 0:  # Columnas de sigla
                worksheet.set_column(i, i, 8)
            elif i % 3 == 1:  # Columnas de nombre
                worksheet.set_column(i, i, 30)
            else:  # Columnas de créditos
                worksheet.set_column(i, i, 6)

    def _generar_hoja_expediente(self, workbook: Workbook, expediente: Expediente, formatos: Dict[str, Format]) -> None:
        """
        Genera la hoja con el expediente detallado (formato nuevo).
        
        Args:
            workbook: Libro de Excel
            expediente: Expediente del estudiante
            formatos: Diccionario de formatos
        """
        worksheet = workbook.add_worksheet('Expediente Detallado')
        worksheet.hide_gridlines(2)

        # Escribir encabezado
        fila, columna = self._escribir_encabezado_expediente(
            expediente, workbook, worksheet, 0, 0, formatos
        )
        
        # Escribir contenido del expediente
        self._escribir_expediente(expediente, workbook, worksheet, fila, columna, formatos)

    def _generar_hoja_historial(self, workbook: Workbook, expediente: Expediente, formatos: Dict[str, Format]) -> None:
        """
        Genera la hoja con el historial completo de todos los cursos.
        
        Args:
            workbook: Libro de Excel
            expediente: Expediente del estudiante
            formatos: Diccionario de formatos
        """
        worksheet = workbook.add_worksheet('Historial Completo')
        worksheet.hide_gridlines(2)
        
        fila = 0
        
        # Título principal
        worksheet.merge_range(fila, 0, fila, 8, 'HISTORIAL ACADÉMICO COMPLETO', formatos['encabezado'])
        fila += 1
        
        # Información del estudiante
        worksheet.write(fila, 0, 'Carné:', formatos['info_estudiante'])
        worksheet.write(fila, 1, expediente.carne, formatos['info_estudiante'])
        worksheet.write(fila, 3, 'Nombre:', formatos['info_estudiante'])
        worksheet.merge_range(fila, 4, fila, 8, expediente.nombre, formatos['info_estudiante'])
        fila += 2
        
        # Encabezados de columnas
        encabezados = ['Sigla', 'Curso', 'Créditos', 'Grupo', 'Período', 'Año', 'Estado', 'Nota', 'Semestre Plan']
        for i, encabezado in enumerate(encabezados):
            worksheet.write(fila, i, encabezado, formatos['encabezado'])
        fila += 1
        
        # Recopilar todo el historial
        todo_historial = []
        
        for numero_semestre in sorted(expediente.semestres.keys()):
            semestre = expediente.semestres[numero_semestre]
            for curso in semestre.cursos:
                if curso.historial:
                    # Si el curso tiene historial, agregar cada registro
                    for registro in curso.historial:
                        todo_historial.append({
                            'sigla': registro.sigla,
                            'nombre': registro.nombre,
                            'creditos': curso.creditos,
                            'grupo': registro.grupo,
                            'periodo': registro.periodo,
                            'anno': registro.anno,
                            'estado': registro.estado,
                            'nota': registro.nota or '',
                            'semestre_plan': numero_semestre
                        })
                else:
                    # Si no tiene historial, agregar con datos del curso
                    todo_historial.append({
                        'sigla': curso.sigla,
                        'nombre': curso.nombre,
                        'creditos': curso.creditos,
                        'grupo': '',
                        'periodo': '',
                        'anno': '',
                        'estado': curso.get_estado_actual(),
                        'nota': curso.get_nota_actual(),
                        'semestre_plan': numero_semestre
                    })
        
        # Ordenar por año, período, sigla
        todo_historial.sort(key=lambda x: (x['anno'] or 0, x['periodo'] or 0, x['sigla']))
        
        # Escribir historial
        for registro in todo_historial:
            formato_fila = self._obtener_formato_curso(registro['estado'], formatos)
            
            worksheet.write(fila, 0, registro['sigla'], formato_fila)
            worksheet.write(fila, 1, registro['nombre'], formato_fila)
            worksheet.write(fila, 2, registro['creditos'], formato_fila)
            worksheet.write(fila, 3, registro['grupo'], formato_fila)
            worksheet.write(fila, 4, registro['periodo'], formato_fila)
            worksheet.write(fila, 5, registro['anno'], formato_fila)
            worksheet.write(fila, 6, registro['estado'], formato_fila)
            worksheet.write(fila, 7, registro['nota'], formato_fila)
            worksheet.write(fila, 8, registro['semestre_plan'], formato_fila)
            
            fila += 1
        
        # Estadísticas finales
        fila += 1
        cursos_aprobados = len([r for r in todo_historial if r['estado'] in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO']])
        cursos_reprobados = len([r for r in todo_historial if r['estado'] == 'REPROBADO'])
        cursos_matriculados = len([r for r in todo_historial if r['estado'] == 'MATRICULADO'])
        
        worksheet.write(fila, 0, 'RESUMEN:', formatos['encabezado'])
        fila += 1
        worksheet.write(fila, 0, f'Cursos Aprobados: {cursos_aprobados}', formatos['info_estudiante'])
        fila += 1
        worksheet.write(fila, 0, f'Cursos Reprobados: {cursos_reprobados}', formatos['info_estudiante'])
        fila += 1
        worksheet.write(fila, 0, f'Cursos Matriculados: {cursos_matriculados}', formatos['info_estudiante'])
        
        # Ajustar ancho de columnas
        worksheet.set_column(0, 0, 10)  # Sigla
        worksheet.set_column(1, 1, 50)  # Curso
        worksheet.set_column(2, 2, 10)  # Créditos
        worksheet.set_column(3, 3, 8)   # Grupo
        worksheet.set_column(4, 4, 10)  # Período
        worksheet.set_column(5, 5, 8)   # Año
        worksheet.set_column(6, 6, 15)  # Estado
        worksheet.set_column(7, 7, 8)   # Nota
        worksheet.set_column(8, 8, 12)  # Semestre Plan
