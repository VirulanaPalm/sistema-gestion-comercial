"""
Módulo encargado de la interfaz gráfica para la pestaña de Auditoría de Caja
(Estadísticas). Permite visualizar un resumen de indicadores globales y un
historial interactivo de las ventas agrupadas por turno de caja.
"""

import customtkinter as ctk
from tkinter import ttk
from src.logica.gestion_ventas import (
    mostrar_estadisticas,
    obtener_ventas_agrupadas_por_ciclo,
    buscar_ticket_por_id
)


class TabEstadisticas(ctk.CTkFrame):
    """
    Clase que representa la pestaña de Auditoría de Caja en la aplicación.
    Hereda de ctk.CTkFrame.
    """

    def __init__(self, master, app):
        """
        Inicializa la vista de la pestaña de estadísticas.

        Args:
            master: El widget padre (contenedor de pestañas).
            app: La instancia principal de la aplicación para comunicarse
                 con otras vistas.
        """
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Configura e inicializa todos los componentes visuales de la pestaña,
        como etiquetas, botones y tablas (Treeview) para indicadores y ciclos.
        """
        lbl_g = ctk.CTkLabel(
            self, 
            text="Resumen de Ventas", 
            font=("Arial", 14, "bold")
        )
        lbl_g.pack(pady=(10, 2), anchor="w", padx=20)

        self.tree_globales = ttk.Treeview(
            self, 
            columns=("Indicador", "Valor"), 
            show="headings", 
            height=4
        )
        self.tree_globales.pack(padx=20, pady=5, fill="x")
        
        self.tree_globales.heading("Indicador", text="Métrica / Indicador")
        self.tree_globales.heading("Valor", text="Valor")
        self.tree_globales.column("Indicador", width=350, anchor="w")
        self.tree_globales.column("Valor", width=250, anchor="center")

        lbl_c = ctk.CTkLabel(
            self, 
            text="Auditoría por Turnos (Doble clic para ver Ticket)", 
            font=("Arial", 14, "bold")
        )
        lbl_c.pack(pady=(15, 2), anchor="w", padx=20)

        frame_ciclos = ctk.CTkFrame(self)
        frame_ciclos.pack(padx=20, pady=5, fill="both", expand=True)

        scroll_y = ctk.CTkScrollbar(frame_ciclos, orientation="vertical")
        scroll_y.pack(side="right", fill="y")

        self.tree_ciclos = ttk.Treeview(
            frame_ciclos, 
            columns=("Total", "Detalle"), 
            show="tree headings", 
            yscrollcommand=scroll_y.set
        )
        self.tree_ciclos.pack(side="left", fill="both", expand=True)
        scroll_y.configure(command=self.tree_ciclos.yview)

        self.tree_ciclos.heading("#0", text="Turno / Venta")
        self.tree_ciclos.heading("Total", text="Total Abonado")
        self.tree_ciclos.heading("Detalle", text="Fecha / Detalles")

        self.tree_ciclos.column("#0", width=250, anchor="w")
        self.tree_ciclos.column("Total", width=100, anchor="center")
        self.tree_ciclos.column("Detalle", width=200, anchor="w")

        self.tree_ciclos.bind("<Double-1>", self.evento_doble_click_ticket)
        
        btn_refrescar = ctk.CTkButton(
            self, 
            text="Refrescar Auditoría", 
            command=self.actualizar_estadisticas
        )
        btn_refrescar.pack(pady=10)
        
        self.actualizar_estadisticas()

    def actualizar_estadisticas(self) -> None:
        """
        Limpia y vuelve a cargar los datos de las tablas de métricas globales
        y del historial de turnos consultando a la capa lógica.
        """
        for item in self.tree_globales.get_children():
            self.tree_globales.delete(item)
        for item in self.tree_ciclos.get_children():
            self.tree_ciclos.delete(item)

        estadisticas = mostrar_estadisticas()
        if "mensaje" in estadisticas:
            self.tree_globales.insert(
                "", 
                "end", 
                values=("Estado", estadisticas["mensaje"])
            )
        else:
            for clave, valor in estadisticas.items():
                self.tree_globales.insert(
                    "", 
                    "end", 
                    values=(clave, valor)
                )

        ventas_por_ciclo = obtener_ventas_agrupadas_por_ciclo()
        for ciclo_id in sorted(ventas_por_ciclo.keys(), reverse=True):
            tickets = ventas_por_ciclo[ciclo_id]
            total_ciclo = sum(t["total_ticket"] for t in tickets)
            
            fecha_turno = tickets[0]["fecha"]
            
            padre = self.tree_ciclos.insert(
                "", 
                "end", 
                text=f"Turno Caja - {fecha_turno}", 
                values=(f"${total_ciclo:.2f}", f"{len(tickets)} ventas"), 
                open=True
            )
            
            for t in reversed(tickets):
                self.tree_ciclos.insert(
                    padre, 
                    "end", 
                    text=f"Venta #{t['id_ticket']}", 
                    values=(f"${t['total_ticket']:.2f}", t['fecha']), 
                    tags=(f"ticket_{t['id_ticket']}",)
                )

    def evento_doble_click_ticket(self, event) -> None:
        """
        Evento disparado al hacer doble clic en el Treeview de ciclos.
        Captura el ID del ticket si se seleccionó una venta y abre su detalle.
        """
        item_seleccionado = self.tree_ciclos.selection()
        if not item_seleccionado:
            return
        tags = self.tree_ciclos.item(item_seleccionado[0], "tags")
        if tags and tags[0].startswith("ticket_"):
            self.mostrar_ventana_ticket(int(tags[0].split("_")[1]))
            
    def mostrar_ventana_ticket(self, id_ticket: int) -> None:
        """
        Despliega una ventana emergente simulando la impresión de un ticket 
        físico con todos los detalles de la venta seleccionada.
        """
        ticket = buscar_ticket_por_id(id_ticket)
        if not ticket:
            return
        
        ventana_ticket = ctk.CTkToplevel(self)
        ventana_ticket.title(f"Ticket #{id_ticket}")
        ventana_ticket.geometry("380x450")
        ventana_ticket.transient(self.app) 
        ventana_ticket.grab_set() 
        
        textbox_items = ctk.CTkTextbox(ventana_ticket, font=("Courier", 12))
        textbox_items.pack(padx=20, pady=20, fill="both", expand=True)
        
        ticket_str = f"         TICKET DE VENTA #{id_ticket}\n"
        ticket_str += f" Fecha: {ticket['fecha']}\n"
        ticket_str += f" Turno: {ticket['ciclo_id']}\n"
        ticket_str += "="*37 + "\n"
        ticket_str += "CANT PRODUCTO                SUBTOTAL\n"
        ticket_str += "-"*37 + "\n"
        
        for item in ticket["items"]:
            nombre = item['nombre_producto']
            if len(nombre) > 21:
                prod_nombre = nombre[:19] + '..'
            else:
                prod_nombre = nombre.ljust(21)
                
            ticket_str += (
                f"{item['cantidad']:<4} {prod_nombre} "
                f"${item['subtotal']:.2f}\n"
            )
            
        ticket_str += "-"*37 + "\n"
        ticket_str += (
            f"TOTAL FACTURADO:             "
            f"${ticket['total_ticket']:.2f}\n"
        )
        ticket_str += "="*37 + "\n"
        ticket_str += "        ¡Gracias por su compra!      \n"
        
        textbox_items.insert("end", ticket_str)
        textbox_items.configure(state="disabled")