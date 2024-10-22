import time
import threading
from utils import (
    get_formatted_time, print_results, generate_table,
    get_file_paths, read_file_in_chunks, monitor_memory
)
from rich.console import Console
from rich.live import Live

def process_file(file_path, results, memory_usage):
    """
    Procesa un archivo individual en un hilo.
    Args:
        file_path (str): Ruta del archivo a procesar.
        results (list): Lista para almacenar los videos procesados.
        memory_usage (list): Lista para almacenar el uso de memoria.
    """
    start_time = time.time()
    videos = read_file_in_chunks(file_path)
    memory = monitor_memory()
    end_time = time.time()

    # Guardar los resultados del archivo procesado
    results.append((file_path, start_time, end_time, memory, videos))

def load_files_single_core(folder_path):
    """
    Carga y procesa archivos utilizando hilos en un solo núcleo.
    Args:
        folder_path (str): Ruta del directorio que contiene los archivos a procesar.
    """
    console = Console()
    file_paths = get_file_paths(folder_path)

    # Listas compartidas para almacenar resultados y uso de memoria
    results = []
    memory_usage = []

    program_start_time = time.time()
    print(f'\nHora de inicio del programa: {get_formatted_time(program_start_time)}\n')

    threads = []

    # Usar Rich.Live para mostrar en vivo el uso de CPU
    with Live(console=console, refresh_per_second=4, screen=False) as live:
        # Crear un hilo para cada archivo
        for file_path in file_paths:
            thread = threading.Thread(
                target=process_file, 
                args=(file_path, results, memory_usage)
            )
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        live.update(generate_table())

    program_end_time = time.time()

    # Desempaquetar los resultados
    file_paths, start_times, end_times, memory_usage, all_videos = zip(*results)
    all_videos = [video for sublist in all_videos for video in sublist]

    # Imprimir los resultados finales
    print_results(
        program_start_time, program_end_time,
        file_paths, start_times, end_times, memory_usage, all_videos
    )
