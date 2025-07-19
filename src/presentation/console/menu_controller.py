"""
Controlador del menú principal de la aplicación
"""
import getpass
from datetime import datetime
from termcolor import cprint

from .console_utils import ConsoleUtils
from ...application.services.expediente_service import ExpedienteService
from ...application.services.web_scraping_service import WebScrapingService
from ...shared.config.settings import app_config


class MenuController:
    """
    Controlador principal del menú de la aplicación.
    """

    def __init__(self):
        """Inicializa el controlador del menú."""
        self.expediente_service = ExpedienteService()
        self.web_scraping_service = WebScrapingService()
        self.ancho_menu = 60

    def mostrar_menu_principal(self) -> None:
        """Muestra el menú principal y maneja la navegación."""
        fecha_expiracion = datetime(year=2026, month=2, day=28)
        
        while True:
            ahora = datetime.now()
            dias_restantes = (fecha_expiracion - ahora).days
            
            if dias_restantes < 0:
                self._mostrar_version_expirada()
                break

            ConsoleUtils.limpiar_pantalla()
            self._mostrar_encabezado_menu()
            self._mostrar_opciones_menu()
            self._mostrar_informacion_expiracion(dias_restantes)
            
            opcion = ConsoleUtils.leer_rango_numeros_enteros(
                'Digite la opción del menú:', 0, 5
            )
            
            if opcion == 0:
                self._opcion_salir()
                break
            elif opcion == 1:
                self._opcion_descargar_expedientes()
            elif opcion == 2:
                self._opcion_mostrar_informacion()
            elif opcion == 3:
                self._opcion_procesar_memoria()
            elif opcion == 4:
                self._opcion_regenerar_excel()
            elif opcion == 5:
                self._opcion_analisis_equiparacion()

    def _mostrar_encabezado_menu(self) -> None:
        """Muestra el encabezado del menú principal."""
        texto = f'{"MENU PRINCIPAL":^{self.ancho_menu}}'
        cprint(texto, 'blue', 'on_white')

    def _mostrar_opciones_menu(self) -> None:
        """Muestra las opciones del menú principal."""
        opciones = [
            (1, 'DESCARGAR EXPEDIENTES'),
            (2, 'INFORMACIÓN'),
            (3, 'PROCESAR EXPEDIENTE EN MEMORIA RAM'),
            (4, 'REGENERAR ARCHIVOS EXCEL'),
            (5, 'ANÁLISIS DE EQUIPARACIÓN'),
            (0, 'SALIR')
        ]
        
        for numero, descripcion in opciones:
            opcion_texto = f'{numero:2d} > {descripcion:55}'
            print(f'{opcion_texto:^{self.ancho_menu}}')
        
        desarrollador = 'DESARROLLADO POR MAURICIO ANDRÉS ZAMORA HERNÁNDEZ'
        print(f'{desarrollador:^{self.ancho_menu}}')

    def _mostrar_informacion_expiracion(self, dias_restantes: int) -> None:
        """
        Muestra información sobre la expiración de la versión.
        
        Args:
            dias_restantes: Días restantes antes de la expiración
        """
        texto_expiracion = f'{dias_restantes:3} DIAS PARA QUE DEJE FUNCIONAR ESTA VERSION DE PRUEBA'
        texto_centrado = f'{texto_expiracion:^{self.ancho_menu}}'
        cprint(texto_centrado, 'yellow', 'on_red')

    def _mostrar_version_expirada(self) -> None:
        """Muestra el mensaje de versión expirada."""
        mensajes = [
            'SE HA VENCIDO LA VERSION DE PRUEBAS',
            'POR FAVOR CONSULTAR POR LA VERSIÓN ACTUAL',
            'mauricio.zamora@gmail.com'
        ]
        
        for mensaje in mensajes:
            print(f'{mensaje:^{self.ancho_menu}}')

    def _opcion_descargar_expedientes(self) -> None:
        """Maneja la opción de descargar expedientes."""
        print('POR FAVOR ESCRIBA SUS CREDENCIALES DE LA UCR')
        
        usuario = ConsoleUtils.leer_texto('Usuario: (como el correo, pero sin el @ucr.ac.cr)')
        print(f'Usuario: {usuario}')
        
        try:
            clave = getpass.getpass('Contraseña: ')
        except Exception as error:
            print(f'ERROR: {error}')
            ConsoleUtils.pausar()
            return

        # Actualizar configuración
        app_config.auth.user = usuario
        app_config.auth.password = clave

        # Iniciar proceso de descarga
        if self.web_scraping_service.iniciar_proceso_descarga_completo(usuario, clave):
            self._procesar_archivos_expedientes()
        
        ConsoleUtils.pausar()

    def _opcion_mostrar_informacion(self) -> None:
        """Muestra información sobre la aplicación."""
        mensajes = [
            'ESTA ES UNA VERSIÓN DE PRUEBA',
            'EN CADA PREMATRICULA ALGO SE AGREGA O CORRIJE',
            '',
            'ESTE SOFTWARE ES DE TIPO "AS IS"',
            'https://en.wikipedia.org/wiki/As_is',
            '',
            'Este script fue hecho en mi tiempo libre,',
            'si quieren invitar a un combo de BK por',
            'semestre que lo usen se les agradece.',
            '',
            'por Mauricio Zamora',
            'mauricio@zamora.cr'
        ]
        
        for mensaje in mensajes:
            print(f'{mensaje:^{self.ancho_menu}}')
        
        ConsoleUtils.pausar()

    def _opcion_procesar_memoria(self) -> None:
        """Maneja la opción de procesar expediente desde memoria."""
        import pyperclip
        from ...infrastructure.adapters.html_parser import StudentParser
        from ...application.services.memory_reader_service import MemoryReaderService
        
        self._mostrar_titulo_procesador()
        
        try:
            texto = pyperclip.paste()
            memory_service = MemoryReaderService()
            
            if memory_service.procesar_contenido_memoria(texto):
                self._procesar_archivos_expedientes()
            
        except Exception as e:
            print(f'Error al procesar memoria: {str(e)}')
        
        ConsoleUtils.pausar()

    def _opcion_salir(self) -> None:
        """Maneja la opción de salir de la aplicación."""
        self._mostrar_mensaje_despedida()

    def _mostrar_titulo_procesador(self) -> None:
        """Muestra el título del procesador de prematrículas."""
        print("PROCESADOR DE PREMATRICULAS")
        print("Desarrollado por Mauricio Andrés Zamora Hernández")
        print("Versión 2022 ALFA")

    def _mostrar_mensaje_despedida(self) -> None:
        """Muestra el mensaje de despedida."""
        print("FINALIZADO")
        print("SI LA APLICACIÓN FUE DE UTILIDAD PUEDE DONAR")
        print("EL EQUIVALENTE A UN CAFECITO AL SINPE MOVIL 50123456 (SI ES UN NUMERO DE VERDAD)")
        print("SI REALMENTE LE GUSTO CONSIDERE DONAR UN WHOPPER")
        print("SI TIENE DUDAS, NO LLAME, NO WHATSAPP SOLO RESPONDO TELEGRAM")
        print("SIGA EL CANAL DE YT https://www.youtube.com/mauricioz7")

    def _procesar_archivos_expedientes(self) -> None:
        """Procesa todos los archivos de expedientes disponibles."""
        from ...infrastructure.repositories.file_repository import FileRepository
        import xlsxwriter
        from datetime import timedelta
        
        file_repo = FileRepository()
        archivos_expedientes = file_repo.listar_archivos_expedientes()
        
        if not archivos_expedientes:
            print("No se encontraron expedientes para procesar.")
            return

        tiempo_total = timedelta(seconds=0)
        self.expediente_service.imprimir_encabezado_procesamiento()
        
        for i, archivo in enumerate(archivos_expedientes):
            try:
                # Leer información del estudiante
                carne, nombre = file_repo.leer_informacion_estudiante(archivo.replace('.edf', ''))
                
                # Leer historial
                historial = file_repo.leer_historial(carne)
                
                # Procesar expediente
                expediente = self.expediente_service.procesar_expediente_estudiante(
                    carne, nombre, historial
                )
                
                # Calcular tiempo estimado
                tiempo = self.expediente_service.calcular_tiempo_estimado_revision(len(historial))
                tiempo_total += tiempo
                
                # Mostrar progreso
                self.expediente_service.imprimir_resumen_procesamiento(
                    carne, nombre, len(historial), tiempo, i % 2 == 0
                )
                
                # Generar archivo Excel
                self._generar_archivo_excel(expediente, file_repo)
                
            except Exception as e:
                print(f"Error procesando {archivo}: {str(e)}")
        
        # Mostrar tiempo total ahorrado
        self.expediente_service.imprimir_tiempo_total_ahorrado(tiempo_total)

    def _generar_archivo_excel(self, expediente, file_repo):
        """
        Genera un archivo Excel para el expediente.
        
        Args:
            expediente: Expediente del estudiante
            file_repo: Repositorio de archivos
        """
        import xlsxwriter
        from ...infrastructure.adapters.excel_writer import ExcelWriter
        
        nombre_archivo = f'{expediente.carne}-{expediente.nombre.upper()}.xlsx'
        ruta_salida = file_repo.obtener_ruta_salida(nombre_archivo)
        
        excel_writer = ExcelWriter()
        excel_writer.generar_expediente(expediente, str(ruta_salida))

    def _opcion_regenerar_excel(self) -> None:
        """Regenera archivos Excel desde expedientes existentes."""
        from ...infrastructure.repositories.file_repository import FileRepository
        
        print("REGENERACIÓN DE ARCHIVOS EXCEL")
        print("=" * self.ancho_menu)
        print("Esta opción regenera los archivos Excel desde los expedientes")
        print("que ya fueron descargados anteriormente.")
        print()
        
        file_repo = FileRepository()
        archivos_expedientes = file_repo.listar_archivos_expedientes()
        
        if not archivos_expedientes:
            cprint("No se encontraron expedientes para procesar.", 'white', 'on_red', attrs=['bold'])
            print("Primero debe descargar expedientes usando la opción 1.")
            ConsoleUtils.pausar()
            return

        print(f"Se encontraron {len(archivos_expedientes)} expedientes para procesar.")
        
        respuesta = ConsoleUtils.leer_texto("¿Desea continuar? (s/n): ").lower()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            return
        
        print()
        print("Procesando expedientes...")
        print("=" * self.ancho_menu)
        
        exitosos = 0
        errores = 0
        
        for i, archivo in enumerate(archivos_expedientes, 1):
            try:
                # Leer información del estudiante
                carne = archivo.replace('.edf', '')
                carne_info, nombre = file_repo.leer_informacion_estudiante(carne)
                
                # Leer historial
                historial = file_repo.leer_historial(carne)
                
                # Procesar expediente
                expediente = self.expediente_service.procesar_expediente_estudiante(
                    carne, nombre, historial
                )
                
                # Generar archivo Excel
                self._generar_archivo_excel(expediente, file_repo)
                
                # Mostrar progreso
                print(f"[{i:3d}/{len(archivos_expedientes)}] ✓ {carne} - {nombre[:30]}")
                exitosos += 1
                
            except Exception as e:
                print(f"[{i:3d}/{len(archivos_expedientes)}] ✗ Error en {archivo}: {str(e)}")
                errores += 1
        
        print()
        print("=" * self.ancho_menu)
        cprint(f"Proceso completado: {exitosos} exitosos, {errores} errores", 'green', attrs=['bold'])
        
        if exitosos > 0:
            print("Los archivos Excel se han generado en la carpeta 'salida/'")
            print("Cada archivo contiene 7 hojas especializadas:")
            print("  • Malla Curricular: Vista de mapa por semestres")
            print("  • Expediente Detallado: Vista tabular por semestres")
            print("  • Historial Completo: Todos los registros académicos")
            print("  • Análisis por Semestres: Rendimiento cronológico con gráficos")
            print("  • Progreso del Plan: Estado por semestre del plan")
            print("  • Cursos Pendientes: Análisis de requisitos para matrícula")
            print("  • Cursos Reprobados: Historial de intentos fallidos")
        
        ConsoleUtils.pausar()

    def _opcion_analisis_equiparacion(self) -> None:
        """Realiza análisis de equiparación para nuevo plan de estudios."""
        from ...infrastructure.adapters.equiparacion_analyzer import EquiparacionAnalyzer
        
        print("ANÁLISIS DE EQUIPARACIÓN AL NUEVO PLAN DE ESTUDIOS")
        print("=" * self.ancho_menu)
        print("Esta opción analiza los expedientes existentes para determinar")
        print("la equiparación de cursos al nuevo plan de estudios.")
        print()
        
        # Verificar archivos Excel existentes
        import os
        from pathlib import Path
        
        directorio_salida = Path('./salida')
        if not directorio_salida.exists():
            cprint("No se encontraron archivos Excel para analizar.", 'white', 'on_red', attrs=['bold'])
            print("Primero debe generar los expedientes usando la opción 1 o 4.")
            ConsoleUtils.pausar()
            return
        
        archivos_excel = list(directorio_salida.glob('*.xlsx'))
        # Filtrar archivos de prueba
        archivos_excel = [f for f in archivos_excel if not f.name.startswith('TEST-')]
        
        if not archivos_excel:
            cprint("No se encontraron archivos Excel válidos para analizar.", 'white', 'on_red', attrs=['bold'])
            print("Primero debe generar los expedientes usando la opción 1 o 4.")
            ConsoleUtils.pausar()
            return
        
        print(f"Se encontraron {len(archivos_excel)} expedientes para analizar.")
        
        respuesta = ConsoleUtils.leer_texto("¿Desea continuar con el análisis? (s/n): ").lower()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            return
        
        print()
        print("Analizando expedientes para equiparación...")
        print("=" * self.ancho_menu)
        
        analyzer = EquiparacionAnalyzer()
        exitosos = 0
        errores = 0
        
        for i, archivo_excel in enumerate(archivos_excel, 1):
            try:
                # Procesar archivo para equiparación
                resultado = analyzer.analizar_expediente(str(archivo_excel))
                
                if resultado:
                    # Extraer nombre del estudiante del archivo
                    nombre_archivo = archivo_excel.stem
                    partes = nombre_archivo.split('-', 1)
                    carne = partes[0] if len(partes) > 0 else "N/A"
                    nombre = partes[1] if len(partes) > 1 else "N/A"
                    
                    print(f"[{i:3d}/{len(archivos_excel)}] ✓ {carne} - {nombre[:30]}")
                    exitosos += 1
                else:
                    print(f"[{i:3d}/{len(archivos_excel)}] ⚠️ {archivo_excel.name} - Sin análisis")
                    
            except Exception as e:
                print(f"[{i:3d}/{len(archivos_excel)}] ✗ Error en {archivo_excel.name}: {str(e)}")
                errores += 1
        
        print()
        print("=" * self.ancho_menu)
        cprint(f"Análisis completado: {exitosos} exitosos, {errores} errores", 'green', attrs=['bold'])
        
        if exitosos > 0:
            print("Se ha agregado la hoja 'Equiparación' a los archivos Excel.")
            print("Esta hoja contiene:")
            print("  • Análisis de cursos para el nuevo plan")
            print("  • Convalidaciones de química general e intensiva")
            print("  • Verificación de curso de precálculo")
            print("  • Recomendaciones de equiparación")
        
        ConsoleUtils.pausar()
