import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from utils import (
    get_formatted_time, print_results, generate_table,
    get_file_paths, read_file_in_chunks, monitor_memory
)

from rich.console import Console
from rich.live import Live

def process_file(file_path):
    """
    Procesa un archivo individual en un solo núcleo.

    Args:
        file_path (str): Ruta del archivo a procesar.

    Returns:
        tuple: Una tupla que contiene la ruta del archivo, tiempo de inicio, tiempo de finalización,
        uso de memoria y los videos procesados.
    """
    start_time = time.time()
    videos = read_file_in_chunks(file_path)
    memory_usage = monitor_memory()
    end_time = time.time()
    return file_path, start_time, end_time, memory_usage, videos

def load_files_single_core(folder_path):
    """
    Carga y procesa archivos en paralelo utilizando un solo núcleo, un solo proceso y múltiples hilos.

    Args:
        folder_path (str): Ruta del directorio que contiene los archivos a procesar.
    
    Este metodo utiliza un Pool de procesos para cargar y procesar múltiples archivos 
    simultáneamente, pero limitado a un solo núcleo del procesador.
    
    """
    console = Console()
    file_paths = get_file_paths(folder_path)

    program_start_time = time.time()
    print(f'\nHora de inicio del programa: {get_formatted_time(program_start_time)}\n')

    results = []
    with Live(console=console, refresh_per_second=4, screen=False) as live:
        with ThreadPoolExecutor() as executor:
            # Se envían los archivos a procesar al executor
            future_to_file = {executor.submit(process_file, file_path): file_path for file_path in file_paths}

            # Recolecta los resultados a medida que se completan
            for future in concurrent.futures.as_completed(future_to_file):
                results.append(future.result())
                live.update(generate_table())

    program_end_time = time.time()

    file_paths, start_times, end_times, memory_usage, all_videos = zip(*results)
    all_videos = [video for sublist in all_videos for video in sublist]

    print_results(
        program_start_time, program_end_time,
        file_paths, start_times, end_times, memory_usage, all_videos
    )