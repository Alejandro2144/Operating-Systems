import time
import os
from tabulate import tabulate
import psutil
from rich.table import Table
import sys

def get_formatted_time(time_in_seconds):
    """
    Función que convierte un tiempo en segundos a un formato de H-M-S-MS.

    Args:
    - time (float): Tiempo en segundos.

    Returns:
    - string_output (str): Tiempo en formato de H-M-S-MS.
    """
    milliseconds = (time_in_seconds - int(time_in_seconds)) * 1000
    formatted_time = time.strftime('%H:%M:%S', time.localtime(time_in_seconds))
    string_output = formatted_time + f".{int(milliseconds):03}"

    return string_output

def calculate_total_time(start_time, end_time):
    """
    Función que calcula el tiempo total de carga de los archivos en milisegundos.

    Args:
    - start_time (float): Tiempo de inicio de la carga de los archivos en segundos.
    - end_time (float): Tiempo de finalización de la carga de los archivos en segundos.

    Returns:
    - total_time (float): Tiempo total de carga de los archivos en milisegundos.
    """
    total_time = (end_time - start_time) * 1000
    return total_time

def get_file_paths(folder_path):
    """
    Genera una lista de rutas de archivos en un directorio dado.

    Args:
    - folder_path (str): Ruta del directorio que contiene los archivos.

    Returns:
    - List[str]: Lista de rutas de archivos completas.
    """
    return [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]

def read_files(file_path, results):
    """
    Función que lee un archivo y guarda el resultado en una lista compartida.

    Args:
    - file_path (str): Ruta del archivo a leer.
    - results (list): Lista compartida para guardar los resultados.
    """

    try:
        with open(file_path, 'r', encoding='latin1') as file:
            data = file.read()
            results.append(( (sys.getsizeof(data))/(1024**2) ))
            # results.append((data))
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    
    return os.getpid()

def print_results(program_start_time, program_end_time, file_names, start_times, end_times, results, child_pids, rss, vms):
    """
    Función que imprime los resultados en una tabla.

    Args:
    - program_start_time (float): Tiempo de inicio del programa.
    - program_end_time (float): Tiempo de finalización del programa.
    - file_names (list): Lista de nombres de archivos.
    - start_times (list): Lista de tiempos de inicio de carga de archivos.
    - end_times (list): Lista de tiempos de finalización de carga de archivos.
    - results (list): Lista de resultados de la carga de archivos.
    """
    total_time = calculate_total_time(program_start_time, program_end_time)
    headers = ["Nombre", "T. Inicial", "T. Final", "Duración", "Peso", "PID", "RSS", "VMS"]
    table = []

    for i, file_name in enumerate(file_names):
        start_time = get_formatted_time(start_times[i])
        end_time = get_formatted_time(end_times[i])
        duration = calculate_total_time(start_times[i], end_times[i])
        result = results[i] if i < len(results) else "N/A"
        pid = child_pids[i] if i < len(child_pids) else "N/A"
        rss_memory = rss[i] if i < len(rss) else "N/A"
        vms_memory = vms[i] if i < len(vms) else "N/A"
        table.append([file_name, start_time, end_time, duration, result, pid, rss_memory, vms_memory])

    print(tabulate(table, headers=headers, tablefmt="grid"))
    print(f"\nTiempo total del programa: {total_time:.2f} ms\n")

def generate_table():
    """
    Genera una tabla que muestra el uso de la CPU.

    Returns:
    - Table: Tabla con el uso de la CPU por núcleo.
    """
    cpu_usages = psutil.cpu_percent(interval=None, percpu=True)
    table = Table(title="Uso de CPU por Núcleo")

    table.add_column("Núcleo", justify="right", style="cyan", no_wrap=True)
    table.add_column("Uso (%)", justify="right", style="magenta")

    for i, usage in enumerate(cpu_usages):
        table.add_row(f"Núcleo {i}", f"{usage:.2f}%")

    return table