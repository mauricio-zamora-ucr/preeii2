"""
Enumeraciones y constantes del dominio
"""
from enum import Enum


class EstadoCurso(Enum):
    """
    Estados posibles de un curso en el sistema académico.
    """
    SIN_DATOS = 0
    MATRICULADO = 1
    REPROBADO = 2
    RETIRADO = 3
    APROBADO = 4
    CONVALIDADO = 5
    EQUIVALENTE = 6

    @classmethod
    def estados_aprobados(cls) -> list['EstadoCurso']:
        """Retorna los estados que se consideran como aprobados."""
        return [cls.APROBADO, cls.EQUIVALENTE, cls.CONVALIDADO]

    @classmethod
    def es_aprobado(cls, estado: str) -> bool:
        """Verifica si un estado en string corresponde a un curso aprobado."""
        return estado in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO']


class EstadoRequisito(Enum):
    """
    Estados de cumplimiento de requisitos y correquisitos.
    """
    SIN_DATOS = 0
    MATRICULADO = 1
    REPROBADO = 2
    RETIRADO = 3
    APROBADO = 4
    CONVALIDADO = 5
