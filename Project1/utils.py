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

def read_files(file_path, results):
    """
    Función que lee un archivo y guarda el resultado en una lista compartida.

    Args:
    - file_path (str): Ruta del archivo a leer.
    - results (list): Lista compartida para guardar los resultados.
    """
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            results.append((file_path, len(data)))  # Append file path and length of data as an example
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")

def print_results(mode, program_start_time, program_end_time, file_names, start_times, end_times, results):
    """
    Función que imprime los resultados en una tabla.

    Args:
    - mode (str): Modo de carga de archivos (secuencial o paralelo).
    - program_start_time (float): Tiempo de inicio del programa.
    - program_end_time (float): Tiempo de finalización del programa.
    - file_names (list): Lista de nombres de archivos.
    - start_times (list): Lista de tiempos de inicio de carga de archivos.
    - end_times (list): Lista de tiempos de finalización de carga de archivos.
    - results (list): Lista de resultados de la carga de archivos.
    """
    total_time = calculate_total_time(program_start_time, program_end_time)
    headers = ["File Name", "Start Time", "End Time", "Duration (ms)", "Result"]
    table = []

    for i, file_name in enumerate(file_names):
        start_time = get_formatted_time(start_times[i])
        end_time = get_formatted_time(end_times[i])
        duration = calculate_total_time(start_times[i], end_times[i])
        result = results[i] if i < len(results) else "N/A"
        table.append([file_name, start_time, end_time, duration, result])

    print(tabulate(table, headers=headers, tablefmt="grid"))
    print(f"\nTotal program time: {total_time:.2f} ms")

