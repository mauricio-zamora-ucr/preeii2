"""
Servicio para el web scraping del sistema de matrícula
"""
import re
import requests
from typing import List, Optional, Tuple, Dict
from termcolor import cprint

from ...shared.config.settings import app_config
from ...infrastructure.adapters.http_adapter import HttpAdapter
from ...infrastructure.adapters.html_parser import StudentParser, MainListingParser


class WebScrapingService:
    """
    Servicio que maneja el web scraping del sistema de matrícula de la UCR.
    """

    def __init__(self, http_adapter: Optional[HttpAdapter] = None):
        """
        Inicializa el servicio de web scraping.
        
        Args:
            http_adapter: Adaptador HTTP personalizado
        """
        self.http_adapter = http_adapter or HttpAdapter()
        self.urls = app_config.urls

    def autenticar_usuario(self, usuario: str, clave: str) -> bool:
        """
        Autentica al usuario en el sistema de matrícula.
        
        Args:
            usuario: Nombre de usuario
            clave: Contraseña del usuario
        
        Returns:
            True si la autenticación fue exitosa, False en caso contrario
        """
        datos_auth = {'user': usuario, 'password': clave}
        return self.http_adapter.autenticar(self.urls.login, datos_auth)

    def obtener_listado_estudiantes(self) -> List[Tuple[str, str, str, str]]:
        """
        Obtiene el listado de estudiantes asignados al profesor.
        
        Returns:
            Lista de tuplas con (clave, carne, nombre, correo) de cada estudiante
        """
        response = self.http_adapter.obtener_contenido(self.urls.listado)
        
        if not self._validar_acceso_listado(response):
            raise ValueError("No se pudo acceder al listado de estudiantes")

        parser = MainListingParser()
        parser.feed(response)
        return parser.get_lista()

    def descargar_expediente_estudiante(self, clave_estudiante: str) -> str:
        """
        Descarga el expediente de un estudiante específico.
        
        Args:
            clave_estudiante: Clave única del estudiante en el sistema
        
        Returns:
            Contenido HTML del expediente del estudiante
        """
        url_expediente = self.urls.notas.format(clave_estudiante)
        return self.http_adapter.obtener_contenido(url_expediente)

    def procesar_expediente_estudiante(self, contenido_html: str) -> List[Dict[str, str]]:
        """
        Procesa el contenido HTML del expediente y extrae la información.
        
        Args:
            contenido_html: Contenido HTML del expediente
        
        Returns:
            Lista de diccionarios con la información de cada curso
        """
        parser = StudentParser()
        parser.feed(contenido_html)
        return parser.get_lista()

    def iniciar_proceso_descarga_completo(self, usuario: str, clave: str) -> bool:
        """
        Ejecuta el proceso completo de descarga de expedientes.
        
        Args:
            usuario: Nombre de usuario
            clave: Contraseña del usuario
        
        Returns:
            True si el proceso fue exitoso, False en caso contrario
        """
        try:
            # Autenticar usuario
            if not self.autenticar_usuario(usuario, clave):
                self._mostrar_error_credenciales()
                return False

            # Obtener listado de estudiantes
            estudiantes = self.obtener_listado_estudiantes()
            
            if not estudiantes:
                cprint('No se encontraron estudiantes asignados.', 'yellow', 'on_red')
                return False

            # Procesar cada estudiante
            for estudiante in estudiantes:
                clave_estudiante, carne, nombre, correo = estudiante
                self._procesar_estudiante_individual(clave_estudiante, carne, nombre)

            return True

        except Exception as e:
            cprint(f'Error durante el proceso de descarga: {str(e)}', 'white', 'on_red', attrs=['bold'])
            return False

    def _procesar_estudiante_individual(self, clave: str, carne: str, nombre: str) -> None:
        """
        Procesa un estudiante individual descargando y guardando su expediente.
        
        Args:
            clave: Clave del estudiante en el sistema
            carne: Carné del estudiante
            nombre: Nombre del estudiante
        """
        # Descargar expediente
        contenido_expediente = self.descargar_expediente_estudiante(clave)
        
        # Procesar contenido
        datos_cursos = self.procesar_expediente_estudiante(contenido_expediente)
        
        # Aquí se conectaría con el repositorio para guardar los datos
        # Por ahora mantenemos la funcionalidad original
        from ...infrastructure.repositories.file_repository import FileRepository
        
        file_repo = FileRepository()
        encabezados = ['SIGLA', 'CURSO', 'CREDITOS', 'GRUPO', 'SEM', 'AÑO', 'ESTADO', 'NOTA']
        file_repo.escribir_historial(carne, encabezados, datos_cursos)
        file_repo.escribir_informacion_estudiante(carne, carne, nombre)

    def _validar_acceso_listado(self, contenido: str) -> bool:
        """
        Valida que se haya podido acceder correctamente al listado de estudiantes.
        
        Args:
            contenido: Contenido HTML de la respuesta
        
        Returns:
            True si el acceso fue exitoso, False en caso contrario
        """
        return bool(re.findall(r'Listado de estudiantes asignados al profesor', contenido))

    def _mostrar_error_credenciales(self) -> None:
        """Muestra un mensaje de error por credenciales incorrectas."""
        cprint(
            'NO SE HA PODIDO OBTENER LA INFORMACIÓN, FAVOR VERIFIQUE SUS CREDENCIALES (USUARIO Y CLAVE)',
            'white', 'on_red', attrs=['bold']
        )
