"""
Módulo encargado de la interfaz gráfica para la pestaña de Ventas (Punto de Venta).
Permite gestionar el carrito de compras, operar la caja registradora (apertura/cierre)
y finalizar las transacciones comerciales.
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from src.logica.gestion_productos import buscar_producto_por_id
from src.logica.gestion_ventas import registrar_ticket
from src.logica.gestion_caja import abrir_caja, cerrar_caja, obtener_estado_caja


class TabVentas(ctk.CTkFrame):
    """
    Clase que representa la pestaña de Ventas en la aplicación.
    Proporciona la interfaz para agregar productos al carrito y procesar el cobro.
    Hereda de ctk.CTkFrame.
    """

    def __init__(self, master, app):
        """
        Inicializa la vista de la pestaña de ventas.

        Args:
            master: El widget padre (contenedor de pestañas).
            app: La instancia principal de la aplicación para comunicarse con otras vistas.
        """
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.carrito = []
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Configura e inicializa todos los componentes visuales de la pestaña,
        incluyendo controles de caja, ingreso de productos, tabla del carrito y totales.

        Returns:
            None
        """
        self.frame_caja = ctk.CTkFrame(self)
        self.frame_caja.pack(pady=5, padx=20, fill="x")
        
        self.lbl_estado_caja = ctk.CTkLabel(self.frame_caja, text="Estado: CALCULANDO...", font=("Arial", 16, "bold"))
        self.lbl_estado_caja.pack(pady=5)
        self.lbl_hora_caja = ctk.CTkLabel(self.frame_caja, text="")
        self.lbl_hora_caja.pack()
        
        frame_btn_caja = ctk.CTkFrame(self.frame_caja, fg_color="transparent")
        frame_btn_caja.pack(pady=5)
        ctk.CTkButton(frame_btn_caja, text="Abrir Caja", fg_color="#388E3C", command=self.evento_abrir_caja).pack(side="left", padx=5)
        ctk.CTkButton(frame_btn_caja, text="Cerrar Caja", fg_color="#D32F2F", command=self.evento_cerrar_caja).pack(side="left", padx=5)

        frame_agregar = ctk.CTkFrame(self)
        frame_agregar.pack(pady=10, padx=20, fill="x")
        
        self.entry_id_venta = ctk.CTkEntry(frame_agregar, placeholder_text="ID Producto", width=120)
        self.entry_id_venta.pack(side="left", padx=10, pady=10)
        
        self.entry_cant_venta = ctk.CTkEntry(frame_agregar, placeholder_text="Cantidad", width=120)
        self.entry_cant_venta.pack(side="left", padx=10)
        
        ctk.CTkButton(frame_agregar, text="Añadir al Carrito", command=self.evento_agregar_carrito).pack(side="left", padx=10)

        frame_tabla_carrito = ctk.CTkFrame(self)
        frame_tabla_carrito.pack(padx=20, pady=5, fill="both", expand=True)

        scroll_y_carrito = ctk.CTkScrollbar(frame_tabla_carrito, orientation="vertical")
        scroll_y_carrito.pack(side="right", fill="y")

        self.tree_carrito = ttk.Treeview(frame_tabla_carrito, columns=("Cantidad", "Producto", "Precio U.", "Subtotal"), show="headings", yscrollcommand=scroll_y_carrito.set)
        self.tree_carrito.pack(side="left", fill="both", expand=True)
        scroll_y_carrito.configure(command=self.tree_carrito.yview)

        self.tree_carrito.heading("Cantidad", text="Cant.")
        self.tree_carrito.heading("Producto", text="Producto")
        self.tree_carrito.heading("Precio U.", text="Precio U.")
        self.tree_carrito.heading("Subtotal", text="Subtotal")

        self.tree_carrito.column("Cantidad", width=60, anchor="center")
        self.tree_carrito.column("Producto", width=250, anchor="w")
        self.tree_carrito.column("Precio U.", width=100, anchor="center")
        self.tree_carrito.column("Subtotal", width=100, anchor="center")

        frame_inferior = ctk.CTkFrame(self, fg_color="transparent")
        frame_inferior.pack(pady=10, padx=20, fill="x")
        
        self.lbl_total_carrito = ctk.CTkLabel(frame_inferior, text="Total: $0.00", font=("Arial", 20, "bold"), text_color="#F57C00")
        self.lbl_total_carrito.pack(side="left", padx=20)
        
        ctk.CTkButton(frame_inferior, text="Vaciar", fg_color="gray", width=80, command=self.evento_vaciar_carrito).pack(side="right", padx=5)
        ctk.CTkButton(frame_inferior, text="Finalizar Compra", fg_color="#F57C00", hover_color="#E65100", command=self.evento_finalizar_compra).pack(side="right", padx=10)

        self.actualizar_visor_carrito()
        self.actualizar_ui_caja()

    def actualizar_ui_caja(self) -> None:
        """
        Consulta el estado lógico de la caja y actualiza las etiquetas visuales
        mostrando si está abierta o cerrada, junto con el horario y el turno.

        Returns:
            None
        """
        caja = obtener_estado_caja()
        if caja["estado"] == "abierta":
            self.lbl_estado_caja.configure(text=f"Estado: ABIERTA (Ciclo {caja['ciclo_actual']})", text_color="#4CAF50")
            self.lbl_hora_caja.configure(text=f"Abierta desde: {caja['hora_apertura']}")
        else:
            self.lbl_estado_caja.configure(text="Estado: CERRADA", text_color="#F44336")
            self.lbl_hora_caja.configure(text=f"Cerrada desde: {caja['hora_cierre']}" if caja['hora_cierre'] else "")

    def evento_abrir_caja(self) -> None:
        """
        Captura el evento del botón de abrir caja. Solicita la apertura a la capa lógica
        y notifica a la aplicación para que se refresque la interfaz.

        Returns:
            None
        """
        if abrir_caja():
            self.actualizar_ui_caja()
            self.app.actualizar_todo()

    def evento_cerrar_caja(self) -> None:
        """
        Captura el evento del botón de cerrar caja. Solicita el cierre a la capa lógica
        y notifica a la aplicación para que se refresque la interfaz.

        Returns:
            None
        """
        if cerrar_caja():
            self.actualizar_ui_caja()
            self.app.actualizar_todo()

    def evento_agregar_carrito(self) -> None:
        """
        Captura y valida los datos de entrada para agregar un producto al carrito.
        Comprueba la existencia del producto y valida que el stock sea suficiente
        considerando lo que ya está añadido previamente.

        Returns:
            None
        """
        try:
            id_prod = int(self.entry_id_venta.get())
            cantidad = int(self.entry_cant_venta.get())
            if cantidad <= 0:
                return messagebox.showerror("Error", "Cantidad debe ser mayor a 0.")
                
            producto = buscar_producto_por_id(id_prod)
            if not producto:
                return messagebox.showerror("Error", "Producto no encontrado.")
            
            cant_en_carrito = sum(item["cantidad"] for item in self.carrito if item["id_producto"] == id_prod)
            
            if producto["stock"] < (cantidad + cant_en_carrito):
                return messagebox.showerror("Error", f"Stock insuficiente.")
            
            subtotal = producto["precio"] * cantidad
            item_existente = next((i for i in self.carrito if i["id_producto"] == id_prod), None)
            
            if item_existente:
                item_existente["cantidad"] += cantidad
                item_existente["subtotal"] += subtotal
            else:
                self.carrito.append({
                    "id_producto": id_prod,
                    "nombre_producto": producto["nombre"],
                    "precio_unitario": producto["precio"],
                    "cantidad": cantidad,
                    "subtotal": subtotal
                })
                
            self.actualizar_visor_carrito()
            self.entry_id_venta.delete(0, 'end')
            self.entry_cant_venta.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Ingresá números válidos.")

    def actualizar_visor_carrito(self) -> None:
        """
        Limpia la tabla del carrito y la vuelve a cargar con los items actuales,
        calculando y actualizando dinámicamente el precio total de la compra.

        Returns:
            None
        """
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
            
        total = 0
        for i in self.carrito:
            self.tree_carrito.insert("", "end", values=(i['cantidad'], i['nombre_producto'], f"${i['precio_unitario']:.2f}", f"${i['subtotal']:.2f}"))
            total += i["subtotal"]
        
        self.lbl_total_carrito.configure(text=f"Total: ${total:.2f}")

    def evento_vaciar_carrito(self) -> None:
        """
        Vacía la lista temporal de productos del carrito y refresca la tabla visual.

        Returns:
            None
        """
        self.carrito = []
        self.actualizar_visor_carrito()

    def evento_finalizar_compra(self) -> None:
        """
        Intenta procesar y registrar el ticket con los artículos actuales del carrito.
        Maneja errores si la caja está cerrada y notifica a todo el sistema del cambio.

        Returns:
            None
        """
        if not self.carrito:
            return messagebox.showwarning("Aviso", "El carrito está vacío.")
            
        try:
            ticket = registrar_ticket(self.carrito)
            messagebox.showinfo("Éxito", f"Compra finalizada.\nTicket #{ticket['id_ticket']} por ${ticket['total_ticket']}")
            self.evento_vaciar_carrito()
            self.app.actualizar_todo() # Notificamos a toda la aplicación
            
        except PermissionError as e:
            messagebox.showerror("Caja Cerrada", str(e))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            