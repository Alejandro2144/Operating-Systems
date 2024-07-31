import os
import time
import multiprocessing
import psutil
from utils import calculate_total_time, process_file_secuentially, get_formatted_time

def set_affinity(pid, core_id):
    """ Configura la afinidad del núcleo para un proceso específico usando psutil. """
    try:
        p = psutil.Process(pid)
        p.cpu_affinity([core_id])
    except psutil.NoSuchProcess:
        print(f"El proceso con PID {pid} no existe.")
    except psutil.AccessDenied:
        print(f"Acceso denegado para modificar la afinidad del proceso con PID {pid}.")
    except Exception as e:
        print(f"Error al establecer la afinidad del núcleo: {e}")

def load_files_single_core(folder_path):
    """
    Carga archivos CSV en procesos independientes, asignando cada uno al mismo núcleo.

    Args:
    - folder_path (str): Ruta del directorio que contiene los archivos a cargar.

    Returns:
    - None
    """
    core_id = 0  # Ajusta esto según tu necesidad

    # Obtener la lista de archivos CSV
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    processes = []
    time_results = []
    results = []

    program_start_time = time.time()
    print('\nHora de inicio del programa: ', get_formatted_time(program_start_time), '\n')

    for file_name in csv_files:
        # Crear un proceso hijo para cada archivo
        process = multiprocessing.Process(target=process_file_secuentially, args=(folder_path, file_name, time_results, results))
        process.start()
        set_affinity(process.pid, core_id)  # Configurar afinidad del núcleo
        processes.append(process)

    for process in processes:
        process.join()

        if process.exitcode != 0:
            print(f"Proceso hijo para el archivo {file_name} falló.")

    end_time = time.time()
    print("Hora de finalización de la carga del último archivo:", get_formatted_time(end_time), '\n')

    total_time = calculate_total_time(program_start_time, end_time)
    print(f"Tiempo total del proceso: {total_time:.2f} ms", '\n')

    print("Tabla de resumen de duración de carga de archivos:", '\n')
    for i, duration in enumerate(time_results):
        print(f"Archivo {i+1}: {duration:.2f} ms")
    print('\n')