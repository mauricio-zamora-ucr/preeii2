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
        
        # Hojas originales
        self._generar_hoja_malla(workbook, expediente, formatos)
        self._generar_hoja_expediente(workbook, expediente, formatos)
        self._generar_hoja_historial(workbook, expediente, formatos)
        
        # Nuevas hojas de análisis
        self._generar_hoja_analisis_semestres(workbook, expediente, formatos)
        self._generar_hoja_progreso_plan(workbook, expediente, formatos)
        self._generar_hoja_cursos_pendientes(workbook, expediente, formatos)
        self._generar_hoja_cursos_reprobados(workbook, expediente, formatos)
        
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
        
        # Formatos adicionales para nuevas hojas
        formatos['requisito_cumplido'] = workbook.add_format({
            'bg_color': '#C6EFCE',
            'border': 1,
            'align': 'center',
            'font_size': 9
        })
        
        formatos['requisito_pendiente'] = workbook.add_format({
            'bg_color': '#FFEB9C',
            'border': 1,
            'align': 'center',
            'font_size': 9
        })
        
        formatos['curso_pendiente'] = workbook.add_format({
            'bg_color': '#E6E6FA',
            'border': 1,
            'font_size': 10
        })
        
        formatos['numero_grande'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'font_size': 12,
            'bold': True
        })
        
        formatos['porcentaje'] = workbook.add_format({
            'border': 1,
            'align': 'center',
            'font_size': 10,
            'num_format': '0.0%'
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

    def _generar_hoja_analisis_semestres(self, workbook: Workbook, expediente: Expediente, formatos: Dict[str, Format]) -> None:
        """
        Genera la hoja de análisis por semestres cronológicos.
        
        Args:
            workbook: Libro de Excel
            expediente: Expediente del estudiante
            formatos: Diccionario de formatos
        """
        worksheet = workbook.add_worksheet('Análisis por Semestres')
        worksheet.hide_gridlines(2)
        
        fila = 0
        
        # Título principal
        worksheet.merge_range(fila, 0, fila, 11, 'ANÁLISIS DE RENDIMIENTO POR SEMESTRES', formatos['encabezado'])
        fila += 1
        
        # Información del estudiante
        worksheet.write(fila, 0, 'Carné:', formatos['info_estudiante'])
        worksheet.write(fila, 1, expediente.carne, formatos['info_estudiante'])
        worksheet.write(fila, 3, 'Nombre:', formatos['info_estudiante'])
        worksheet.merge_range(fila, 4, fila, 11, expediente.nombre, formatos['info_estudiante'])
        fila += 2
        
        # Recopilar datos por período cronológico
        periodos_cronologicos = {}
        
        for semestre in expediente.semestres.values():
            for curso in semestre.cursos:
                if curso.historial:
                    for registro in curso.historial:
                        if registro.anno and registro.periodo:
                            periodo_key = f"{registro.anno}-{registro.periodo}"
                            
                            if periodo_key not in periodos_cronologicos:
                                periodos_cronologicos[periodo_key] = {
                                    'año': registro.anno,
                                    'periodo': registro.periodo,
                                    'cursos_matriculados': 0,
                                    'cursos_aprobados': 0,
                                    'cursos_reprobados': 0,
                                    'cursos_en_matricula': 0,
                                    'cursos_retiro': 0,
                                    'creditos_matriculados': 0,
                                    'creditos_aprobados': 0,
                                    'creditos_reprobados': 0,
                                    'creditos_en_matricula': 0,
                                    'creditos_retiro': 0
                                }
                            
                            periodo = periodos_cronologicos[periodo_key]
                            periodo['cursos_matriculados'] += 1
                            periodo['creditos_matriculados'] += curso.creditos
                            
                            if registro.estado in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO']:
                                periodo['cursos_aprobados'] += 1
                                periodo['creditos_aprobados'] += curso.creditos
                            elif registro.estado == 'REPROBADO':
                                periodo['cursos_reprobados'] += 1
                                periodo['creditos_reprobados'] += curso.creditos
                            elif registro.estado == 'MATRICULADO':
                                periodo['cursos_en_matricula'] += 1
                                periodo['creditos_en_matricula'] += curso.creditos
                            elif 'RETIRO' in registro.estado:
                                periodo['cursos_retiro'] += 1
                                periodo['creditos_retiro'] += curso.creditos
        
        # Ordenar períodos cronológicamente
        periodos_ordenados = sorted(periodos_cronologicos.items(), 
                                  key=lambda x: (x[1]['año'], x[1]['periodo']))
        
        # Encabezados
        encabezados = [
            'Período', 'Total Cursos', 'Aprobados', 'Reprobados', 'En Matrícula', 'Retiros',
            'Total Créditos', 'Créditos Aprob.', 'Créditos Reprob.', 'Créditos Matr.', 'Créditos Retiro', 'Rendimiento %'
        ]
        
        for i, encabezado in enumerate(encabezados):
            worksheet.write(fila, i, encabezado, formatos['encabezado'])
        fila += 1
        
        # Datos por período
        datos_graficos = []
        
        for periodo_key, datos in periodos_ordenados:
            rendimiento = (datos['cursos_aprobados'] / datos['cursos_matriculados'] * 100) if datos['cursos_matriculados'] > 0 else 0
            
            worksheet.write(fila, 0, periodo_key, formatos['texto_centrado'])
            worksheet.write(fila, 1, datos['cursos_matriculados'], formatos['numero'])
            worksheet.write(fila, 2, datos['cursos_aprobados'], formatos['numero'])
            worksheet.write(fila, 3, datos['cursos_reprobados'], formatos['numero'])
            worksheet.write(fila, 4, datos['cursos_en_matricula'], formatos['numero'])
            worksheet.write(fila, 5, datos['cursos_retiro'], formatos['numero'])
            worksheet.write(fila, 6, datos['creditos_matriculados'], formatos['numero'])
            worksheet.write(fila, 7, datos['creditos_aprobados'], formatos['numero'])
            worksheet.write(fila, 8, datos['creditos_reprobados'], formatos['numero'])
            worksheet.write(fila, 9, datos['creditos_en_matricula'], formatos['numero'])
            worksheet.write(fila, 10, datos['creditos_retiro'], formatos['numero'])
            worksheet.write(fila, 11, rendimiento/100, formatos['porcentaje'])
            
            datos_graficos.append({
                'periodo': periodo_key,
                'cursos_total': datos['cursos_matriculados'],
                'creditos_total': datos['creditos_matriculados'],
                'rendimiento': rendimiento
            })
            
            fila += 1
        
        # Crear gráficos si hay datos
        if datos_graficos:
            self._crear_graficos_rendimiento(workbook, worksheet, datos_graficos, fila + 2)
        
        # Ajustar ancho de columnas
        worksheet.set_column(0, 0, 12)  # Período
        worksheet.set_column(1, 11, 10)  # Resto de columnas

    def _crear_graficos_rendimiento(self, workbook: Workbook, worksheet, datos_graficos: list, fila_inicio: int) -> None:
        """
        Crea gráficos de línea para visualizar el rendimiento.
        
        Args:
            workbook: Libro de Excel
            worksheet: Hoja de trabajo
            datos_graficos: Datos para los gráficos
            fila_inicio: Fila donde insertar los gráficos
        """
        # Gráfico 1: Cursos por período
        chart_cursos = workbook.add_chart({'type': 'line'})
        chart_cursos.add_series({
            'name': 'Cursos Matriculados',
            'categories': [worksheet.name, 4, 0, 3 + len(datos_graficos), 0],
            'values': [worksheet.name, 4, 1, 3 + len(datos_graficos), 1],
            'line': {'color': '#1f77b4', 'width': 3}
        })
        
        chart_cursos.set_title({'name': 'Evolución de Cursos por Período'})
        chart_cursos.set_x_axis({'name': 'Período'})
        chart_cursos.set_y_axis({'name': 'Número de Cursos'})
        chart_cursos.set_size({'width': 480, 'height': 300})
        
        worksheet.insert_chart(fila_inicio, 0, chart_cursos)
        
        # Gráfico 2: Créditos por período
        chart_creditos = workbook.add_chart({'type': 'line'})
        chart_creditos.add_series({
            'name': 'Créditos Matriculados',
            'categories': [worksheet.name, 4, 0, 3 + len(datos_graficos), 0],
            'values': [worksheet.name, 4, 6, 3 + len(datos_graficos), 6],
            'line': {'color': '#ff7f0e', 'width': 3}
        })
        
        chart_creditos.set_title({'name': 'Evolución de Créditos por Período'})
        chart_creditos.set_x_axis({'name': 'Período'})
        chart_creditos.set_y_axis({'name': 'Número de Créditos'})
        chart_creditos.set_size({'width': 480, 'height': 300})
        
        worksheet.insert_chart(fila_inicio, 7, chart_creditos)

    def _generar_hoja_progreso_plan(self, workbook: Workbook, expediente: Expediente, formatos: Dict[str, Format]) -> None:
        """
        Genera la hoja de progreso por semestre del plan de estudios.
        
        Args:
            workbook: Libro de Excel
            expediente: Expediente del estudiante
            formatos: Diccionario de formatos
        """
        worksheet = workbook.add_worksheet('Progreso del Plan')
        worksheet.hide_gridlines(2)
        
        fila = 0
        
        # Título principal
        worksheet.merge_range(fila, 0, fila, 7, 'PROGRESO POR SEMESTRE DEL PLAN', formatos['encabezado'])
        fila += 1
        
        # Información del estudiante
        worksheet.write(fila, 0, 'Carné:', formatos['info_estudiante'])
        worksheet.write(fila, 1, expediente.carne, formatos['info_estudiante'])
        worksheet.write(fila, 3, 'Nombre:', formatos['info_estudiante'])
        worksheet.merge_range(fila, 4, fila, 7, expediente.nombre, formatos['info_estudiante'])
        fila += 2
        
        # Encabezados
        encabezados = ['Semestre', 'Cursos Aprobados', 'Cursos Reprobados', 'Cursos en Matrícula', 'Cursos Pendientes', 'Total Cursos', 'Progreso %', 'Estado']
        for i, encabezado in enumerate(encabezados):
            worksheet.write(fila, i, encabezado, formatos['encabezado'])
        fila += 1
        
        # Datos por semestre del plan
        for numero_semestre in sorted(expediente.semestres.keys()):
            semestre = expediente.semestres[numero_semestre]
            
            cursos_aprobados = len([c for c in semestre.cursos if c.esta_aprobado()])
            cursos_reprobados = len([c for c in semestre.cursos if any(h.estado == 'REPROBADO' for h in c.historial)])
            cursos_matriculados = len([c for c in semestre.cursos if any(h.estado == 'MATRICULADO' for h in c.historial)])
            cursos_pendientes = len([c for c in semestre.cursos if not c.esta_aprobado() and not any(h.estado == 'MATRICULADO' for h in c.historial)])
            total_cursos = len(semestre.cursos)
            
            progreso = (cursos_aprobados / total_cursos * 100) if total_cursos > 0 else 0
            
            # Determinar estado del semestre
            if cursos_aprobados == total_cursos:
                estado = "COMPLETADO"
                formato_fila = formatos['curso_aprobado']
            elif cursos_matriculados > 0:
                estado = "EN PROGRESO"
                formato_fila = formatos['curso_matriculado']
            elif cursos_aprobados > 0:
                estado = "PARCIAL"
                formato_fila = formatos['curso_sin_datos']
            else:
                estado = "PENDIENTE"
                formato_fila = formatos['curso_pendiente']
            
            worksheet.write(fila, 0, f'Semestre {numero_semestre}', formato_fila)
            worksheet.write(fila, 1, cursos_aprobados, formato_fila)
            worksheet.write(fila, 2, cursos_reprobados, formato_fila)
            worksheet.write(fila, 3, cursos_matriculados, formato_fila)
            worksheet.write(fila, 4, cursos_pendientes, formato_fila)
            worksheet.write(fila, 5, total_cursos, formato_fila)
            worksheet.write(fila, 6, progreso/100, formatos['porcentaje'])
            worksheet.write(fila, 7, estado, formato_fila)
            
            fila += 1
        
        # Ajustar ancho de columnas
        worksheet.set_column(0, 0, 15)  # Semestre
        worksheet.set_column(1, 7, 12)  # Resto de columnas

    def _generar_hoja_cursos_pendientes(self, workbook: Workbook, expediente: Expediente, formatos: Dict[str, Format]) -> None:
        """
        Genera la hoja de cursos pendientes con análisis detallado de requisitos.
        
        Args:
            workbook: Libro de Excel
            expediente: Expediente del estudiante
            formatos: Diccionario de formatos
        """
        worksheet = workbook.add_worksheet('Cursos Pendientes')
        worksheet.hide_gridlines(2)
        
        fila = 0
        
        # Título principal
        worksheet.merge_range(fila, 0, fila, 15, 'CURSOS PENDIENTES Y ANÁLISIS DETALLADO DE REQUISITOS', formatos['encabezado'])
        fila += 1
        
        # Información del estudiante
        worksheet.write(fila, 0, 'Carné:', formatos['info_estudiante'])
        worksheet.write(fila, 1, expediente.carne, formatos['info_estudiante'])
        worksheet.write(fila, 3, 'Nombre:', formatos['info_estudiante'])
        worksheet.merge_range(fila, 4, fila, 15, expediente.nombre, formatos['info_estudiante'])
        fila += 2
        
        # Leyenda
        worksheet.write(fila, 0, 'LEYENDA:', formatos['encabezado'])
        worksheet.write(fila, 2, '✓ Cumplido', formatos['requisito_cumplido'])
        worksheet.write(fila, 3, '✗ Pendiente', formatos['requisito_pendiente'])
        worksheet.write(fila, 4, '⚠️ En Matrícula', formatos['curso_matriculado'])
        fila += 2
        
        # Obtener cursos aprobados y matriculados para verificar requisitos
        cursos_aprobados = set()
        cursos_matriculados = set()
        for semestre in expediente.semestres.values():
            for curso in semestre.cursos:
                if curso.esta_aprobado():
                    cursos_aprobados.add(curso.sigla)
                elif any(h.estado == 'MATRICULADO' for h in curso.historial):
                    cursos_matriculados.add(curso.sigla)
        
        # Procesar cursos pendientes
        cursos_pendientes_data = []
        
        for numero_semestre in sorted(expediente.semestres.keys()):
            semestre = expediente.semestres[numero_semestre]
            
            for curso in semestre.cursos:
                if not curso.esta_aprobado() and not any(h.estado == 'MATRICULADO' for h in curso.historial):
                    # Este es un curso pendiente
                    requisitos = self._obtener_requisitos_curso(curso.sigla)
                    correquisitos = self._obtener_correquisitos_curso(curso.sigla)
                    
                    cursos_pendientes_data.append({
                        'curso': curso,
                        'semestre': numero_semestre,
                        'requisitos': requisitos,
                        'correquisitos': correquisitos
                    })
        
        if not cursos_pendientes_data:
            worksheet.write(fila, 0, 'No hay cursos pendientes. ¡Felicidades!', formatos['curso_aprobado'])
            return
        
        # Encabezados
        encabezados = ['Sigla', 'Curso', 'Créditos', 'Sem.', 'Requisitos', 'Estado Req.', 'Correquisitos', 'Estado Correq.', 'Puede Matricular?']
        for i, encabezado in enumerate(encabezados):
            worksheet.write(fila, i, encabezado, formatos['encabezado'])
        fila += 1
        
        # Procesar cada curso pendiente
        for data in cursos_pendientes_data:
            curso = data['curso']
            requisitos = data['requisitos']
            correquisitos = data['correquisitos']
            
            # Analizar requisitos
            requisitos_status = []
            for req in requisitos:
                if req in cursos_aprobados:
                    requisitos_status.append(f"✓ {req}")
                elif req in cursos_matriculados:
                    requisitos_status.append(f"⚠️ {req}")
                else:
                    requisitos_status.append(f"✗ {req}")
            
            # Analizar correquisitos
            correquisitos_status = []
            for correq in correquisitos:
                if correq in cursos_aprobados:
                    correquisitos_status.append(f"✓ {correq}")
                elif correq in cursos_matriculados:
                    correquisitos_status.append(f"⚠️ {correq}")
                else:
                    correquisitos_status.append(f"✗ {correq}")
            
            # Determinar si puede matricular
            requisitos_cumplidos = all(req in cursos_aprobados for req in requisitos) if requisitos else True
            correquisitos_disponibles = all(
                correq in cursos_aprobados or correq in cursos_matriculados or self._curso_disponible(correq, expediente) 
                for correq in correquisitos
            ) if correquisitos else True
            
            puede_matricular = requisitos_cumplidos and correquisitos_disponibles
            
            # Escribir datos principales del curso
            formato_curso = formatos['curso_aprobado'] if puede_matricular else formatos['curso_pendiente']
            
            worksheet.write(fila, 0, curso.sigla, formato_curso)
            worksheet.write(fila, 1, curso.nombre[:40] + '...' if len(curso.nombre) > 40 else curso.nombre, formato_curso)
            worksheet.write(fila, 2, curso.creditos, formato_curso)
            worksheet.write(fila, 3, data['semestre'], formato_curso)
            
            # Mostrar requisitos con estado
            if requisitos:
                requisitos_texto = ', '.join([req.split(' ', 1)[1] for req in requisitos_status])  # Solo siglas
                worksheet.write(fila, 4, requisitos_texto, formato_curso)
                
                # Estado de requisitos (con colores)
                todos_cumplidos = all('✓' in req for req in requisitos_status)
                alguno_en_matricula = any('⚠️' in req for req in requisitos_status)
                
                if todos_cumplidos:
                    worksheet.write(fila, 5, '✓ CUMPLIDO', formatos['requisito_cumplido'])
                elif alguno_en_matricula:
                    worksheet.write(fila, 5, '⚠️ PARCIAL', formatos['curso_matriculado'])
                else:
                    worksheet.write(fila, 5, '✗ PENDIENTE', formatos['requisito_pendiente'])
            else:
                worksheet.write(fila, 4, 'N/A', formato_curso)
                worksheet.write(fila, 5, '✓ N/A', formatos['requisito_cumplido'])
            
            # Mostrar correquisitos con estado
            if correquisitos:
                correquisitos_texto = ', '.join([correq.split(' ', 1)[1] for correq in correquisitos_status])  # Solo siglas
                worksheet.write(fila, 6, correquisitos_texto, formato_curso)
                
                # Estado de correquisitos
                todos_disponibles = all('✓' in correq or '⚠️' in correq for correq in correquisitos_status)
                
                if todos_disponibles:
                    worksheet.write(fila, 7, '✓ DISPONIBLE', formatos['requisito_cumplido'])
                else:
                    worksheet.write(fila, 7, '✗ NO DISPONIBLE', formatos['requisito_pendiente'])
            else:
                worksheet.write(fila, 6, 'N/A', formato_curso)
                worksheet.write(fila, 7, '✓ N/A', formatos['requisito_cumplido'])
            
            # Resultado final
            worksheet.write(fila, 8, 'SÍ PUEDE' if puede_matricular else 'NO PUEDE',
                          formatos['curso_aprobado'] if puede_matricular else formatos['curso_reprobado'])
            
            fila += 1
            
            # Si hay muchos requisitos o correquisitos, mostrar detalle en filas adicionales
            max_items = max(len(requisitos), len(correquisitos))
            if max_items > 1:
                for i in range(max_items):
                    # Fila de detalle para requisitos individuales
                    if i < len(requisitos_status):
                        req_status = requisitos_status[i]
                        worksheet.write(fila, 4, req_status, 
                                      formatos['requisito_cumplido'] if '✓' in req_status 
                                      else formatos['curso_matriculado'] if '⚠️' in req_status
                                      else formatos['requisito_pendiente'])
                    
                    if i < len(correquisitos_status):
                        correq_status = correquisitos_status[i]
                        worksheet.write(fila, 6, correq_status,
                                      formatos['requisito_cumplido'] if '✓' in correq_status 
                                      else formatos['curso_matriculado'] if '⚠️' in correq_status
                                      else formatos['requisito_pendiente'])
                    
                    if i < max_items - 1:  # No agregar fila extra después del último
                        fila += 1
        
        # Resumen final
        fila += 2
        puede_matricular_count = sum(1 for data in cursos_pendientes_data 
                                   if self._puede_matricular_curso(data, cursos_aprobados, cursos_matriculados, expediente))
        total_pendientes = len(cursos_pendientes_data)
        
        worksheet.write(fila, 0, 'RESUMEN:', formatos['encabezado'])
        fila += 1
        worksheet.write(fila, 0, f'Total cursos pendientes: {total_pendientes}', formatos['info_estudiante'])
        fila += 1
        worksheet.write(fila, 0, f'Cursos que puede matricular: {puede_matricular_count}', formatos['curso_aprobado'])
        fila += 1
        worksheet.write(fila, 0, f'Cursos bloqueados por requisitos: {total_pendientes - puede_matricular_count}', formatos['curso_reprobado'])
        
        # Ajustar ancho de columnas
        worksheet.set_column(0, 0, 10)  # Sigla
        worksheet.set_column(1, 1, 45)  # Curso
        worksheet.set_column(2, 2, 8)   # Créditos
        worksheet.set_column(3, 3, 6)   # Semestre
        worksheet.set_column(4, 4, 25)  # Requisitos
        worksheet.set_column(5, 5, 15)  # Estado Req
        worksheet.set_column(6, 6, 25)  # Correquisitos
        worksheet.set_column(7, 7, 15)  # Estado Correq
        worksheet.set_column(8, 8, 15)  # Puede Matricular

    def _generar_hoja_cursos_reprobados(self, workbook: Workbook, expediente: Expediente, formatos: Dict[str, Format]) -> None:
        """
        Genera la hoja de cursos reprobados con su historial.
        
        Args:
            workbook: Libro de Excel
            expediente: Expediente del estudiante
            formatos: Diccionario de formatos
        """
        worksheet = workbook.add_worksheet('Cursos Reprobados')
        worksheet.hide_gridlines(2)
        
        fila = 0
        
        # Título principal
        worksheet.merge_range(fila, 0, fila, 6, 'CURSOS REPROBADOS E HISTORIAL', formatos['encabezado'])
        fila += 1
        
        # Información del estudiante
        worksheet.write(fila, 0, 'Carné:', formatos['info_estudiante'])
        worksheet.write(fila, 1, expediente.carne, formatos['info_estudiante'])
        worksheet.write(fila, 3, 'Nombre:', formatos['info_estudiante'])
        worksheet.merge_range(fila, 4, fila, 6, expediente.nombre, formatos['info_estudiante'])
        fila += 2
        
        # Recopilar cursos con estado reprobado o retiro
        cursos_problema = {}
        
        for semestre in expediente.semestres.values():
            for curso in semestre.cursos:
                if curso.historial:
                    registros_problema = [h for h in curso.historial 
                                        if h.estado in ['REPROBADO', 'RETIRO', 'RETIRO DE MATRÍCULA']]
                    
                    if registros_problema:
                        if curso.sigla not in cursos_problema:
                            cursos_problema[curso.sigla] = {
                                'nombre': curso.nombre,
                                'creditos': curso.creditos,
                                'registros': []
                            }
                        cursos_problema[curso.sigla]['registros'].extend(registros_problema)
        
        if not cursos_problema:
            worksheet.write(fila, 0, 'No hay cursos reprobados o con retiros.', formatos['info_estudiante'])
            return
        
        # Procesar cada curso con problemas
        for sigla, datos in cursos_problema.items():
            # Encabezado del curso
            worksheet.merge_range(fila, 0, fila, 6, f'{sigla} - {datos["nombre"]} ({datos["creditos"]} créditos)', formatos['encabezado'])
            fila += 1
            
            # Encabezados de columnas
            encabezados = ['Intento', 'Período', 'Año', 'Grupo', 'Estado', 'Nota', 'Observaciones']
            for i, encabezado in enumerate(encabezados):
                worksheet.write(fila, i, encabezado, formatos['info_estudiante'])
            fila += 1
            
            # Ordenar registros por año y período
            registros_ordenados = sorted(datos['registros'], 
                                       key=lambda x: (x.anno or 0, x.periodo or 0))
            
            # Mostrar cada intento
            for i, registro in enumerate(registros_ordenados, 1):
                formato_fila = formatos['curso_reprobado'] if registro.estado == 'REPROBADO' else formatos['curso_matriculado']
                
                worksheet.write(fila, 0, i, formato_fila)
                worksheet.write(fila, 1, f'{registro.anno}-{registro.periodo}' if registro.anno and registro.periodo else 'N/A', formato_fila)
                worksheet.write(fila, 2, registro.anno or 'N/A', formato_fila)
                worksheet.write(fila, 3, registro.grupo or 'N/A', formato_fila)
                worksheet.write(fila, 4, registro.estado, formato_fila)
                worksheet.write(fila, 5, registro.nota or 'N/A', formato_fila)
                worksheet.write(fila, 6, self._generar_observacion_reprobado(registro, i), formato_fila)
                fila += 1
            
            # Resumen del curso
            total_intentos = len(registros_ordenados)
            worksheet.write(fila, 0, 'Total intentos:', formatos['numero_grande'])
            worksheet.write(fila, 1, total_intentos, formatos['numero_grande'])
            
            if total_intentos >= 3:
                worksheet.write(fila, 3, '⚠️ ATENCIÓN: 3+ intentos', formatos['curso_reprobado'])
            
            fila += 2  # Espacio entre cursos
        
        # Ajustar ancho de columnas
        worksheet.set_column(0, 0, 8)   # Intento
        worksheet.set_column(1, 1, 12)  # Período
        worksheet.set_column(2, 2, 8)   # Año
        worksheet.set_column(3, 3, 8)   # Grupo
        worksheet.set_column(4, 4, 15)  # Estado
        worksheet.set_column(5, 5, 8)   # Nota
        worksheet.set_column(6, 6, 25)  # Observaciones

    def _obtener_requisitos_curso(self, sigla: str) -> list:
        """
        Obtiene los requisitos de un curso desde la configuración.
        """
        try:
            import config
            for curso_dict in config.detalle_cursos:
                if curso_dict.get('sigla') == sigla:
                    return curso_dict.get('requisitos', [])
        except Exception:
            pass
        
        return []

    def _obtener_correquisitos_curso(self, sigla: str) -> list:
        """
        Obtiene los correquisitos de un curso desde la configuración.
        """
        try:
            import config
            for curso_dict in config.detalle_cursos:
                if curso_dict.get('sigla') == sigla:
                    return curso_dict.get('correquisitos', [])
        except Exception:
            pass
            
        return []

    def _puede_matricular_curso(self, curso_data: dict, cursos_aprobados: set, cursos_matriculados: set, expediente: Expediente) -> bool:
        """
        Determina si un curso puede ser matriculado basado en sus requisitos.
        """
        requisitos = curso_data['requisitos']
        correquisitos = curso_data['correquisitos']
        
        # Verificar requisitos
        requisitos_cumplidos = all(req in cursos_aprobados for req in requisitos) if requisitos else True
        
        # Verificar correquisitos
        correquisitos_disponibles = all(
            correq in cursos_aprobados or correq in cursos_matriculados or self._curso_disponible(correq, expediente) 
            for correq in correquisitos
        ) if correquisitos else True
        
        return requisitos_cumplidos and correquisitos_disponibles

    def _curso_disponible(self, sigla: str, expediente: Expediente) -> bool:
        """
        Verifica si un curso está disponible para matrícula.
        """
        for semestre in expediente.semestres.values():
            for curso in semestre.cursos:
                if curso.sigla == sigla:
                    return any(h.estado == 'MATRICULADO' for h in curso.historial)
        return False

    def _generar_observacion_reprobado(self, registro, intento: int) -> str:
        """
        Genera observaciones para cursos reprobados.
        """
        if intento == 1:
            return "Primer intento"
        elif intento == 2:
            return "Segundo intento"
        elif intento == 3:
            return "⚠️ Tercer intento - Revisar estrategia"
        else:
            return f"⚠️ Intento #{intento} - Requiere intervención"
