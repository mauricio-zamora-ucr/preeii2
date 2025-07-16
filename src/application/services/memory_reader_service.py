"""
Servicio para el procesamiento de contenido desde memoria (clipboard)
"""
import re
from typing import Optional, Tuple, List, Dict

from ...infrastructure.repositories.file_repository import FileRepository
from .expediente_service import ExpedienteService


class MemoryReaderService:
    """
    Servicio que procesa contenido copiado al clipboard desde el sistema de matrícula.
    """

    def __init__(self, file_repository: Optional[FileRepository] = None):
        """
        Inicializa el servicio de lectura de memoria.
        
        Args:
            file_repository: Repositorio de archivos para persistencia
        """
        self.file_repo = file_repository or FileRepository()
        self.expediente_service = ExpedienteService()

    def identificar_tipo_contenido(self, texto: str) -> Optional[str]:
        """
        Identifica el tipo de contenido basado en patrones del texto.
        
        Args:
            texto: Contenido del clipboard
        
        Returns:
            'exp' para expediente, 'pre' para prematrícula, None si no se identifica
        """
        patron_expediente = re.compile(r'(Expediente académico)')
        patron_prematricula = re.compile(r'(Cursos solicitados en prematrícula)')
        
        if patron_prematricula.search(texto):
            return 'pre'
        elif patron_expediente.search(texto):
            return 'exp'
        else:
            return None

    def procesar_contenido_memoria(self, texto: str) -> bool:
        """
        Procesa el contenido de la memoria según su tipo.
        
        Args:
            texto: Contenido del clipboard
        
        Returns:
            True si se procesó exitosamente, False en caso contrario
        """
        tipo_contenido = self.identificar_tipo_contenido(texto)
        
        if tipo_contenido == 'pre':
            print("SOLICITUD PROCESADO")
            carne, nombre = self._procesar_cursos_solicitados(texto)
            return True
        elif tipo_contenido == 'exp':
            print("EXPEDIENTE PROCESADO")
            carne, nombre = self._procesar_expediente(texto)
            return True
        else:
            print("NO HAY DATOS PARA PROCESAR")
            return False

    def _procesar_cursos_solicitados(self, texto: str) -> Tuple[str, str]:
        """
        Procesa cursos solicitados en prematrícula.
        
        Args:
            texto: Contenido del clipboard con información de prematrícula
        
        Returns:
            Tupla con (carné, nombre) del estudiante
        """
        # Extraer información básica del estudiante
        carne = self._extraer_carne(texto)
        nombre = self._extraer_nombre(texto)

        # Extraer comentarios
        comentario_estudiante = self._extraer_comentario_estudiante(texto)
        comentario_profesor = self._extraer_comentario_profesor(texto)

        # Extraer cursos solicitados
        cursos_solicitados = self._extraer_cursos_solicitados(texto)

        # Guardar información
        encabezados = ['SIGLA', 'CURSO', 'CREDITOS', 'AUTORIZACION', 'DEC']
        self.file_repo.escribir_cursos_solicitados(carne, encabezados, cursos_solicitados)
        self.file_repo.escribir_comentarios(carne, comentario_estudiante, comentario_profesor)

        # Mostrar resumen
        self._imprimir_cursos_solicitados(cursos_solicitados)

        return carne, nombre

    def _procesar_expediente(self, texto: str) -> Tuple[str, str]:
        """
        Procesa expediente académico.
        
        Args:
            texto: Contenido del clipboard con información del expediente
        
        Returns:
            Tupla con (carné, nombre) del estudiante
        """
        # Extraer información básica del estudiante
        carne, nombre = self._extraer_info_estudiante_expediente(texto)

        # Extraer historial académico
        historial = self._extraer_historial_academico(texto)

        # Guardar información
        self.file_repo.escribir_informacion_estudiante(carne, carne, nombre)
        
        encabezados = ['SIGLA', 'CURSO', 'CREDITOS', 'GRUPO', 'SEM', 'AÑO', 'ESTADO', 'NOTA']
        self.file_repo.escribir_historial(carne, encabezados, historial)

        return carne, nombre

    def _extraer_carne(self, texto: str) -> str:
        """Extrae el carné del estudiante del texto."""
        patron = re.compile(r"Carné:\s+([A-Z]?\d{5})\s*\r\n")
        match = patron.search(texto)
        return match.group(1) if match else ""

    def _extraer_nombre(self, texto: str) -> str:
        """Extrae el nombre del estudiante del texto."""
        patron = re.compile(r"Nombre:\s+([\w\s]+)\s*\r\n")
        match = patron.search(texto)
        return match.group(1).strip() if match else ""

    def _extraer_comentario_estudiante(self, texto: str) -> str:
        """Extrae el comentario del estudiante."""
        patron = re.compile(r"Comentario del estudiante\r\n(.*)\r\n", re.IGNORECASE)
        match = patron.search(texto)
        if match:
            comentario = match.group(1)
            if comentario.startswith('Cantidad de créditos solicitados'):
                return ''
            return comentario
        return ''

    def _extraer_comentario_profesor(self, texto: str) -> str:
        """Extrae el comentario del profesor."""
        patron = re.compile(r"Comentario hacia el Estudiante\s*\r\n(.*)\r\n", re.IGNORECASE)
        match = patron.search(texto)
        if match:
            comentario = match.group(1)
            if comentario.startswith('* Cursos con Declaración Jurada'):
                return ''
            return comentario
        return ''

    def _extraer_cursos_solicitados(self, texto: str) -> List[Dict[str, str]]:
        """Extrae los cursos solicitados del texto."""
        patron = re.compile(
            r"(\*?)[ ]?([A-Z]{2}\d{4}|[A-Z]{2}-[A-Z]|[A-Z]{2}-[I]{1,3})\s*"
            r"([\.:\dA-Z\(\) ÁÉÍÓÚÑ]+)\s+(\d{1,2}).*\r\n(.*)\r\n"
        )

        cursos = []
        for match in patron.finditer(texto):
            declaracion = match.group(1)
            sigla = match.group(2)
            curso = match.group(3)
            creditos = match.group(4)
            otros = match.group(5).strip()
            
            curso_dict = {
                'SIGLA': sigla,
                'CURSO': curso,
                'CREDITOS': creditos,
                'AUTORIZACION': otros,
                'DEC': 'SI' if declaracion == '*' else 'NO'
            }
            cursos.append(curso_dict)

        # Ordenar por sigla
        cursos.sort(key=lambda x: x['SIGLA'])
        return cursos

    def _extraer_info_estudiante_expediente(self, texto: str) -> Tuple[str, str]:
        """Extrae información del estudiante del expediente."""
        patron = re.compile(r"Carné:\s+([A-Z]?\d{5})\s+([\w\s]+)\r\n", re.VERBOSE)
        match = patron.search(texto)
        if match:
            carne = match.group(1)
            nombre = match.group(2).strip()
            return carne, nombre
        return "", ""

    def _extraer_historial_academico(self, texto: str) -> List[Dict[str, str]]:
        """Extrae el historial académico del texto."""
        patron = re.compile(
            r"([A-Z]{2}\d{4})\s+([\.:\dA-Z\(\) ÁÉÍÓÚÑ]+)\s+(\d{1,2})\s+"
            r"(\d{1,3})\s+([I]{1,3})\s+(\d{4})\s+([A-Z ]+)\s+(.+)\r\n"
        )

        historial = []
        for match in patron.finditer(texto):
            curso_dict = {
                'SIGLA': match.group(1),
                'CURSO': match.group(2),
                'CREDITOS': match.group(3),
                'GRUPO': match.group(4),
                'SEM': match.group(5),
                'AÑO': match.group(6),
                'ESTADO': match.group(7),
                'NOTA': match.group(8)
            }
            historial.append(curso_dict)

        # Ordenar por año, semestre y sigla
        historial.sort(key=lambda x: (x['AÑO'], x['SEM'], x['SIGLA']))
        return historial

    def _imprimir_cursos_solicitados(self, cursos: List[Dict[str, str]]) -> None:
        """
        Imprime un resumen de los cursos solicitados.
        
        Args:
            cursos: Lista de cursos solicitados
        """
        print("\n=== CURSOS SOLICITADOS ===")
        for curso in cursos:
            print(f"{curso['SIGLA']:8} {curso['CURSO']:50} {curso['CREDITOS']:2} {curso['DEC']:3}")
        print(f"\nTotal de cursos: {len(cursos)}")
        print("==========================")
