import os
import time
import multiprocessing
from utils import calculate_total_time, process_files, get_formatted_time, set_cpu_affinity

def load_files_single_core(folder_path):
    """
    Función que carga los archivos de un directorio y mide el tiempo de carga de cada uno
    utilizando procesos para cargar los archivos en paralelo en el mismo núcleo del programa.

    Args: 
    - folder_path (str): Ruta del directorio que contiene los archivos a cargar.

    Returns:
    - None
    """

    manager = multiprocessing.Manager()
    time_results = manager.list()
    results = manager.list()
    processes = []
    # core_id = 0

    is_first_file = True

    print(f"\nProceso padre iniciado con PID {os.getpid()}.", '\n')

    program_start_time = time.time()
    print('Hora de inicio del programa: ', get_formatted_time(program_start_time), '\n')

    for file_name in os.listdir(folder_path):

        if is_first_file:  # Este bloque será ejecutado por el proceso hijo
            is_first_file = False
            first_start_time = time.time()
            print("Hora de inicio de la carga del primer archivo:", get_formatted_time(first_start_time), '\n')

        process = multiprocessing.Process(target=process_files, args=(folder_path, file_name, time_results, results))
        process.start()
        # set_cpu_affinity(process.pid, core_id)
        # print(f"Proceso hijo con PID {process.pid} para el archivo {file_name} iniciado.")
        processes.append(process)

    for process in processes:
        process.join()

        if process.exitcode != 0:
            print(f"Proceso hijo con PID {process.pid} para el archivo {file_name} falló.")

    end_time = time.time()
    print("Hora de finalización de la carga del último archivo:", get_formatted_time(end_time), '\n')

    total_time = calculate_total_time(program_start_time, end_time)
    print(f"Tiempo total del proceso: {total_time:.2f} ms", '\n')

    print("Tabla de resumen de duración de carga de archivos:", '\n')
    for i, duration in enumerate(time_results):
        print(f"Archivo {i+1}: {duration:.2f} ms")
    print('\n')