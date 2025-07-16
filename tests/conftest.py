"""
Configuración para pruebas del proyecto
"""
import pytest
import sys
import os

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

@pytest.fixture
def sample_expediente_data():
    """Datos de ejemplo para pruebas de expediente."""
    return {
        'carne': 'C12345',
        'nombre': 'Juan Pérez Rodríguez',
        'historial': [
            {
                'SIGLA': 'MA1001',
                'CURSO': 'CÁLCULO I',
                'CREDITOS': '3',
                'GRUPO': '01',
                'SEM': 'I',
                'AÑO': '2023',
                'ESTADO': 'APROBADO',
                'NOTA': '8.5'
            }
        ]
    }

@pytest.fixture
def sample_cursos_data():
    """Datos de ejemplo para pruebas de cursos."""
    return [
        {
            'sigla': 'MA1001',
            'curso': 'CÁLCULO I',
            'creditos': 3,
            'semestre': 1
        },
        {
            'sigla': 'MA1002',
            'curso': 'CÁLCULO II',
            'creditos': 4,
            'requisitos': ['MA1001'],
            'semestre': 2
        }
    ]
