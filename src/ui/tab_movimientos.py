"""
Módulo encargado de la interfaz gráfica para la pestaña de Movimientos.
Permite visualizar el registro histórico de las operaciones del sistema.
"""

import customtkinter as ctk
from src.utils.logger import leer_movimientos


class TabMovimientos(ctk.CTkFrame):
    """
    Clase que representa la pestaña de Movimientos en la aplicación.
    Muestra un registro de texto (log) con todas las acciones realizadas.
    Hereda de ctk.CTkFrame.
    """

    def __init__(self, master, app):
        """
        Inicializa la vista de la pestaña de movimientos.

        Args:
            master: El widget padre (contenedor de pestañas).
            app: La instancia principal de la aplicación para comunicarse con otras vistas.
        """
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Configura e inicializa los componentes visuales de la pestaña,
        incluyendo el cuadro de texto para el registro y el botón de actualización.
        
        Returns:
            None
        """
        self.textbox_movimientos = ctk.CTkTextbox(self, height=250)
        self.textbox_movimientos.pack(pady=20, fill="both", expand=True)
        
        ctk.CTkButton(self, text="Refrescar Historial", command=self.actualizar_movimientos).pack(pady=10)
        
        self.actualizar_movimientos()

    def actualizar_movimientos(self) -> None:
        """
        Limpia el cuadro de texto y vuelve a cargar el historial completo
        de movimientos consultando al registro de logs del sistema.

        Returns:
            None
        """
        self.textbox_movimientos.delete("1.0", "end")
        self.textbox_movimientos.insert("end", leer_movimientos())
        