"""
Domain entities
"""
from .curso import Curso
from .curso_carrera import CursoCarrera
from .expediente import Expediente
from .historial import Historial
from .semestre import Semestre
from .enums import EstadoCurso, EstadoRequisito

__all__ = [
    'Curso',
    'CursoCarrera', 
    'Expediente',
    'Historial',
    'Semestre',
    'EstadoCurso',
    'EstadoRequisito'
]
