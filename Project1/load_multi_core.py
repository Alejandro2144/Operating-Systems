import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from utils import print_results, read_files, generate_table, get_file_paths
from rich.console import Console
from rich.live import Live

def load_files_multi_core(folder_path):
    """
    Función que carga los archivos de un directorio y mide el tiempo de carga de cada uno
    utilizando múltiples núcleos.

    Args: 
    - folder_path (str): Ruta del directorio que contiene los archivos a cargar.

    Returns:
    - None
    """
    num_cores = multiprocessing.cpu_count()
    print(f"\nLeyendo los archivos en multi core, utilizando {num_cores} núcleos")

    console = Console()
    file_paths = get_file_paths(folder_path)

    manager = multiprocessing.Manager()
    results = manager.list()

    start_times = [time.time()] * len(file_paths)
    end_times = []

    with Live(console=console, refresh_per_second=4, screen=False) as live:
        start_time_program = time.time()
        
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            future_results = [executor.submit(read_files, file_path, results) for file_path in file_paths]

            for future in future_results:

                live.update(generate_table())
                future.result()
                end_times.append(time.time())

        end_time_program = time.time()

        print_results(start_time_program, end_time_program, 
                      file_paths, start_times, end_times, list(results))
