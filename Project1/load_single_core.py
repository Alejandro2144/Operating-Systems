import os
import time
import psutil
from utils import calculate_total_time, get_formatted_time

def read_file(file_path):
    """
    Lee un archivo CSV y mide el tiempo de carga.
    
    Args:
    - file_path (str): Ruta del archivo a leer.
    
    Returns:
    - duration (float): Tiempo que tardó en cargar el archivo en segundos.
    """
    start_time = time.time()
    data = []
    try:
        with open(file_path, 'r') as file:
            data = list(file)  # Leer el archivo
    except Exception as e:
        print(f"Error procesando el archivo {file_path}: {e}")
    end_time = time.time()
    duration = end_time - start_time
    return duration

def load_files_single_core(folder_path):
    """
    Carga los archivos de un directorio en un solo núcleo.
    
    Args:
    - folder_path (str): Ruta del directorio que contiene los archivos a cargar.
    
    Returns:
    - None
    """
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

    def process_function(file_path):
        # Establece la afinidad a un solo núcleo (0 por ejemplo)
        p = psutil.Process(os.getpid())
        p.cpu_affinity([0])
        return read_file(file_path)

    program_start_time = time.time()
    print('\nHora de inicio del programa: ', get_formatted_time(program_start_time), '\n')

    durations = []
    for file_path in file_paths:
        duration = process_function(file_path)
        durations.append(duration)

    end_time = time.time()
    print("Hora de finalización de la carga del último archivo:", get_formatted_time(end_time), '\n')

    total_time = calculate_total_time(program_start_time, end_time)
    print(f"Tiempo total del proceso: {total_time:.2f} ms", '\n')

    print("Tabla de resumen de duración de carga de archivos:", '\n')
    for i, duration in enumerate(durations):
        print(f"Archivo {i+1}: {duration:.2f} s")
    print('\n')
