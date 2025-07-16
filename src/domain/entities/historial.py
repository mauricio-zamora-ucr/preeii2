"""
Entidad Historial del dominio
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Historial:
    """
    Representa el historial académico de un curso específico en un período determinado.
    """
    sigla: str
    sigla_normalizada: str
    nombre: str
    grupo: int
    periodo: int
    anno: int
    estado: str
    nota: Optional[str] = None

    def __str__(self) -> str:
        """
        Representación en string del historial para fines de debugging o logging.
        """
        nota_display = self.nota if self.nota is not None else ''
        return (f'{self.sigla:8} {self.sigla_normalizada:8} '
                f'{self.nombre:75} {self.periodo:3} {self.anno:4} '
                f'{nota_display:4} {self.estado:15}')
