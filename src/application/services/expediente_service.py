"""
Servicio para el procesamiento de expedientes académicos
"""
import os
from datetime import timedelta
from typing import List, Dict, Tuple, Optional
from termcolor import cprint

from ...domain.entities.expediente import Expediente
from ...domain.entities.semestre import Semestre
from ...domain.entities.curso_carrera import CursoCarrera
from ...shared.config.settings import DETALLE_CURSOS


class ExpedienteService:
    """
    Servicio que maneja la lógica de negocio para el procesamiento de expedientes.
    """

    @staticmethod
    def cargar_cursos_carrera(
        listado_cursos: Optional[List[Dict]] = None
    ) -> Tuple[Dict[str, CursoCarrera], Dict[int, Semestre], Expediente]:
        """
        Carga la estructura de cursos de la carrera y crea un expediente vacío.
        
        Args:
            listado_cursos: Lista de diccionarios con información de cursos.
                          Si es None, usa DETALLE_CURSOS por defecto.
        
        Returns:
            Tupla con diccionario de cursos por sigla, semestres y expediente vacío.
        """
        if listado_cursos is None:
            listado_cursos = DETALLE_CURSOS

        sigla_cursos: Dict[str, CursoCarrera] = {}
        semestre_cursos: Dict[int, Semestre] = {}
        expediente = Expediente()

        for detalle_curso in listado_cursos:
            sigla = detalle_curso['sigla']
            nombre = detalle_curso['curso']
            semestre = detalle_curso['semestre']
            creditos = detalle_curso['creditos']
            
            curso = CursoCarrera(
                sigla=sigla,
                nombre=nombre,
                creditos=creditos,
                semestre=semestre
            )

            # Agregar requisitos si existen
            if 'requisitos' in detalle_curso:
                for requisito in detalle_curso['requisitos']:
                    curso.agregar_requisito(requisito)

            # Agregar correquisitos si existen
            if 'correquisitos' in detalle_curso:
                for correquisito in detalle_curso['correquisitos']:
                    curso.agregar_correquisito(correquisito)

            sigla_cursos[sigla] = curso
            
            # Crear semestre si no existe
            if semestre not in semestre_cursos:
                semestre_cursos[semestre] = Semestre(numero=semestre)
            
            semestre_cursos[semestre].agregar_curso(curso)

        # Agregar todos los semestres al expediente
        for sem in semestre_cursos.values():
            expediente.agregar_semestre(sem)

        return sigla_cursos, semestre_cursos, expediente

    @staticmethod
    def procesar_expediente_estudiante(
        carne: str, 
        nombre: str, 
        datos_historial: List[Dict[str, str]]
    ) -> Expediente:
        """
        Procesa el expediente completo de un estudiante.
        
        Args:
            carne: Carné del estudiante
            nombre: Nombre del estudiante
            datos_historial: Lista con los datos del historial académico
        
        Returns:
            Expediente procesado del estudiante
        """
        _, _, expediente = ExpedienteService.cargar_cursos_carrera()
        expediente.carne = carne
        expediente.nombre = nombre

        # Procesar cada línea del historial
        for linea in datos_historial:
            expediente.agregar_curso(linea)

        # Procesar requisitos y correquisitos
        expediente.procesar_requisitos_correquisitos()

        return expediente

    @staticmethod
    def calcular_tiempo_estimado_revision(lineas_historial: int) -> timedelta:
        """
        Calcula el tiempo estimado que se ahorra en la revisión manual.
        
        Args:
            lineas_historial: Número de líneas en el historial
        
        Returns:
            Tiempo estimado ahorrado
        """
        return timedelta(minutes=1) + lineas_historial * timedelta(seconds=20)

    @staticmethod
    def validar_directorio_salida(directorio: str = './salida') -> None:
        """
        Valida que exista el directorio de salida, lo crea si no existe.
        
        Args:
            directorio: Ruta del directorio de salida
        """
        if not os.path.isdir(directorio):
            os.makedirs(directorio, exist_ok=True)

    @staticmethod
    def imprimir_resumen_procesamiento(
        carne: str, 
        nombre: str, 
        lineas: int, 
        tiempo: timedelta, 
        es_impar: bool = True
    ) -> None:
        """
        Imprime un resumen del procesamiento de un expediente.
        
        Args:
            carne: Carné del estudiante
            nombre: Nombre del estudiante
            lineas: Número de líneas procesadas
            tiempo: Tiempo estimado de procesamiento
            es_impar: Para alternar colores en la salida
        """
        texto = f'{carne:9} {nombre:69} {lineas:9} {str(tiempo):>10}'
        
        if es_impar:
            cprint(texto, 'blue', 'on_white')
        else:
            cprint(texto, 'blue', 'on_cyan')

    @staticmethod
    def imprimir_encabezado_procesamiento() -> None:
        """Imprime el encabezado para el resumen de procesamiento."""
        texto = f'{"CARNE":9} {"NOMBRE":69} {"LINEAS":>9} {"TIEMPO":>10}'
        cprint(texto, 'magenta', 'on_yellow')

    @staticmethod
    def imprimir_tiempo_total_ahorrado(tiempo_total: timedelta) -> None:
        """
        Imprime el tiempo total ahorrado en el procesamiento.
        
        Args:
            tiempo_total: Tiempo total ahorrado
        """
        texto = f'TIEMPO TOTAL ESTIMADO QUE USTED SE AHORRO SOLO EN ESTA ETAPA: {tiempo_total}'
        texto = f'{texto:^100}'
        cprint(texto, 'cyan', 'on_red', attrs=['bold', 'blink'])
