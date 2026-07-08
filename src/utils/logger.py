"""
Módulo para el registro de eventos y auditoría del sistema (Logger).
Se encarga de guardar un historial detallado de las operaciones
realizadas, incluyendo fecha y hora, y permite la lectura de dichos
movimientos.
"""

import os
from datetime import datetime

# Definimos dónde se va a guardar el historial
RUTA_LOG = "data/movimientos.log"


def registrar_movimiento(accion: str) -> None:
    """
    Guarda un registro de la acción realizada con su fecha y hora.
    Se usa el modo 'a' (append) para no borrar el historial anterior.

    Args:
        accion (str): Descripción de la acción o movimiento a
                      registrar en el sistema.

    Returns:
        None
    """
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"[{fecha_hora}] {accion}\n"

    try:

        with open(RUTA_LOG, "a", encoding="utf-8") as f:
            f.write(mensaje)
    except IOError as e:
        print(f"Error al escribir en el log: {e}")


def leer_movimientos() -> str:
    """
    Lee todo el historial de movimientos para mostrarlo en la interfaz.

    Returns:
        str: El contenido completo del archivo de registro, o un
             mensaje indicando que está vacío o que hubo un error
             de lectura.
    """
    if not os.path.exists(RUTA_LOG):
        return "Aún no hay movimientos registrados en el sistema."
    try:
        with open(RUTA_LOG, "r", encoding="utf-8") as f:
            return f.read()
    except IOError:
        return "Error al leer el archivo de movimientos."
