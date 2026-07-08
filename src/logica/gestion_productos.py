"""
Módulo para la gestión del inventario de productos
Permite realizar operaciones de listado, búsqueda, alta, modificación y baja.
"""

from src.utils.persistencia import cargar_datos, guardar_datos
from src.utils.logger import registrar_movimiento

RUTA_PRODUCTOS = "data/productos.json"


def listar_productos() -> list:
    """
    Obtiene la lista completa de productos disponibles en el sistema.

    Returns:
        list: Lista de diccionarios donde cada uno representa un producto.
    """
    return cargar_datos(RUTA_PRODUCTOS)


def buscar_productos(consulta: str) -> list:
    """
    Busca productos que coincidan con la consulta proporcionada.

    Args:
        consulta (str): Texto o ID numérico a buscar.

    Returns:
        list: Lista de productos que coinciden con el criterio de búsqueda.
    """
    productos = cargar_datos(RUTA_PRODUCTOS)
    consulta = str(consulta).strip().lower()

    if not consulta:
        return productos

    resultados = []
    for p in productos:

        if str(p["id"]) == consulta or consulta in p["nombre"].lower():
            resultados.append(p)

    return resultados


def agregar_producto(nombre: str, precio: float, stock: int) -> dict:
    """
    Registra un nuevo producto en el sistema.

    Args:
        nombre (str): Nombre del producto.
        precio (float): Precio unitario. Debe ser mayor a 0.
        stock (int): Cantidad inicial. Debe ser mayor o igual a 0.

    Returns:
        dict: El nuevo producto creado con su ID asignado.

    Raises:
        ValueError: Si el precio o stock son negativos.
    """
    if precio <= 0 or stock < 0:
        raise ValueError("Precio y stock deben ser valores positivos.")

    productos = cargar_datos(RUTA_PRODUCTOS)

    nuevo_id = max([producto["id"] for producto in productos], default=0) + 1

    nuevo_producto = {
        "id": nuevo_id,
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
    }

    productos.append(nuevo_producto)
    guardar_datos(RUTA_PRODUCTOS, productos)

    registrar_movimiento(
        f"ALTA: Se agregó el producto '{nombre}' "
        f"(ID: {nuevo_id}) con {stock} unidades."
    )

    return nuevo_producto


def buscar_producto_por_id(id_producto: int) -> dict:
    """
    Busca un producto por su ID único.

    Args:
        id_producto (int): ID del producto buscado.

    Returns:
        dict: Diccionario del producto si existe, de lo contrario None.
    """
    productos = cargar_datos(RUTA_PRODUCTOS)
    for producto in productos:
        if producto["id"] == id_producto:
            return producto
    return None


def modificar_stock(id_producto: int, nueva_cantidad: int) -> bool:
    """
    Actualiza la cantidad de stock de un producto existente.

    Args:
        id_producto (int): ID del producto a modificar.
        nueva_cantidad (int): Nueva cantidad de stock.

    Returns:
        bool: True si la operación fue exitosa, False si no se encontró.
    """
    productos = cargar_datos(RUTA_PRODUCTOS)
    for producto in productos:
        if producto["id"] == id_producto:
            producto["stock"] = nueva_cantidad
            guardar_datos(RUTA_PRODUCTOS, productos)
            return True
    return False


def modificar_producto(
    id_producto: int,
    nuevo_nombre: str = None,
    nuevo_precio: float = None,
    nuevo_stock: int = None,
) -> bool:
    """
    Modifica atributos de un producto. Si es None, se conserva el anterior.

    Args:
        id_producto (int): ID del producto a modificar.
        nuevo_nombre (str, optional): Nuevo nombre del producto.
        nuevo_precio (float, optional): Nuevo precio. Debe ser mayor a 0.
        nuevo_stock (int, optional): Nuevo stock. Debe ser >= 0.

    Returns:
        bool: True si la modificación fue exitosa, False si no existe el ID.
    """

    precio_invalido = nuevo_precio is not None and nuevo_precio <= 0
    stock_invalido = nuevo_stock is not None and nuevo_stock < 0

    if precio_invalido or stock_invalido:
        raise ValueError("Valores de precio o stock no válidos.")

    productos = cargar_datos(RUTA_PRODUCTOS)
    for producto in productos:
        if producto["id"] == id_producto:
            nombre_viejo = producto["nombre"]
            precio_viejo = producto["precio"]
            stock_viejo = producto["stock"]

            if nuevo_nombre:
                producto["nombre"] = nuevo_nombre
            if nuevo_precio is not None:
                producto["precio"] = nuevo_precio
            if nuevo_stock is not None:
                producto["stock"] = nuevo_stock

            guardar_datos(RUTA_PRODUCTOS, productos)

            registrar_movimiento(
                f"MODIFICACIÓN: Producto ID {id_producto}. "
                f"Antes '{nombre_viejo}' (${precio_viejo} | {stock_viejo} un.). "
                f"Ahora '{producto['nombre']}' (${producto['precio']} | "
                f"{producto['stock']} un.)."
            )
            return True
    return False


def eliminar_producto(id_producto: int) -> bool:
    """
    Elimina un producto del sistema mediante su ID.

    Args:
        id_producto (int): ID del producto a dar de baja.

    Returns:
        bool: True si se eliminó el producto, False si no se encontró.
    """
    productos = cargar_datos(RUTA_PRODUCTOS)

    producto_a_borrar = next(
        (p for p in productos if p["id"] == id_producto), None)

    if producto_a_borrar:
        productos_filtrados = [p for p in productos if p["id"] != id_producto]
        guardar_datos(RUTA_PRODUCTOS, productos_filtrados)

        # Se formatea el string largo
        registrar_movimiento(
            f"BAJA: Se eliminó el producto '{producto_a_borrar['nombre']}' "
            f"(ID: {id_producto})."
        )
        return True

    return False
