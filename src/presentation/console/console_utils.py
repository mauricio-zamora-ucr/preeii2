"""
Utilidades para la interfaz de consola
"""
import os
from typing import Optional


class ConsoleUtils:
    """
    Utilidades para manejar la interfaz de consola.
    """

    @staticmethod
    def limpiar_pantalla() -> None:
        """Limpia la pantalla de la consola según el sistema operativo."""
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # macOS y Linux
            os.system('clear')

    @staticmethod
    def leer_numero_entero(etiqueta: Optional[str] = None) -> int:
        """
        Lee un número entero desde la entrada estándar con validación.
        
        Args:
            etiqueta: Texto a mostrar como prompt
        
        Returns:
            Número entero válido ingresado por el usuario
        """
        if etiqueta:
            print(etiqueta)
        
        while True:
            try:
                numero = input()
                return int(numero)
            except (ValueError, TypeError):
                print('El valor no es entero, por favor reintente: ')

    @staticmethod
    def leer_rango_numeros_enteros(
        etiqueta: Optional[str] = None, 
        rango_inferior: int = 0, 
        rango_superior: int = 99999999
    ) -> int:
        """
        Lee un número entero dentro de un rango específico.
        
        Args:
            etiqueta: Texto a mostrar como prompt
            rango_inferior: Límite inferior del rango (inclusive)
            rango_superior: Límite superior del rango (inclusive)
        
        Returns:
            Número entero válido dentro del rango especificado
        """
        while True:
            numero = ConsoleUtils.leer_numero_entero(etiqueta)
            
            if rango_inferior <= numero <= rango_superior:
                return numero
            else:
                print(f'Debe digitar un número entre {rango_inferior} y {rango_superior}')

    @staticmethod
    def leer_texto(etiqueta: Optional[str] = None, requerido: bool = True) -> str:
        """
        Lee texto desde la entrada estándar.
        
        Args:
            etiqueta: Texto a mostrar como prompt
            requerido: Si es True, no permite texto vacío
        
        Returns:
            Texto ingresado por el usuario
        """
        if etiqueta:
            print(etiqueta)
        
        while True:
            texto = input().strip()
            
            if not requerido or texto:
                return texto
            else:
                print('Este campo es requerido, por favor ingrese un valor: ')

    @staticmethod
    def confirmar(mensaje: str, por_defecto: bool = False) -> bool:
        """
        Solicita confirmación al usuario.
        
        Args:
            mensaje: Mensaje a mostrar
            por_defecto: Valor por defecto si el usuario solo presiona Enter
        
        Returns:
            True si el usuario confirma, False en caso contrario
        """
        sufijo = " [S/n]: " if por_defecto else " [s/N]: "
        
        while True:
            respuesta = input(mensaje + sufijo).strip().lower()
            
            if not respuesta:
                return por_defecto
            elif respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                return True
            elif respuesta in ['n', 'no']:
                return False
            else:
                print("Por favor responda 's' para sí o 'n' para no.")

    @staticmethod
    def pausar(mensaje: str = "Presione Enter para continuar...") -> None:
        """
        Pausa la ejecución hasta que el usuario presione Enter.
        
        Args:
            mensaje: Mensaje a mostrar
        """
        input(mensaje)
