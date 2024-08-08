import os
import time
import multiprocessing
from utils import read_files, get_formatted_time, print_results
import psutil

def load_files_sequential(folder_path):
    """
    Función que carga los archivos de un directorio y mide el tiempo de carga de cada uno
    utilizando procesos hijos para cargar los archivos secuencialmente utilizando un solo núcleo.

    Args: 
    - folder_path (str): Ruta del directorio que contiene los archivos a cargar.

    Returns:
    - None
    """
    manager = multiprocessing.Manager()
    results = manager.list()
    p = psutil.Process(os.getpid())

    is_first_file = True
    program_start_time = time.time()

    print(f'\nHora de inicio del programa: {get_formatted_time(program_start_time)}\n')

    start_times = []
    end_times = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if is_first_file: 
            is_first_file = False
            start_time_first_file = time.time()
            start_times.append(start_time_first_file)
        else:
            start_times.append(end_times[-1])

        process = multiprocessing.Process(target=read_files, args=(file_path, results))
        process.start()
        process.join()

        end_times.append(time.time())

        if process.exitcode != 0:
            print(f"Proceso hijo para el archivo {file_name} falló.")

        memory_info = p.memory_info()
        print(f"Memory used: {file_path}: {memory_info.rss / 1024:.2f} KB")

    program_end_time = time.time()

    final_memory_info = p.memory_info()
    print(f"Memory used at the end of the program: {final_memory_info.rss / 1024:.2f} KB")

    print_results("sequential", program_start_time, program_end_time, 
                list(os.listdir(folder_path)), start_times, end_times, list(results))