"""
Módulo principal de la aplicación.
Contiene la ventana base del sistema de gestión comercial, 
encargada de inicializar y coordinar las diferentes pestañas (vistas).
"""

import customtkinter as ctk
from tkinter import ttk

from src.ui.tab_productos import TabProductos
from src.ui.tab_ventas import TabVentas
from src.ui.tab_estadisticas import TabEstadisticas
from src.ui.tab_movimientos import TabMovimientos


class AppComercial(ctk.CTk):
    """
    Clase principal que representa la ventana base de la aplicación.
    Hereda de ctk.CTk y maneja la navegación entre las distintas pestañas.
    """

    def __init__(self):
        """
        Inicializa la ventana principal, configura el tema visual oscuro,
        el tamaño de la ventana y agrega las pestañas de navegación al sistema.
        """
        super().__init__()
        
        self.title("Sistema de Gestión Comercial")
        self.geometry("700x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configurar_estilo_tablas()

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        tab_p = self.tabview.add("Productos")
        tab_v = self.tabview.add("Ventas")
        tab_e = self.tabview.add("Auditoría de Caja")
        tab_m = self.tabview.add("Movimientos")

        self.vista_productos = TabProductos(tab_p, app=self)
        self.vista_productos.pack(fill="both", expand=True)

        self.vista_ventas = TabVentas(tab_v, app=self)
        self.vista_ventas.pack(fill="both", expand=True)

        self.vista_estadisticas = TabEstadisticas(tab_e, app=self)
        self.vista_estadisticas.pack(fill="both", expand=True)

        self.vista_movimientos = TabMovimientos(tab_m, app=self)
        self.vista_movimientos.pack(fill="both", expand=True)

    def configurar_estilo_tablas(self) -> None:
        """
        Configura el estilo visual para todas las tablas (Treeview) 
        utilizadas a lo largo de la aplicación para que respeten el modo oscuro.

        Returns:
            None
        """
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure(
            "Treeview", 
            background="#2b2b2b", 
            foreground="white", 
            rowheight=25, 
            fieldbackground="#2b2b2b", 
            bordercolor="#343638", 
            borderwidth=0
        )
        
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        style.configure(
            "Treeview.Heading", 
            background="#565b5e", 
            foreground="white", 
            relief="flat", 
            font=("Arial", 10, "bold")
        )
        
        style.map("Treeview.Heading", background=[('active', '#343638')])

    def actualizar_todo(self) -> None:
        """
        Función orquestadora que notifica a todas las pestañas para que 
        refresquen sus datos de manera simultánea cuando ocurre un cambio global.

        Returns:
            None
        """
        self.vista_productos.actualizar_lista_productos()
        self.vista_estadisticas.actualizar_estadisticas()
        self.vista_movimientos.actualizar_movimientos()