import os
import csv
import time
import logging
from tabulate import tabulate

def get_formatted_time(time_in_seconds):
    """
    Función que convierte un tiempo en segundos a un formato de H-M-S-MS.

    Args:
    - time (float): Tiempo en segundos.

    Returns:
    - string_output (str): Tiempo en formato de H-M-S-MS.
    """
    milliseconds = (time_in_seconds - int(time_in_seconds)) * 1000
    formatted_time = time.strftime('%H:%M:%S', time.localtime(time_in_seconds))
    string_output = formatted_time + f".{int(milliseconds):03}"

    return string_output

def calculate_total_time(start_time, end_time):
    """
    Función que calcula el tiempo total de carga de los archivos en milisegundos.

    Args:
    - start_time (float): Tiempo de inicio de la carga de los archivos en segundos.
    - end_time (float): Tiempo de finalización de la carga de los archivos en segundos.

    Returns:
    - total_time (float): Tiempo total de carga de los archivos en milisegundos.
    """
    total_time = (end_time - start_time) * 1000
    return total_time

def read_files(file_path):
    """
    Función que lee un archivo y mide el tiempo de carga del archivo.

    Args:
    - file_path (str): Ruta del archivo a leer.

    Returns:
    - data (list): Datos leídos del archivo.
    - duration (float): Duración de la carga del archivo en milisegundos.
    """
    try:
        start_time = time.time()
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        end_time = time.time()
        duration = calculate_total_time(start_time, end_time)
        return data, duration
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return None, 0

def print_results(mode, start_time_program, end_time_program, file_paths, start_times, end_times, durations):
    """
    Imprime el resumen de tiempos de lectura y resultados en una tabla organizada.

    Args:
    - mode (str): Modo de lectura (single core, multi core).
    - start_time_program (float): Hora de inicio del programa.
    - end_time_program (float): Hora de finalización del programa.
    - file_paths (list): Lista de rutas a los archivos.
    - start_times (list): Tiempos de inicio de lectura de cada archivo.
    - end_times (list): Tiempos de fin de lectura de cada archivo.
    - durations (list): Duración de lectura de cada archivo en milisegundos.

    Returns:
    - None
    """
    total_time = calculate_total_time(start_time_program, end_time_program)
    headers = ["Archivo", "Hora de Inicio", "Hora de Fin", "Duración (ms)"]

    rows = [
        [os.path.basename(file_path), get_formatted_time(start), get_formatted_time(end), f"{duration:.2f}"]
        for file_path, start, end, duration in zip(file_paths, start_times, end_times, durations)
    ]

    print(f"\nHora de inicio del programa: {get_formatted_time(start_time_program)}")
    print(f"Hora de finalización del programa: {get_formatted_time(end_time_program)}")
    print(f"Tiempo total del proceso en modo {mode}: {total_time:.2f} ms")
    print("\nTabla de resumen de duración de carga de archivos:")
    print(tabulate(rows, headers=headers, tablefmt='grid'))
    print('\n')
