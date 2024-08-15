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

    start_times = []
    end_times = []
    child_pids = []

    with Live(console=console, refresh_per_second=4, screen=False) as live:
        start_time_program = time.time()
        
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            future_results = []

            # Se guarda un objeto Future en future_results por cada archivo para que sea leido por el executor
            for file_path in file_paths:
                start_times.append(time.time())
                future_results.append(executor.submit(read_files, file_path, results))

            # Se procesan los resultados de los archivos
            for future in future_results:
                live.update(generate_table())
                try:
                    child_pids.append(future.result())
                except Exception as e:
                    print(f"Error al procesar el archivo: {e}")
                end_times.append(time.time())

        end_time_program = time.time()

        print_results(start_time_program, end_time_program, 
                      file_paths, start_times, end_times, results, child_pids)