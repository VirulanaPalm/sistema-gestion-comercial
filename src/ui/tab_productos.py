"""
Módulo encargado de la interfaz gráfica para la pestaña de Productos.
Permite gestionar el inventario (alta, baja, modificación y búsqueda)
y visualizar el stock actualizado mediante una tabla interactiva.
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from src.logica.gestion_productos import (
    listar_productos,
    agregar_producto,
    eliminar_producto,
    modificar_producto,
    buscar_productos,
)


class TabProductos(ctk.CTkFrame):
    """
    Clase que representa la pestaña de Gestión de Productos en la aplicación.
    Proporciona los formularios y la tabla para realizar operaciones CRUD
    sobre el inventario.
    Hereda de ctk.CTkFrame.
    """

    def __init__(self, master, app):
        """
        Inicializa la vista de la pestaña de productos.

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
        incluyendo los formularios de entrada, los botones de acción y la
        tabla de datos.

        Returns:
            None
        """
        frame_add = ctk.CTkFrame(self)
        frame_add.pack(pady=5, fill="x")

        self.entry_nombre = ctk.CTkEntry(
            frame_add, placeholder_text="Nombre", width=150
        )
        self.entry_nombre.pack(side="left", padx=5)

        self.entry_precio = ctk.CTkEntry(
            frame_add, placeholder_text="Precio", width=90)
        self.entry_precio.pack(side="left", padx=5)

        self.entry_stock = ctk.CTkEntry(
            frame_add, placeholder_text="Stock", width=90)
        self.entry_stock.pack(side="left", padx=5)

        btn_agregar = ctk.CTkButton(
            frame_add, text="Agregar", command=self.evento_agregar_producto, width=100
        )
        btn_agregar.pack(side="left", padx=10)

        frame_edit = ctk.CTkFrame(self)
        frame_edit.pack(pady=5, fill="x")

        self.entry_id_edit = ctk.CTkEntry(
            frame_edit, placeholder_text="ID a Editar", width=80
        )
        self.entry_id_edit.pack(side="left", padx=5)

        self.entry_nombre_edit = ctk.CTkEntry(
            frame_edit, placeholder_text="Nuevo Nombre", width=150
        )
        self.entry_nombre_edit.pack(side="left", padx=5)

        self.entry_precio_edit = ctk.CTkEntry(
            frame_edit, placeholder_text="Nuevo Precio", width=90
        )
        self.entry_precio_edit.pack(side="left", padx=5)

        self.entry_stock_edit = ctk.CTkEntry(
            frame_edit, placeholder_text="Nuevo Stock", width=90
        )
        self.entry_stock_edit.pack(side="left", padx=5)

        btn_editar = ctk.CTkButton(
            frame_edit,
            text="Modificar",
            fg_color="#F57C00",
            hover_color="#E65100",
            command=self.evento_modificar_producto,
            width=100,
        )
        btn_editar.pack(side="left", padx=10)

        frame_delete = ctk.CTkFrame(self)
        frame_delete.pack(pady=5, fill="x")

        self.entry_id_eliminar = ctk.CTkEntry(
            frame_delete, placeholder_text="ID a Eliminar", width=110
        )
        self.entry_id_eliminar.pack(side="left", padx=5)

        btn_eliminar = ctk.CTkButton(
            frame_delete,
            text="Eliminar",
            fg_color="#D32F2F",
            hover_color="#9A0007",
            command=self.evento_eliminar_producto,
            width=100,
        )
        btn_eliminar.pack(side="left", padx=10)

        frame_search = ctk.CTkFrame(self)
        frame_search.pack(pady=10, fill="x")

        self.entry_buscar = ctk.CTkEntry(
            frame_search, placeholder_text="Buscar por nombre o ID...", width=200
        )
        self.entry_buscar.pack(side="left", padx=5)

        btn_buscar = ctk.CTkButton(
            frame_search, text="Buscar", command=self.evento_buscar_producto, width=90
        )
        btn_buscar.pack(side="left", padx=5)

        btn_ver_todos = ctk.CTkButton(
            frame_search,
            text="Ver Todos",
            fg_color="gray",
            hover_color="darkgray",
            command=self.evento_limpiar_busqueda,
            width=90,
        )
        btn_ver_todos.pack(side="left", padx=5)

        self.lbl_alerta_stock = ctk.CTkLabel(
            self, text="Verificando stock...", font=("Arial", 12, "bold")
        )
        self.lbl_alerta_stock.pack(pady=2)

        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.pack(pady=5, fill="both", expand=True)

        scroll_y = ctk.CTkScrollbar(frame_tabla, orientation="vertical")
        scroll_y.pack(side="right", fill="y")

        self.tree_productos = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Producto", "Precio", "Stock"),
            show="headings",
            yscrollcommand=scroll_y.set,
        )
        self.tree_productos.pack(side="left", fill="both", expand=True)
        scroll_y.configure(command=self.tree_productos.yview)

        self.tree_productos.heading("ID", text="ID")
        self.tree_productos.heading("Producto", text="Producto")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Stock", text="Stock")

        self.tree_productos.column("ID", width=50, anchor="center")
        self.tree_productos.column("Producto", width=300, anchor="w")
        self.tree_productos.column("Precio", width=100, anchor="center")
        self.tree_productos.column("Stock", width=100, anchor="center")

        self.actualizar_lista_productos()

    def evento_agregar_producto(self) -> None:
        """
        Captura los datos del formulario de alta y solicita a la capa lógica
        la creación de un nuevo producto. Actualiza la vista si es exitoso.

        Returns:
            None
        """
        nombre = self.entry_nombre.get()
        try:
            precio = float(self.entry_precio.get())
            stock = int(self.entry_stock.get())
            if nombre:
                agregar_producto(nombre, precio, stock)
                self.app.actualizar_todo()
                self.entry_nombre.delete(0, "end")
                self.entry_precio.delete(0, "end")
                self.entry_stock.delete(0, "end")
            else:
                messagebox.showerror(
                    "Error", "El nombre no puede estar vacío.")
        except ValueError:
            messagebox.showerror(
                "Error", "Precio y stock deben ser numéricos.")

    def evento_modificar_producto(self) -> None:
        """
        Captura los datos del formulario de edición y solicita a la capa lógica
        la actualización de los atributos de un producto existente.

        Returns:
            None
        """
        try:
            id_str = self.entry_id_edit.get().strip()
            if not id_str:
                return
            id_prod = int(id_str)

            n_nom = self.entry_nombre_edit.get().strip() or None
            n_pre_str = self.entry_precio_edit.get().strip()
            n_sto_str = self.entry_stock_edit.get().strip()

            n_pre = float(n_pre_str) if n_pre_str else None
            n_sto = int(n_sto_str) if n_sto_str else None

            if n_nom is None and n_pre is None and n_sto is None:
                return

            if modificar_producto(id_prod, n_nom, n_pre, n_sto):
                self.app.actualizar_todo()
            else:
                messagebox.showerror("Error", "No se encontró ID.")
        except ValueError:
            messagebox.showerror("Error", "Valores numéricos inválidos.")

    def evento_eliminar_producto(self) -> None:
        """
        Captura el ID ingresado y solicita a la capa lógica la eliminación
        del producto correspondiente, previa confirmación del usuario.

        Returns:
            None
        """
        try:
            id_prod = int(self.entry_id_eliminar.get())
            if messagebox.askyesno("Confirmar", f"¿Eliminar ID {id_prod}?"):
                if eliminar_producto(id_prod):
                    self.app.actualizar_todo()
                else:
                    messagebox.showerror("Error", "No se encontró ID.")
        except ValueError:
            messagebox.showerror("Error", "Ingresá un ID numérico.")

    def evento_buscar_producto(self) -> None:
        """
        Captura el término de búsqueda ingresado y filtra la tabla de productos
        según las coincidencias devueltas por la capa lógica.

        Returns:
            None
        """
        resultados = buscar_productos(self.entry_buscar.get())
        self.actualizar_lista_productos(resultados)

    def evento_limpiar_busqueda(self) -> None:
        """
        Limpia el campo de texto de búsqueda y restaura la tabla
        para mostrar todos los productos del inventario.

        Returns:
            None
        """
        self.entry_buscar.delete(0, "end")
        self.actualizar_lista_productos()

    def actualizar_lista_productos(self, productos_a_mostrar: list = None) -> None:
        """
        Refresca el contenido del Treeview (tabla) con los productos actuales.
        Además, actualiza la alerta visual si existen artículos con
        stock crítico.

        Args:
            productos_a_mostrar (list, optional): Lista filtrada de productos a
                                                  visualizar. Si es None, se
                                                  muestran todos.

        Returns:
            None
        """
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)

        todos_los_productos = listar_productos()
        if productos_a_mostrar is not None:
            productos = productos_a_mostrar
        else:
            productos = todos_los_productos

        for p in productos:
            self.tree_productos.insert(
                "",
                "end",
                values=(p["id"], p["nombre"],
                        f"${p['precio']:.2f}", p["stock"]),
            )

        criticos = [p for p in todos_los_productos if p["stock"] < 5]
        if criticos:
            nombres = " - ".join([f"{p['nombre']} ({p['stock']})" for p in criticos])
            self.lbl_alerta_stock.configure(
                text=f"STOCK CRÍTICO (< 5 unidades): {nombres}", text_color="#F44336"
            )
        else:
            self.lbl_alerta_stock.configure(
                text="Stock saludable (> 5 unidades)", text_color="#4CAF50"
            )
