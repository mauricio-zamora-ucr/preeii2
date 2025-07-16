"""
Parsers HTML para extraer información del sistema de matrícula
"""
import base64
from html.parser import HTMLParser
from typing import List, Dict


class StudentParser(HTMLParser):
    """
    Parser HTML para extraer información del expediente académico de un estudiante.
    """

    def __init__(self):
        """Inicializa el parser del estudiante."""
        super().__init__()
        self.reset()
        self._lista: List[Dict[str, str]] = []
        self._bandera_table: bool = False
        self._bandera_tr_header: bool = False
        self._bandera_tr: bool = False
        self._bandera_lectura: bool = False
        self._contador: int = 0
        self._datos_temporales: List[str] = []

    def get_lista(self) -> List[Dict[str, str]]:
        """
        Obtiene la lista de cursos procesados, ordenada por año, semestre y sigla.
        
        Returns:
            Lista de diccionarios con información de cada curso
        """
        # Convertir lista de listas a lista de diccionarios
        cursos_dict = []
        for curso_data in self._lista:
            if len(curso_data) >= 7:
                curso_dict = {
                    'SIGLA': curso_data[0],
                    'CURSO': curso_data[1],
                    'CREDITOS': curso_data[2],
                    'GRUPO': curso_data[3],
                    'SEM': curso_data[4],
                    'AÑO': curso_data[5],
                    'ESTADO': curso_data[6] if len(curso_data) > 6 else '',
                    'NOTA': curso_data[7] if len(curso_data) > 7 else ''
                }
                cursos_dict.append(curso_dict)
        
        # Ordenar por año, semestre y sigla (más reciente primero)
        cursos_dict.sort(key=lambda x: (x['AÑO'], x['SEM'], x['SIGLA']), reverse=True)
        return cursos_dict

    def handle_starttag(self, tag: str, attrs: List[tuple]) -> None:
        """
        Maneja las etiquetas de apertura HTML.
        
        Args:
            tag: Nombre de la etiqueta HTML
            attrs: Atributos de la etiqueta
        """
        if tag == 'table':
            self._bandera_table = True

        if tag == 'tr' and not self._bandera_tr_header:
            self._bandera_tr_header = True

        if tag == 'tr' and self._bandera_tr_header:
            self._bandera_tr = True
            self._contador = 0

        if tag == 'td' and self._bandera_tr:
            self._bandera_lectura = True

    def handle_data(self, data: str) -> None:
        """
        Maneja el contenido de texto de las etiquetas HTML.
        
        Args:
            data: Contenido de texto
        """
        if not self._bandera_lectura:
            return

        if self._contador == 0:
            self._datos_temporales = []

        texto_limpio = data.strip()
        
        if self._contador == 4:  # Columna de semestre/año
            # Procesar datos de semestre y año
            texto_limpio = ' '.join(data.strip().split())
            partes = texto_limpio.split(' ')
            self._datos_temporales.extend(partes)
        else:
            if self._contador == 6:  # Columna de nota
                try:
                    # Intentar convertir a float para validar que es un número
                    float(texto_limpio)
                except (ValueError, TypeError):
                    texto_limpio = texto_limpio.strip()

            self._datos_temporales.append(texto_limpio)

        if self._contador == 6:
            # Se completó una fila, agregar a la lista
            self._lista.append(self._datos_temporales.copy())
        
        self._contador += 1

    def handle_endtag(self, tag: str) -> None:
        """
        Maneja las etiquetas de cierre HTML.
        
        Args:
            tag: Nombre de la etiqueta HTML
        """
        if tag == 'tr' and self._bandera_tr_header:
            self._bandera_tr = False

        if tag == 'td' and self._bandera_tr_header:
            self._bandera_lectura = False


class MainListingParser(HTMLParser):
    """
    Parser HTML para extraer el listado principal de estudiantes asignados.
    """

    def __init__(self):
        """Inicializa el parser del listado principal."""
        super().__init__()
        self.reset()
        self._lista: List[List[str]] = []
        self._estudiante_detectado: bool = False
        self._contador: int = 0
        self._datos_temporales: List[str] = []

    def get_lista(self) -> List[List[str]]:
        """
        Obtiene la lista de estudiantes procesados.
        
        Returns:
            Lista con información de cada estudiante [clave, carne, nombre, correo]
        """
        return self._lista

    def handle_starttag(self, tag: str, attrs: List[tuple]) -> None:
        """
        Maneja las etiquetas de apertura HTML.
        
        Args:
            tag: Nombre de la etiqueta HTML
            attrs: Atributos de la etiqueta
        """
        if tag == 'input':
            atributos = dict(attrs)
            if 'name' in atributos and atributos['name'] == 'radio':
                # Procesar la clave del estudiante
                clave_raw = '!!'.join(atributos['value'].split(','))
                clave_encoded = base64.b64encode(clave_raw.encode("utf-8")).decode("utf-8")
                
                self._estudiante_detectado = True
                self._datos_temporales = [clave_encoded]
                self._lista.append(self._datos_temporales)

        if tag == 'td' and self._estudiante_detectado:
            self._contador += 1
            if self._contador == 5:  # Se completaron las columnas del estudiante
                self._contador = 0
                self._estudiante_detectado = False

    def handle_data(self, data: str) -> None:
        """
        Maneja el contenido de texto de las etiquetas HTML.
        
        Args:
            data: Contenido de texto
        """
        if self._estudiante_detectado and data.strip():
            self._datos_temporales.append(data.strip())
