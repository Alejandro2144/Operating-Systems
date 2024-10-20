import time
from utils import (
    get_formatted_time, print_results, generate_table,
    get_file_paths, read_file_in_chunks, monitor_memory
)
from rich.console import Console
from rich.live import Live

def load_files_sequential(folder_path):
    """
    Carga los archivos de un directorio de manera secuencial y realiza el análisis correspondiente.

    Args:
    - folder_path (str): Ruta del directorio que contiene los archivos .csv.
    """
    # Inicialización de la consola Rich para mostrar información en tiempo real
    console = Console()

    file_paths = get_file_paths(folder_path)

    # Listas para almacenar los tiempos y uso de memoria
    start_times = []
    end_times = []
    memory_usage = []
    results = []  # Almacena los videos leídos para su análisis

    program_start_time = time.time()
    print(f'\nHora de inicio del programa: {get_formatted_time(program_start_time)}\n')

    # Usar Rich.Live para mostrar en vivo la tabla de uso de CPU durante la carga de los archivos
    with Live(console=console, refresh_per_second=4, screen=False) as live:
        for file_path in file_paths:
            live.update(generate_table())

            start_time = time.time()
            start_times.append(start_time)

            # Leer el archivo en fragmentos para optimizar el uso de memoria
            videos = read_file_in_chunks(file_path)
            results.extend(videos)  # Agregar los videos leídos a la lista de resultados

            memory_usage.append(monitor_memory())

            end_times.append(time.time())

    program_end_time = time.time()

    print_results(
        program_start_time, program_end_time, 
        file_paths, start_times, end_times, memory_usage, results
    )
