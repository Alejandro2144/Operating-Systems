import os
import csv
import time
import logging

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
    total_time = (end_time - start_time)*1000
    return total_time

def process_file_secuentially(folder_path, file_name, time_results, results):
    """
    Función que procesa secuencialmente la cantidad de archivos que haya en un directorio y mide el tiempo de carga de cada uno.

    Args:
    - folder_path (str): Ruta del directorio que contiene los archivos a cargar.
    - file_name (str): Nombre del archivo a procesar.
    - file_start_time (float): Tiempo de inicio de la carga del archivo en segundos.
    - time_results (list): Lista enlazada con los tiempos de carga de los archivos.

    Returns:
    - None
    """

    try:
        file_path = os.path.join(folder_path, file_name)
        file_start_time = time.time()
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data_list = list(reader)
            results.append(data_list)
        file_end_time = time.time()
        total_time_file = calculate_total_time(file_start_time, file_end_time)
        time_results.append(total_time_file)

    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")
        os._exit(1)