import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from utils import (
    get_formatted_time, print_results, generate_table,
    get_file_paths, read_file_in_chunks, monitor_memory, process_chunk
)
from rich.console import Console
from rich.live import Live

def process_file(file_path):
    """
    Procesa un archivo individual utilizando múltiples hilos.

    Args:
        file_path (str): Ruta al archivo que se va a procesar.

    Returns:
        tuple: Contiene la ruta del archivo, tiempo de inicio, tiempo de finalización,
               uso de memoria y los videos procesados.

    Esta función utiliza un ThreadPoolExecutor para procesar los chunks del archivo
    en paralelo, mejorando la eficiencia del procesamiento.

    """
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        chunks = read_file_in_chunks(file_path, return_chunks=True)
        videos = list(executor.map(process_chunk, chunks))
    
    videos = [video for sublist in videos for video in sublist]
    memory_usage = monitor_memory()
    end_time = time.time()
    return file_path, start_time, end_time, memory_usage, videos

def load_files_multi_core(folder_path):
    """
    Carga y procesa archivos en paralelo utilizando múltiples núcleos.

    Args:
        folder_path (str): Ruta a la carpeta que contiene los archivos a procesar.

    Este método utiliza un ProcessPoolExecutor para procesar múltiples archivos
    simultáneamente, aprovechando múltiples núcleos del procesador. Además,
    cada archivo se procesa internamente utilizando múltiples hilos.

    """
    console = Console()
    file_paths = get_file_paths(folder_path)

    program_start_time = time.time()
    print(f'\nHora de inicio del programa: {get_formatted_time(program_start_time)}\n')

    with Live(console=console, refresh_per_second=4, screen=False) as live:
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(process_file, file_paths))
        
        live.update(generate_table())

    program_end_time = time.time()

    file_paths, start_times, end_times, memory_usage, all_videos = zip(*results)
    all_videos = [video for sublist in all_videos for video in sublist]

    print_results(
        program_start_time, program_end_time,
        file_paths, start_times, end_times, memory_usage, all_videos
    )
