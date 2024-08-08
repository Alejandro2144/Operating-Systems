import os
import time
import psutil
from utils import calculate_total_time, get_formatted_time, print_results, read_files

def load_files_single_core(folder_path):
    """
    Función que carga los archivos de un directorio y mide el tiempo de carga de cada uno
    utilizando el mismo núcleo para todos los archivos.

    Args: 
    - folder_path (str): Ruta del directorio que contiene los archivos a cargar.

    Returns:
    - None
    """
    print(f"\nLeyendo los archivos en [bold cyan] single core [/bold cyan] mode")

    start_time_program = time.time()

    # Asignar el proceso a un solo núcleo
    p = psutil.Process(os.getpid())
    p.cpu_affinity([0])

    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]
    
    data_list = []
    durations = []
    start_times = []
    end_times = []

    for i, file_path in enumerate(file_paths):
        if i == 0:
            start_time_first_file = time.time()
            start_times.append(start_time_first_file)
        else:
            start_times.append(end_times[-1])

        data, duration = read_files(file_path)
        if data is not None:
            data_list.append(data)
        durations.append(duration)
        end_times.append(time.time())

        memory_info = p.memory_info()
        print(f"Memory used: {file_path}: {memory_info.rss / (1024 / 1024):.2f} MB")

    end_time_program = time.time()

    final_memory_info = p.memory_info()
    print(f"Memory used at the end of the program: {final_memory_info.rss / (1024 / 1024):.2f} MB")

    print_results("single core", start_time_program, end_time_program, 
                file_paths, start_times, end_times, durations)
