"""
Entidad CursoCarrera del dominio
"""
from typing import List, Dict, Optional
from dataclasses import dataclass, field

from .curso import Curso
from .historial import Historial
from .enums import EstadoCurso, EstadoRequisito


@dataclass
class CursoCarrera(Curso):
    """
    Representa un curso específico dentro de una carrera académica.
    Extiende la entidad Curso con información específica de la malla curricular.
    """
    historial: List[Historial] = field(default_factory=list)
    requisitos: Dict[str, int] = field(default_factory=dict)
    correquisitos: Dict[str, int] = field(default_factory=dict)

    def tiene_requisitos(self) -> bool:
        """Verifica si el curso tiene requisitos definidos."""
        return bool(self.requisitos)

    def agregar_requisito(self, sigla: str) -> None:
        """Agrega un requisito al curso."""
        self.requisitos[sigla] = EstadoRequisito.SIN_DATOS.value

    def cumple_requisitos(self) -> bool:
        """Verifica si todos los requisitos están aprobados."""
        if not self.requisitos:
            return True
        return all(estado == EstadoRequisito.APROBADO.value for estado in self.requisitos.values())

    def tiene_correquisitos(self) -> bool:
        """Verifica si el curso tiene correquisitos definidos."""
        return bool(self.correquisitos)

    def agregar_correquisito(self, sigla: str) -> None:
        """Agrega un correquisito al curso."""
        self.correquisitos[sigla] = EstadoRequisito.SIN_DATOS.value

    def cumple_correquisitos(self) -> bool:
        """Verifica si todos los correquisitos están aprobados."""
        if not self.correquisitos:
            return True
        return all(estado == EstadoRequisito.APROBADO.value for estado in self.correquisitos.values())

    def verificar_requisitos_correquisitos_aprobados(self, siglas_cursos_aprobados: List[str]) -> None:
        """Actualiza el estado de requisitos y correquisitos basado en cursos aprobados."""
        if not siglas_cursos_aprobados:
            return
            
        for sigla in self.requisitos.keys():
            if sigla in siglas_cursos_aprobados:
                self.requisitos[sigla] = EstadoRequisito.APROBADO.value
                
        for sigla in self.correquisitos.keys():
            if sigla in siglas_cursos_aprobados:
                self.correquisitos[sigla] = EstadoRequisito.APROBADO.value

    def verificar_requisitos_correquisitos_matriculados(self, siglas_cursos_matriculados: List[str]) -> None:
        """Actualiza el estado de requisitos y correquisitos basado en cursos matriculados."""
        if not siglas_cursos_matriculados:
            return
            
        for sigla in self.requisitos.keys():
            if sigla in siglas_cursos_matriculados:
                self.requisitos[sigla] = EstadoRequisito.MATRICULADO.value
                
        for sigla in self.correquisitos.keys():
            if sigla in siglas_cursos_matriculados:
                self.correquisitos[sigla] = EstadoRequisito.MATRICULADO.value

    def verificar_requisitos_correquisitos_reprobados(self, siglas_cursos_reprobados: List[str]) -> None:
        """Actualiza el estado de requisitos y correquisitos basado en cursos reprobados."""
        if not siglas_cursos_reprobados:
            return
            
        for sigla in self.requisitos.keys():
            if sigla in siglas_cursos_reprobados:
                self.requisitos[sigla] = EstadoRequisito.REPROBADO.value
                
        for sigla in self.correquisitos.keys():
            if sigla in siglas_cursos_reprobados:
                self.correquisitos[sigla] = EstadoRequisito.REPROBADO.value

    def verificar_requisitos_correquisitos_retirados(self, siglas_cursos_retirados: List[str]) -> None:
        """Actualiza el estado de requisitos y correquisitos basado en cursos retirados."""
        if not siglas_cursos_retirados:
            return
            
        for sigla in self.requisitos.keys():
            if sigla in siglas_cursos_retirados:
                self.requisitos[sigla] = EstadoRequisito.RETIRADO.value
                
        for sigla in self.correquisitos.keys():
            if sigla in siglas_cursos_retirados:
                self.correquisitos[sigla] = EstadoRequisito.RETIRADO.value

    def agregar_historial(self, historial: Historial) -> None:
        """Agrega un registro de historial y ordena por año y período (más reciente primero)."""
        self.historial.append(historial)
        self.historial.sort(key=lambda h: (h.anno, h.periodo), reverse=True)

    def get_nota_actual(self) -> str:
        """Obtiene la nota del registro más reciente del historial."""
        if self.historial:
            return self.historial[0].nota or ''
        return ''

    def get_estado_actual(self) -> str:
        """Obtiene el estado del registro más reciente del historial."""
        if self.historial:
            return self.historial[0].estado
        return ''

    def esta_aprobado(self) -> bool:
        """Verifica si el curso está aprobado según el estado actual."""
        return EstadoCurso.es_aprobado(self.get_estado_actual())

    def get_anno_actual(self) -> Optional[int]:
        """Obtiene el año del registro más reciente del historial."""
        if self.historial:
            return self.historial[0].anno
        return None

    def get_periodo_actual(self) -> Optional[int]:
        """Obtiene el período del registro más reciente del historial."""
        if self.historial:
            return self.historial[0].periodo
        return None

    def __str__(self) -> str:
        """Representación en string del curso de carrera."""
        periodo = self.get_periodo_actual() if self.get_periodo_actual() is not None else ''
        anno = self.get_anno_actual() if self.get_anno_actual() is not None else ''
        salida = f'\t{super().__str__()} {periodo:>3} {anno:4} {self.get_nota_actual():4}\n'
        
        if self.historial:
            salida += '\t\tHistorial:'
            for h in self.historial:
                salida += f'\n\t\t{str(h)}'
        else:
            salida += '\t\tSin Historial'
            
        return salida
