"""
Entidad Curso del dominio
"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class Curso:
    """
    Representa un curso académico con toda su información relevante.
    """
    sigla: str
    nombre: str
    creditos: int
    nota: Optional[str] = None
    anno: Optional[int] = None
    periodo: Optional[int] = None
    semestre: Optional[int] = None
    estado: str = ''
    sigla_normalizada: Optional[str] = None

    def get_sigla_normalizada(self) -> str:
        """
        Retorna la sigla normalizada o la sigla original si no está definida.
        """
        return self.sigla_normalizada if self.sigla_normalizada is not None else self.sigla

    def __str__(self) -> str:
        """
        Representación en string del curso para fines de debugging o logging.
        """
        return (f'{self.sigla:8} {self.get_sigla_normalizada():8} '
                f'{self.nombre:75} {self.creditos:2d} {self.estado:15}')
