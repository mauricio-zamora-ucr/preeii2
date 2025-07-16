"""
Adaptador HTTP para manejar las conexiones con el sistema de matrícula
"""
import ssl
import urllib3
import requests
from typing import Dict, Optional


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    """
    Adaptador HTTP personalizado que permite usar un contexto SSL específico.
    Necesario para conectarse a sistemas con configuraciones SSL legacy.
    """

    def __init__(self, ssl_context: Optional[ssl.SSLContext] = None, **kwargs):
        """
        Inicializa el adaptador HTTP personalizado.
        
        Args:
            ssl_context: Contexto SSL personalizado
            **kwargs: Argumentos adicionales para HTTPAdapter
        """
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections: int, maxsize: int, block: bool = False):
        """
        Inicializa el pool manager con el contexto SSL personalizado.
        
        Args:
            connections: Número de conexiones
            maxsize: Tamaño máximo del pool
            block: Si debe bloquear cuando no hay conexiones disponibles
        """
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context
        )


class HttpAdapter:
    """
    Adaptador principal para manejar las comunicaciones HTTP con el sistema de matrícula.
    """

    def __init__(self):
        """Inicializa el adaptador HTTP."""
        self.session: Optional[requests.Session] = None

    def crear_sesion_legacy(self) -> requests.Session:
        """
        Crea una sesión HTTP configurada para sistemas legacy SSL.
        
        Returns:
            Sesión de requests configurada
        """
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        
        session = requests.Session()
        session.mount('https://', CustomHttpAdapter(ctx))
        
        return session

    def autenticar(self, url_login: str, datos_login: Dict[str, str]) -> bool:
        """
        Autentica al usuario en el sistema.
        
        Args:
            url_login: URL del endpoint de login
            datos_login: Diccionario con usuario y contraseña
        
        Returns:
            True si la autenticación fue exitosa, False en caso contrario
        """
        try:
            self.session = self.crear_sesion_legacy()
            response = self.session.post(url_login, data=datos_login)
            return response.status_code == 200
        except Exception:
            return False

    def obtener_contenido(self, url: str) -> str:
        """
        Obtiene el contenido de una URL usando la sesión autenticada.
        
        Args:
            url: URL de la cual obtener el contenido
        
        Returns:
            Contenido de la respuesta como string
        
        Raises:
            ValueError: Si no hay una sesión activa
        """
        if self.session is None:
            raise ValueError("No hay una sesión activa. Debe autenticarse primero.")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ValueError(f"Error al obtener contenido: {str(e)}")

    def cerrar_sesion(self) -> None:
        """Cierra la sesión HTTP actual."""
        if self.session:
            self.session.close()
            self.session = None
