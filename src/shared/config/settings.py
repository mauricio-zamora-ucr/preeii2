"""
Configuración general de la aplicación
"""
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class UrlsConfig:
    """URLs utilizadas para el web scraping del sistema de matrícula."""
    home: str = 'https://ematricula.ucr.ac.cr/ematricula/admin/showAdminLogin.do'
    login: str = 'https://ematricula.ucr.ac.cr/ematricula/admin/loginAdmin.do'
    listado: str = 'https://ematricula.ucr.ac.cr/ematricula/admin/profesorExpedienteEstud.do'
    comentarios: str = 'https://ematricula.ucr.ac.cr/ematricula/admin/showComentariosProfEstud.do?c={}'
    notas: str = 'https://ematricula.ucr.ac.cr/ematricula/admin/nivelAvance.do?c={}'


@dataclass
class AuthConfig:
    """Configuración de autenticación."""
    user: str = ''
    password: str = ''


@dataclass
class ApplicationConfig:
    """Configuración general de la aplicación."""
    debug: bool = True
    urls: UrlsConfig = field(default_factory=UrlsConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)


# Instancia global de configuración
app_config = ApplicationConfig()

# Datos de la configuración de cursos (detalle_cursos de config.py original)
DETALLE_CURSOS: List[Dict[str, Any]] = [
    {'sigla': 'EF-D', 'curso': 'ACTIVIDAD DEPORTIVA', 'creditos': 0, 'semestre': 1},
    {'sigla': 'EG-CA', 'curso': 'CURSO DE ARTE', 'creditos': 2, 'semestre': 1},
    {'sigla': 'EG-I', 'curso': 'CURSO INTEGRADO DE HUMANIDADES I', 'creditos': 6, 'semestre': 1},
    {'sigla': 'MA1001', 'curso': 'CÁLCULO I', 'creditos': 3, 'semestre': 1},
    {'sigla': 'QU0100', 'curso': 'QUÍMICA GENERAL I', 'creditos': 3, 'correquisitos': ['QU0101'], 'semestre': 1},
    {'sigla': 'QU0101', 'curso': 'LABORATORIO DE QUÍMICA GENERAL I', 'creditos': 1, 'correquisitos': ['QU0100'], 'semestre': 1},
    {'sigla': 'RP-1', 'curso': 'REPERTORIO', 'creditos': 3, 'semestre': 1},
    {'sigla': 'EG-II', 'curso': 'CURSO INTEGRADO DE HUMANIDADES II', 'creditos': 6, 'semestre': 2},
    {'sigla': 'FS0210', 'curso': 'FÍSICA GENERAL I', 'creditos': 3, 'requisitos': ['MA1001'], 'correquisitos': ['FS0211'], 'semestre': 2},
    {'sigla': 'FS0211', 'curso': 'LABORATORIO DE FÍSICA GENERAL I', 'creditos': 1, 'requisitos': ['MA1001'], 'correquisitos': ['FS0210'], 'semestre': 2},
    {'sigla': 'II0201', 'curso': 'INTRODUCCIÓN A LA INGENIERÍA INDUSTRIAL', 'creditos': 2, 'semestre': 2},
    {'sigla': 'MA1002', 'curso': 'CÁLCULO II', 'creditos': 4, 'requisitos': ['MA1001'], 'semestre': 2},
    {'sigla': 'QU0102', 'curso': 'QUÍMICA GENERAL II', 'creditos': 3, 'requisitos': ['QU0100', 'QU0101'], 'correquisitos': ['QU0103'], 'semestre': 2},
    {'sigla': 'QU0103', 'curso': 'LABORATORIO DE QUÍMICA GENERAL II', 'creditos': 1, 'requisitos': ['QU0100', 'QU0101'], 'correquisitos': ['QU0102'], 'semestre': 2},
    {'sigla': 'CI0202', 'curso': 'PRINCIPIOS DE INFORMÁTICA', 'creditos': 4, 'requisitos': ['MA0205'], 'semestre': 3},
    {'sigla': 'FS0310', 'curso': 'FÍSICA GENERAL II', 'creditos': 3, 'requisitos': ['FS0210', 'FS0211', 'MA1002'], 'correquisitos': ['FS0311'], 'semestre': 3},
    {'sigla': 'FS0311', 'curso': 'LABORATORIO DE FÍSICA GENERAL II', 'creditos': 1, 'requisitos': ['FS0210', 'FS0211', 'MA1002'], 'correquisitos': ['FS0310'], 'semestre': 3},
    {'sigla': 'II0306', 'curso': 'PROBABILIDAD Y ESTADÍSTICA', 'creditos': 3, 'requisitos': ['MA1002'], 'semestre': 3},
    {'sigla': 'MA1003', 'curso': 'CÁLCULO III', 'creditos': 4, 'requisitos': ['MA1002'], 'correquisitos': ['MA1004'], 'semestre': 3},
    {'sigla': 'MA1004', 'curso': 'ÁLGEBRA LINEAL', 'creditos': 3, 'semestre': 3},
    {'sigla': 'FS0410', 'curso': 'FÍSICA GENERAL III', 'creditos': 3, 'requisitos': ['FS0310', 'FS0311', 'MA1003'], 'correquisitos': ['FS0411'], 'semestre': 4},
    {'sigla': 'FS0411', 'curso': 'LABORATORIO DE FÍSICA GENERAL III', 'creditos': 1, 'requisitos': ['FS0310', 'FS0311', 'MA0450'], 'correquisitos': ['FS0410'], 'semestre': 4},
    {'sigla': 'II0401', 'curso': 'INVESTIGACIÓN DE OPERACIONES', 'creditos': 3, 'requisitos': ['II0306', 'MA1004'], 'semestre': 4},
    {'sigla': 'II0402', 'curso': 'INGENIERÍA DE CALIDAD I', 'creditos': 2, 'requisitos': ['II0306'], 'semestre': 4},
    {'sigla': 'II0501', 'curso': 'TECNOLOGÍAS DE INFORMACIÓN', 'creditos': 2, 'requisitos': ['CI0202'], 'semestre': 4},
    {'sigla': 'IM0202', 'curso': 'DIBUJO I', 'creditos': 3, 'requisitos': ['FS0210', 'MA1001'], 'semestre': 4},
    {'sigla': 'MA1005', 'curso': 'ECUACIONES DIFERENCIALES', 'creditos': 4, 'requisitos': ['MA1002', 'MA1004'], 'semestre': 4},
    {'sigla': 'IE0303', 'curso': 'ELECTROTECNIA I', 'creditos': 3, 'requisitos': ['FS0310', 'FS0311', 'MA1003'], 'semestre': 5},
    {'sigla': 'II0302', 'curso': 'DISEÑO DEL TRABAJO E INGENIERÍA DE FACTORES HUMANOS', 'creditos': 3, 'requisitos': ['II0306'], 'semestre': 5},
    {'sigla': 'II0502', 'curso': 'INGENIERÍA DE CALIDAD II', 'creditos': 4, 'requisitos': ['II0402'], 'semestre': 5},
    {'sigla': 'II0503', 'curso': 'SIMULACIÓN', 'creditos': 3, 'requisitos': ['CI0202', 'II0401'], 'semestre': 5},
    {'sigla': 'II0504', 'curso': 'ADMINISTRACIÓN FINANCIERA Y CONTABLE I', 'creditos': 2, 'requisitos': ['II0201'], 'semestre': 5},
    {'sigla': 'IM0207', 'curso': 'MECÁNICA I', 'creditos': 3, 'requisitos': ['FS0210', 'FS0211', 'IM0202', 'MA1002'], 'semestre': 5},
    {'sigla': 'II0601', 'curso': 'GESTIÓN DE CALIDAD', 'creditos': 4, 'requisitos': ['II0502'], 'semestre': 6},
    {'sigla': 'II0603', 'curso': 'SISTEMAS AUTOMATIZADOS DE MANUFACTURA', 'creditos': 3, 'requisitos': ['FS0410', 'FS0411', 'IE0303', 'II0302', 'II0503', 'II0504'], 'semestre': 6},
    {'sigla': 'II0604', 'curso': 'ADMINISTRACIÓN FINANCIERA Y CONTABLE II', 'creditos': 2, 'requisitos': ['II0504'], 'semestre': 6},
    {'sigla': 'II0605', 'curso': 'LOGÍSTICA DE LA CADENA DEL VALOR I', 'creditos': 3, 'requisitos': ['II0401'], 'semestre': 6},
    {'sigla': 'II0606', 'curso': 'TERMOFLUIDOS', 'creditos': 3, 'requisitos': ['FS0310', 'FS0311', 'IE0303', 'IM0207', 'QU0102', 'QU0103'], 'semestre': 6},
    {'sigla': 'II0701', 'curso': 'DISEÑO DE SISTEMAS DE INFORMACIÓN', 'creditos': 3, 'requisitos': ['II0501'], 'semestre': 6},
    {'sigla': 'II0602', 'curso': 'DISEÑO DE EXPERIMENTOS', 'creditos': 3, 'requisitos': ['II0601'], 'semestre': 7},
    {'sigla': 'II0702', 'curso': 'COMPORTAMIENTO ORGANIZACIONAL', 'creditos': 2, 'requisitos': ['II0302'], 'semestre': 7},
    {'sigla': 'II0703', 'curso': 'INGENIERÍA DE OPERACIONES', 'creditos': 4, 'requisitos': ['II0603', 'II0604', 'II0605', 'II0701'], 'semestre': 7},
    {'sigla': 'II0704', 'curso': 'INGENIERÍA ECONÓMICA Y FINANCIERA', 'creditos': 3, 'requisitos': ['II0604'], 'correquisitos': ['II0703'], 'semestre': 7},
    {'sigla': 'II0705', 'curso': 'LOGÍSTICA DE LA CADENA DEL VALOR II', 'creditos': 4, 'requisitos': ['II0605'], 'semestre': 7},
    {'sigla': 'SR-I', 'curso': 'SEMINARIO DE REALIDAD NACIONAL I', 'creditos': 2, 'semestre': 7},
    {'sigla': 'II0802', 'curso': 'INGENIERÍA DE PROCESOS DE NEGOCIO', 'creditos': 4, 'requisitos': ['II0702'], 'semestre': 8},
    {'sigla': 'II0803', 'curso': 'DISEÑO DE PRODUCTO', 'creditos': 3, 'requisitos': ['II0704'], 'correquisitos': ['II0804'], 'semestre': 8},
    {'sigla': 'II0804', 'curso': 'GESTIÓN DE PROYECTOS', 'creditos': 3, 'requisitos': ['II0704'], 'semestre': 8},
    {'sigla': 'II0805', 'curso': 'DISTRIBUCIÓN Y LOCALIZACIÓN DE INSTALACIONES', 'creditos': 4, 'requisitos': ['II0703', 'II0705'], 'semestre': 8},
    {'sigla': 'II0806', 'curso': 'METROLOGÍA Y NORMALIZACIÓN', 'creditos': 3, 'requisitos': ['II0602'], 'semestre': 8},
    {'sigla': 'SR-II', 'curso': 'SEMINARIO DE REALIDAD NACIONAL II', 'creditos': 2, 'semestre': 8},
    {'sigla': 'II0801', 'curso': 'INGENIERÍA DE SERVICIOS', 'creditos': 3, 'requisitos': ['II0601', 'II0703', 'II0705'], 'semestre': 9},
    {'sigla': 'II0902', 'curso': 'PROYECTO INDUSTRIAL', 'creditos': 3, 'semestre': 9},
    {'sigla': 'II0904', 'curso': 'INGENIERÍA AMBIENTAL', 'creditos': 3, 'requisitos': ['II0601', 'II0804'], 'semestre': 9},
    {'sigla': 'II0905', 'curso': 'INGENIERÍA DE MANUFACTURA', 'creditos': 3, 'requisitos': ['II0703', 'II0803', 'II0805'], 'semestre': 9},
    {'sigla': 'II0906', 'curso': 'GESTIÓN DE MANTENIMIENTO', 'creditos': 3, 'requisitos': ['II0601', 'II0603', 'II0606'], 'semestre': 9},
    {'sigla': 'OPT408a', 'curso': 'BLOQUE OPTATIVO 408', 'creditos': 3, 'semestre': 9},
    {'sigla': 'II1001', 'curso': 'RESPONSABILIDAD SOCIAL', 'creditos': 2, 'requisitos': ['II0904'], 'semestre': 10},
    {'sigla': 'II9500', 'curso': 'INVESTIGACIÓN DIRIGIDA I', 'creditos': 0, 'requisitos': ['II0902'], 'semestre': 10},
    {'sigla': 'OPT408b', 'curso': 'IBLOQUE OPTATIVO 408', 'creditos': 3, 'semestre': 10},
    {'sigla': 'II9501', 'curso': 'INVESTIGACIÓN DIRIGIDA II', 'creditos': 0, 'semestre': 11},
    {'sigla': 'II9502', 'curso': 'INVESTIGACIÓN DIRIGIDA III', 'creditos': 0, 'semestre': 12}
]
