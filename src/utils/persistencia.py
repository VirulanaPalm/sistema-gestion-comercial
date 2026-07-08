"""
Módulo para el manejo de la persistencia de datos en la aplicación.
Proporciona funciones para cargar y guardar información en formato JSON,
asegurando la integridad y accesibilidad de los datos del sistema.
"""

import json
import os


def cargar_datos(nombre_archivo: str) -> list:
    """
    Carga una lista de diccionarios desde un archivo JSON especificado.
    Si el archivo no existe o ocurre un error de lectura, retorna
    una lista vacía.

    Args:
        nombre_archivo (str): Ruta del archivo JSON a leer.

    Returns:
        list: Lista con los datos cargados, o una lista vacía en
              caso de error o inexistencia.
    """
    if not os.path.exists(nombre_archivo):
        return []

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def guardar_datos(nombre_archivo: str, datos: list) -> None:
    """
    Guarda una lista de diccionarios en un archivo JSON, con formato
    legible (indentado) y respetando caracteres especiales mediante
    codificación UTF-8.

    Args:
        nombre_archivo (str): Ruta del archivo JSON donde se
                              guardarán los datos.
        datos (list): Lista de diccionarios que se desea persistir.

    Returns:
        None
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error al guardar los datos en {nombre_archivo}: {e}")