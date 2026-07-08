"""
Módulo principal de ejecución
Actúa como el punto de entrada de la aplicación de Gestión Comercial
Se encarga de importar, inicializar y arrancar el bucle principal de la interfaz gráfica
"""

from src.ui.ventana_principal import AppComercial


def main() -> None:
    """
    Punto de entrada principal de la aplicación.
    Instancia la clase AppComercial y ejecuta su bucle principal de eventos

    Returns:
        None
    """
    app = AppComercial()
    app.mainloop()


if __name__ == "__main__":
    main()
