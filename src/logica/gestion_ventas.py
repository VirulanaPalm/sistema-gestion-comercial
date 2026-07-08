"""
Módulo encargado del registro de ventas y la generación de métricas
y auditoría. Interactúa directamente con el estado de la caja y el
stock de productos.
"""

import pandas as pd
from datetime import datetime
from src.utils.persistencia import cargar_datos, guardar_datos
from src.logica.gestion_productos import (
    buscar_producto_por_id, 
    modificar_stock
)
from src.utils.logger import registrar_movimiento
from src.logica.gestion_caja import obtener_estado_caja

RUTA_VENTAS = 'data/ventas.json'


def registrar_ticket(carrito: list) -> dict:
    """
    Procesa una compra consolidando los artículos en un ticket único.
    Verifica el stock disponible y el estado de la caja antes de procesar.

    Args:
        carrito (list): Lista de diccionarios con los items a comprar.

    Returns:
        dict: El diccionario representando el ticket generado.

    Raises:
        PermissionError: Si la caja registradora está cerrada.
        ValueError: Si el carrito está vacío o no hay stock
            suficiente para algún producto.
    """
    caja = obtener_estado_caja()
    if caja["estado"] == "cerrada":
        raise PermissionError(
            "La caja está cerrada. Debes abrirla antes de vender."
        )

    if not carrito:
        raise ValueError("El carrito está vacío.")

    for item in carrito:
        producto = buscar_producto_por_id(item["id_producto"])
        if not producto:
            raise ValueError(
                f"El producto ID {item['id_producto']} ya no existe."
            )
        if producto["stock"] < item["cantidad"]:
            raise ValueError(
                f"Stock insuficiente para '{producto['nombre']}'. "
                f"Quedan {producto['stock']} un."
            )

    for item in carrito:
        producto = buscar_producto_por_id(item["id_producto"])
        nuevo_stock = producto["stock"] - item["cantidad"]
        modificar_stock(item["id_producto"], nuevo_stock)

    ventas = cargar_datos(RUTA_VENTAS)
    id_ticket = len(ventas) + 1 if ventas else 1
    total_ticket = sum(item["subtotal"] for item in carrito)
    
    nuevo_ticket = {
        "id_ticket": id_ticket,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ciclo_id": caja["ciclo_actual"],
        "items": carrito,
        "total_ticket": total_ticket
    }
    
    ventas.append(nuevo_ticket)
    guardar_datos(RUTA_VENTAS, ventas)
    
    resumen_items = ", ".join(
        [f"{i['cantidad']}x {i['nombre_producto']}" for i in carrito]
    )
    
    registrar_movimiento(
        f"VENTA TICKET #{id_ticket}: [{resumen_items}]. "
        f"Total: ${total_ticket} (Ciclo {caja['ciclo_actual']})"
    )
    
    return nuevo_ticket


def mostrar_estadisticas() -> dict:
    """
    Calcula los indicadores globales históricos procesando los
    tickets registrados utilizando Pandas.

    Returns:
        dict: Diccionario con las métricas clave (Total de Ingresos,
              Tickets Emitidos, Unidades Vendidas y Producto más 
              vendido histórico).
    """
    ventas = cargar_datos(RUTA_VENTAS)
    if not ventas:
        return {"mensaje": "Aún no hay ventas registradas."}
        
    df_tickets = pd.DataFrame(ventas)
    
    items_planos = []
    for ticket in ventas:
        for item in ticket["items"]:
            items_planos.append(item)
    df_items = pd.DataFrame(items_planos)
    
    total_ingresos = df_tickets['total_ticket'].sum()
    total_unidades = df_items['cantidad'].sum()
    ventas_agrupadas = df_items.groupby('nombre_producto')['cantidad'].sum()
    producto_top = ventas_agrupadas.idxmax()
    amount_top = ventas_agrupadas.max()
    
    return {
        "Total de Ingresos": f"${total_ingresos:.2f}",
        "Tickets Emitidos": str(len(ventas)),
        "Unidades Vendidas": str(int(total_unidades)),
        "Producto más vendido histórico": (
            f"{producto_top} ({amount_top} un.)"
        )
    }


def obtener_ventas_agrupadas_por_ciclo() -> dict:
    """
    Agrupa todo el historial de ventas separándolo por ciclo (turno)
    de caja. Ideal para estructuras de vista jerárquica como Treeview.

    Returns:
        dict: Diccionario donde las claves son los ID de ciclo (turnos)
              y los valores son listas de tickets pertenecientes a ese
              ciclo.
    """
    ventas = cargar_datos(RUTA_VENTAS)
    ciclos = {}
    for v in ventas:
        c_id = v.get("ciclo_id", 1)
        if c_id not in ciclos:
            ciclos[c_id] = []
        ciclos[c_id].append(v)
    return ciclos


def buscar_ticket_por_id(id_ticket: int) -> dict:
    """
    Busca y devuelve el detalle completo de un ticket específico
    mediante su ID.

    Args:
        id_ticket (int): Número de identificación del ticket a buscar.

    Returns:
        dict: Estructura de datos del ticket si existe, sino None.
    """
    ventas = cargar_datos(RUTA_VENTAS)
    for ticket in ventas:
        if ticket["id_ticket"] == id_ticket:
            return ticket
    return None