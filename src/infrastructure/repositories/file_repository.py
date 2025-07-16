"""
Repositorio para manejo de archivos del sistema
"""
import os
import csv
from typing import List, Dict, Optional
from pathlib import Path


class FileRepository:
    """
    Repositorio que maneja la persistencia de datos en archivos del sistema de archivos.
    """

    def __init__(self, base_path: str = '.'):
        """
        Inicializa el repositorio de archivos.
        
        Args:
            base_path: Ruta base donde se crearán los directorios
        """
        self.base_path = Path(base_path)
        self.directorio_expedientes = self.base_path / 'expediente'
        self.directorio_solicitudes = self.base_path / 'solicitudes'
        self.directorio_salida = self.base_path / 'salida'

    def _asegurar_directorio(self, directorio: Path) -> None:
        """
        Asegura que un directorio exista, lo crea si no existe.
        
        Args:
            directorio: Ruta del directorio a crear
        """
        directorio.mkdir(parents=True, exist_ok=True)

    def escribir_historial(
        self, 
        archivo: str, 
        encabezado: List[str], 
        historial: List[Dict[str, str]]
    ) -> None:
        """
        Escribe el historial académico de un estudiante a un archivo.
        
        Args:
            archivo: Nombre del archivo (normalmente el carné)
            encabezado: Lista con los nombres de las columnas
            historial: Lista de diccionarios con los datos del historial
        """
        self._asegurar_directorio(self.directorio_expedientes)
        
        archivo_path = self.directorio_expedientes / f'{archivo}.sdf'
        
        with open(archivo_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=encabezado, delimiter='\t', dialect='excel')
            writer.writeheader()
            for registro in historial:
                writer.writerow(registro)

    def leer_historial(self, archivo: str) -> List[Dict[str, str]]:
        """
        Lee el historial académico de un estudiante desde un archivo.
        
        Args:
            archivo: Nombre del archivo (normalmente el carné)
        
        Returns:
            Lista de diccionarios con los datos del historial
        
        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        archivo_path = self.directorio_expedientes / f'{archivo}.sdf'
        
        if not archivo_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de historial: {archivo_path}")
        
        historial = []
        with open(archivo_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t', dialect='excel')
            for linea in reader:
                historial.append(dict(linea))
        
        return historial

    def escribir_informacion_estudiante(self, archivo: str, carne: str, nombre: str) -> None:
        """
        Escribe la información básica de un estudiante a un archivo.
        
        Args:
            archivo: Nombre del archivo (normalmente el carné)
            carne: Carné del estudiante
            nombre: Nombre del estudiante
        """
        self._asegurar_directorio(self.directorio_expedientes)
        
        archivo_path = self.directorio_expedientes / f'{archivo}.edf'
        
        with open(archivo_path, 'w', encoding='utf-8') as file:
            file.write(f'{carne}\n')
            file.write(nombre)

    def leer_informacion_estudiante(self, archivo: str) -> tuple[str, str]:
        """
        Lee la información básica de un estudiante desde un archivo.
        
        Args:
            archivo: Nombre del archivo (normalmente el carné)
        
        Returns:
            Tupla con (carné, nombre) del estudiante
        
        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        archivo_path = self.directorio_expedientes / f'{archivo}.edf'
        
        if not archivo_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de información: {archivo_path}")
        
        with open(archivo_path, 'r', encoding='utf-8') as file:
            lineas = file.readlines()
            carne = lineas[0].strip() if len(lineas) > 0 else ''
            nombre = lineas[1].strip() if len(lineas) > 1 else ''
        
        return carne, nombre

    def escribir_cursos_solicitados(
        self, 
        archivo: str, 
        encabezado: List[str], 
        cursos_solicitados: List[Dict[str, str]]
    ) -> None:
        """
        Escribe los cursos solicitados por un estudiante a un archivo.
        
        Args:
            archivo: Nombre del archivo
            encabezado: Lista con los nombres de las columnas
            cursos_solicitados: Lista de diccionarios con los cursos solicitados
        """
        self._asegurar_directorio(self.directorio_solicitudes)
        
        archivo_path = self.directorio_solicitudes / f'{archivo}.sdf'
        
        with open(archivo_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=encabezado, delimiter='\t', dialect='excel')
            writer.writeheader()
            for curso in cursos_solicitados:
                writer.writerow(curso)

    def escribir_comentarios(self, archivo: str, estudiante: str, revision: str) -> None:
        """
        Escribe comentarios de revisión para un estudiante.
        
        Args:
            archivo: Nombre del archivo
            estudiante: Información del estudiante
            revision: Comentarios de revisión
        """
        self._asegurar_directorio(self.directorio_solicitudes)
        
        archivo_path = self.directorio_solicitudes / f'{archivo}.edf'
        
        with open(archivo_path, 'w', encoding='utf-8') as file:
            file.write(f'estudiante:{estudiante}\n')
            file.write(f'rev:{revision}')

    def listar_archivos_expedientes(self) -> List[str]:
        """
        Lista todos los archivos de expedientes disponibles.
        
        Returns:
            Lista de nombres de archivos de expedientes (.edf)
        """
        if not self.directorio_expedientes.exists():
            return []
        
        return [
            archivo.name for archivo in self.directorio_expedientes.glob('*.edf')
        ]

    def obtener_ruta_salida(self, nombre_archivo: str) -> Path:
        """
        Obtiene la ruta completa para un archivo de salida.
        
        Args:
            nombre_archivo: Nombre del archivo de salida
        
        Returns:
            Ruta completa del archivo de salida
        """
        self._asegurar_directorio(self.directorio_salida)
        return self.directorio_salida / nombre_archivo
