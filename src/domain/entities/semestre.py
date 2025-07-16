"""
Entidad Semestre del dominio
"""
from typing import List, Dict
from dataclasses import dataclass, field

from .curso_carrera import CursoCarrera
from .enums import EstadoCurso


@dataclass
class Semestre:
    """
    Representa un semestre académico con todos sus cursos asociados.
    """
    numero: int
    cursos: List[CursoCarrera] = field(default_factory=list)
    cursos_por_sigla: Dict[str, CursoCarrera] = field(default_factory=dict)
    siglas: List[str] = field(default_factory=list)

    def obtener_cursos_aprobados(self) -> List[str]:
        """Obtiene las siglas de todos los cursos aprobados en este semestre."""
        return [
            c.sigla for c in self.cursos 
            if c.get_estado_actual() in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO']
        ]

    def obtener_cursos_matriculados(self) -> List[str]:
        """Obtiene las siglas de todos los cursos matriculados en este semestre."""
        return [
            c.sigla for c in self.cursos 
            if c.get_estado_actual() == 'MATRICULADO'
        ]

    def obtener_cursos_retirados(self) -> List[str]:
        """Obtiene las siglas de todos los cursos retirados en este semestre."""
        return [
            c.sigla for c in self.cursos 
            if c.get_estado_actual() == 'RETIRO DE MA'
        ]

    def obtener_cursos_reprobados(self) -> List[str]:
        """Obtiene las siglas de todos los cursos reprobados en este semestre."""
        return [
            c.sigla for c in self.cursos 
            if c.get_estado_actual() == 'REPROBADO'
        ]

    def agregar_curso(self, curso: CursoCarrera) -> None:
        """Agrega un curso al semestre y actualiza los índices."""
        self.cursos.append(curso)
        self.siglas.append(curso.sigla)
        self.cursos_por_sigla[curso.sigla] = curso
        self.siglas.sort()

    def obtener_maximo_historial(self) -> int:
        """Obtiene el máximo número de registros de historial entre todos los cursos."""
        if not self.cursos:
            return 0
        return max(len(c.historial) for c in self.cursos)

    def obtener_total_creditos(self) -> int:
        """Obtiene el total de créditos de todos los cursos del semestre."""
        return sum(c.creditos for c in self.cursos)

    def obtener_total_creditos_aprobados(self) -> int:
        """Obtiene el total de créditos de los cursos aprobados del semestre."""
        return sum(
            c.creditos for c in self.cursos 
            if EstadoCurso.es_aprobado(c.get_estado_actual())
        )

    def obtener_maximo_requisitos(self) -> int:
        """Obtiene el máximo número de requisitos entre todos los cursos."""
        cursos_con_requisitos = [c for c in self.cursos if c.tiene_requisitos()]
        if not cursos_con_requisitos:
            return 0
        return max(len(c.requisitos) for c in cursos_con_requisitos)

    def obtener_maximo_correquisitos(self) -> int:
        """Obtiene el máximo número de correquisitos entre todos los cursos."""
        cursos_con_correquisitos = [c for c in self.cursos if c.tiene_correquisitos()]
        if not cursos_con_correquisitos:
            return 0
        return max(len(c.correquisitos) for c in cursos_con_correquisitos)

    def esta_completo(self) -> bool:
        """Verifica si todos los cursos del semestre están aprobados."""
        return all(c.esta_aprobado() for c in self.cursos)

    def tiene_curso(self, sigla: str) -> bool:
        """Verifica si el semestre contiene un curso con la sigla especificada."""
        return sigla in self.siglas

    def __str__(self) -> str:
        """Representación en string del semestre."""
        return f'Semestre {self.numero:2}'
