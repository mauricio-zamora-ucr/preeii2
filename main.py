"""
PreEII - Pre-enrollment review support software for Industrial Engineering
Main entry point of the application.

Python minimum version: 3.8
"""
from src.presentation.console.menu_controller import MenuController


def main() -> None:
    """
    Función principal de la aplicación.
    Inicializa y ejecuta el controlador del menú principal.
    """
    try:
        menu_controller = MenuController()
        menu_controller.mostrar_menu_principal()
    except KeyboardInterrupt:
        print("\n\nAplicación terminada por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        print("Por favor contacte al desarrollador si el problema persiste.")


if __name__ == "__main__":
    main()