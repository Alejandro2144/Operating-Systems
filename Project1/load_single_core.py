import os
import time
import psutil
from utils import print_results, read_files, process_files, generate_table, get_file_paths
from rich.console import Console
from rich.live import Live
from multiprocessing import Process

def load_files_single_core(folder_path):
    """
    Función que carga los archivos de un directorio y mide el tiempo de carga de cada uno
    utilizando el mismo núcleo para todos los archivos.

    Args: 
    - folder_path (str): Ruta del directorio que contiene los archivos a cargar.

    Returns:
    - None
    """

    # Obtener el número de núcleos disponibles y verificar el núcleo a usar
    #available_cores = psutil.cpu_count(logical=True)
    #core_to_use = [3]

    #if core_to_use[0] >= available_cores:
    #    print(f"Error: El núcleo especificado ({core_to_use[0]}) no es válido. El sistema tiene {available_cores} núcleos.")
    #    return

    # Asignar el proceso a un solo núcleo
    #p = psutil.Process(os.getpid())
    #p.cpu_affinity(core_to_use)

    #print(f"Usando el núcleo: {core_to_use[0]}")

    console = Console()
    file_paths = get_file_paths(folder_path)
    results = []
    start_times = []
    end_times = []
    child_pids = []
    processes = []

    print(f"\nProceso padre iniciado con PID: {os.getpid()}")

    with Live(console=console, refresh_per_second=4, screen=False) as live:
        start_time_program = time.time()
        
        for file_path in file_paths:
            live.update(generate_table())

            current_process = Process(target=process_files, args=(file_path, results, start_times, end_times))
            # Iniciar el proceso hijo
            processes.append(current_process)
            current_process.start()
            # Registrar los pIDs de los procesos hijos
            child_pids.append(current_process.pid)
            # Asignar el proceso a un solo núcleo
            current_process.cpu_affinity([0])
        # Esperar a que todos los procesos hijos terminen
        for process in processes:
            process.join()

        end_time_program = time.time()

        print_results(start_time_program, end_time_program, 
                      file_paths, start_times, end_times, results, child_pids)
