import os
import time
import psutil
from utils import print_results, read_files, generate_table, get_file_paths
from rich.console import Console
from rich.live import Live

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
    available_cores = psutil.cpu_count(logical=True)
    core_to_use = [3]

    if core_to_use[0] >= available_cores:
        print(f"Error: El núcleo especificado ({core_to_use[0]}) no es válido. El sistema tiene {available_cores} núcleos.")
        return

    # Asignar el proceso a un solo núcleo
    p = psutil.Process(os.getpid())
    p.cpu_affinity(core_to_use)

    print(f"Usando el núcleo: {core_to_use[0]}")

    console = Console()
    file_paths = get_file_paths(folder_path)
    results = []
    durations = []
    start_times = []
    end_times = []

    with Live(console=console, refresh_per_second=4, screen=False) as live:
        start_time_program = time.time()
        
        for i, file_path in enumerate(file_paths):
           
            live.update(generate_table())
            
            if i == 0:
                start_time_first_file = time.time()
                start_times.append(start_time_first_file)
            else:
                start_times.append(end_times[-1])

            read_files(file_path, results)
            end_times.append(time.time())
            durations.append(end_times[-1] - start_times[-1])

        end_time_program = time.time()

        print_results(start_time_program, end_time_program, 
                      file_paths, start_times, end_times, results)
