"""
Módulo para la gestión del estado de la caja registradora.
Permite obtener, guardar, abrir y cerrar la caja, llevando un registro del turno o ciclo actual.
"""

import json
import os
from datetime import datetime
from src.utils.logger import registrar_movimiento

RUTA_CAJA = 'data/caja.json'


def obtener_estado_caja() -> dict:
    """
    Devuelve el estado actual de la caja. Si el archivo no existe,
    lo crea con el ciclo inicial en 0.

    Returns:
        dict: Diccionario con el estado de la caja, hora de apertura, hora de cierre y ciclo_actual.
    """
    if not os.path.exists(RUTA_CAJA):
        estado_inicial = {"estado": "cerrada", "hora_apertura": None, "hora_cierre": None, "ciclo_actual": 0}
        _guardar_estado(estado_inicial)
        return estado_inicial
        
    try:
        with open(RUTA_CAJA, 'r', encoding='utf-8') as f:
            estado = json.load(f)
            # Compatibilidad si ya tenías un archivo viejo sin 'ciclo_actual'
            if "ciclo_actual" not in estado:
                estado["ciclo_actual"] = 0
            return estado
    except (json.JSONDecodeError, IOError):
        return {"estado": "cerrada", "hora_apertura": None, "hora_cierre": None, "ciclo_actual": 0}


def _guardar_estado(estado: dict) -> None:
    """
    Guarda el estado de la caja en el archivo JSON correspondiente.

    Args:
        estado (dict): Diccionario que contiene la información actualizada de la caja.

    Returns:
        None
    """
    with open(RUTA_CAJA, 'w', encoding='utf-8') as f:
        json.dump(estado, f, indent=4, ensure_ascii=False)


def abrir_caja() -> bool:
    """
    Abre la caja registradora, iniciando un nuevo ciclo o turno.

    Returns:
        bool: True si la caja se abrió exitosamente, False si ya se encontraba abierta.
    """
    estado = obtener_estado_caja()
    if estado["estado"] == "abierta":
        return False
        
    estado["estado"] = "abierta"
    estado["ciclo_actual"] += 1  # Aumentamos el ID de ciclo (turno)
    estado["hora_apertura"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _guardar_estado(estado)
    registrar_movimiento(f"CAJA: Apertura (Ciclo {estado['ciclo_actual']}) a las {estado['hora_apertura']}")
    return True


def cerrar_caja() -> bool:
    """
    Cierra la caja registradora actual, registrando la hora de cierre.

    Returns:
        bool: True si la caja se cerró exitosamente, False si ya se encontraba cerrada.
    """
    estado = obtener_estado_caja()
    if estado["estado"] == "cerrada":
        return False
        
    estado["estado"] = "cerrada"
    estado["hora_cierre"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _guardar_estado(estado)
    registrar_movimiento(f"CAJA: Cierre (Ciclo {estado['ciclo_actual']}) a las {estado['hora_cierre']}")
    return True