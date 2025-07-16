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
                'Digite la opción del menú:', 0, 3
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
