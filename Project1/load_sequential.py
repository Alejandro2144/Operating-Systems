import time
import multiprocessing
from utils import read_files, get_formatted_time, print_results, generate_table, get_file_paths
from rich.console import Console
from rich.live import Live

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

    console = Console()
    file_paths = get_file_paths(folder_path)

    end_times = []
    start_times = []
    child_pids = []

    print(f"\nProceso padre iniciado con PID: {multiprocessing.current_process().pid}")
    program_start_time = time.time()
    print(f'\nHora de inicio del programa: {get_formatted_time(program_start_time)}\n')

    with Live(console=console, refresh_per_second=4, screen=False) as live:
        for file_path in file_paths:
            # Mostrar uso de CPU
            live.update(generate_table())
            # Registrar el tiempo de inicio para cada archivo
            start_time = time.time()
            start_times.append(start_time)

            process = multiprocessing.Process(target=read_files, args=(file_path, results))
            process.start()
            # Registrar los pIDs de los procesos hijos
            child_pids.append(process.pid)

            process.join()

            end_times.append(time.time())

            if process.exitcode != 0:
                print(f"Proceso hijo con PID: {process.pid} para el archivo {file_path} falló.")

        program_end_time = time.time()

        print_results(program_start_time, program_end_time, 
                      file_paths, start_times, end_times, list(results), child_pids)
