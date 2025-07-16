"""
Entidad Expediente del dominio
"""
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

from .semestre import Semestre
from .curso_carrera import CursoCarrera
from .historial import Historial


@dataclass
class Expediente:
    """
    Representa el expediente académico completo de un estudiante.
    """
    carne: str = ''
    nombre: str = ''
    semestres: Dict[int, Semestre] = field(default_factory=dict)
    siglas: List[str] = field(default_factory=list)
    optativos: List[Dict[str, str]] = field(default_factory=list)
    otros_cursos: List[Dict[str, str]] = field(default_factory=list)

    def agregar_semestre(self, semestre: Semestre) -> None:
        """Agrega un semestre al expediente."""
        self.semestres[semestre.numero] = semestre
        self.siglas.extend(semestre.siglas)

    def obtener_semestres_completos(self) -> List[Tuple[int, bool]]:
        """Obtiene una lista de tuplas con el número de semestre y si está completo."""
        return [(numero, semestre.esta_completo()) for numero, semestre in self.semestres.items()]

    def agregar_curso(self, datos_curso: Dict[str, str]) -> None:
        """Agrega un curso al expediente basado en los datos proporcionados."""
        sigla = datos_curso['SIGLA']
        sigla_normalizada = self._convertir_sigla_normalizada(sigla)
        nombre = datos_curso['CURSO']
        
        try:
            grupo = int(datos_curso['GRUPO'])
        except (ValueError, TypeError):
            grupo = 0

        periodo = self._convertir_periodo(datos_curso.get('SEM', ''))
        
        try:
            anno = int(datos_curso['AÑO'])
        except (ValueError, TypeError):
            anno = 0

        estado = datos_curso['ESTADO']
        nota = self._normalizar_nota(datos_curso.get('NOTA'))

        # Buscar el curso en los semestres existentes
        encontrado = False
        for semestre in self.semestres.values():
            if semestre.tiene_curso(sigla_normalizada):
                encontrado = True
                curso = semestre.cursos_por_sigla[sigla_normalizada]
                historial = Historial(
                    sigla=sigla,
                    sigla_normalizada=sigla_normalizada,
                    nombre=nombre,
                    grupo=grupo,
                    periodo=periodo,
                    anno=anno,
                    estado=estado,
                    nota=nota
                )
                curso.agregar_historial(historial)
                break

        if not encontrado:
            if sigla.startswith('II'):
                self.optativos.append(datos_curso)
            else:
                self.otros_cursos.append(datos_curso)

    def obtener_cursos_aprobados(self) -> List[str]:
        """Obtiene todas las siglas de cursos aprobados en todo el expediente."""
        cursos_aprobados = []
        for semestre in self.semestres.values():
            cursos_aprobados.extend(semestre.obtener_cursos_aprobados())
        cursos_aprobados.sort()
        return cursos_aprobados

    def obtener_cursos_matriculados(self) -> List[str]:
        """Obtiene todas las siglas de cursos matriculados en todo el expediente."""
        cursos_matriculados = []
        for semestre in self.semestres.values():
            cursos_matriculados.extend(semestre.obtener_cursos_matriculados())
        cursos_matriculados.sort()
        return cursos_matriculados

    def obtener_cursos_retirados(self) -> List[str]:
        """Obtiene todas las siglas de cursos retirados en todo el expediente."""
        cursos_retirados = []
        for semestre in self.semestres.values():
            cursos_retirados.extend(semestre.obtener_cursos_retirados())
        cursos_retirados.sort()
        return cursos_retirados

    def obtener_cursos_reprobados(self) -> List[str]:
        """Obtiene todas las siglas de cursos reprobados en todo el expediente."""
        cursos_reprobados = []
        for semestre in self.semestres.values():
            cursos_reprobados.extend(semestre.obtener_cursos_reprobados())
        cursos_reprobados.sort()
        return cursos_reprobados

    def procesar_requisitos_correquisitos(self) -> None:
        """Procesa y actualiza el estado de todos los requisitos y correquisitos."""
        cursos_aprobados = self.obtener_cursos_aprobados()
        cursos_matriculados = self.obtener_cursos_matriculados()
        cursos_reprobados = self.obtener_cursos_reprobados()
        cursos_retirados = self.obtener_cursos_retirados()

        for semestre in self.semestres.values():
            for curso in semestre.cursos:
                curso.verificar_requisitos_correquisitos_aprobados(cursos_aprobados)
                curso.verificar_requisitos_correquisitos_matriculados(cursos_matriculados)
                curso.verificar_requisitos_correquisitos_reprobados(cursos_reprobados)
                curso.verificar_requisitos_correquisitos_retirados(cursos_retirados)

    @staticmethod
    def _convertir_sigla_normalizada(sigla: str) -> str:
        """Convierte una sigla a su forma normalizada según las reglas de la UCR."""
        sigla_normalizada = sigla

        conversiones = {
            'EF': 'EF-D',
            'RP': 'RP-1',
            'EG03': 'EG-CA',
            'EG0124': 'EG-I',
            'EG0126': 'EG-I',
            'EG0125': 'EG-II',
            'EG0127': 'EG-II',
            'SR0001': 'SR-I',
            'SR0002': 'SR-I',
            'SR0003': 'SR-I',
            'SR0004': 'SR-I',
            'SR0005': 'SR-I',
            'SR0006': 'SR-I',
            'SR0007': 'SR-I',
            'SR0008': 'SR-I',
            'SR0010': 'SR-I',
            'SR0011': 'SR-II',
            'SR0022': 'SR-II',
            'SR0033': 'SR-II',
            'SR0044': 'SR-II',
            'SR0055': 'SR-II',
            'SR0066': 'SR-II',
            'SR0077': 'SR-II',
            'SR0088': 'SR-II',
            'SR0110': 'SR-II',
        }

        for prefijo, normalizada in conversiones.items():
            if sigla.startswith(prefijo):
                sigla_normalizada = normalizada
                break

        return sigla_normalizada

    @staticmethod
    def _convertir_periodo(semestre_str: str) -> int:
        """Convierte la representación string del semestre a número."""
        if semestre_str == 'I':
            return 1
        elif semestre_str == 'II':
            return 2
        else:
            return 3

    @staticmethod
    def _normalizar_nota(nota_str: Optional[str]) -> Optional[str]:
        """Normaliza la nota a string o None."""
        if nota_str is None:
            return None
        try:
            return str(float(nota_str))
        except (ValueError, TypeError):
            return '' if nota_str is None else nota_str
