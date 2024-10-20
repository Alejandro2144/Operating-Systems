import time
import os
import psutil
import csv
from collections import defaultdict
from tabulate import tabulate
from rich.table import Table

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

def monitor_memory():
    """
    Monitorea y devuelve el uso de memoria en MB.

    Returns:
    - memory_usage (float): Uso de memoria en MB.
    """
    proc_memory = psutil.Process().memory_info()
    return round(proc_memory.rss / (1024 ** 2), 2)

import os
import csv

def read_file_in_chunks(file_path, chunk_size=1024):
    """
    Lee un archivo CSV en fragmentos para optimizar el uso de memoria.

    Args:
    - file_path (str): Ruta del archivo a leer.
    - chunk_size (int): Tamaño del fragmento en registros. Default: 1024.

    Returns:
    - List[dict]: Lista de videos con sus datos y la región correspondiente.
    """
    # Lista principal para almacenar los videos leídos
    videos = []

    # Extraer la región del nombre del archivo (por ejemplo: 'US_videos.csv' → 'US')
    region = os.path.basename(file_path).split('_')[0].upper()

    try:
        # Abrir el archivo usando UTF-8 (intentar con codificación estándar)
        with open(file_path, 'r', encoding='utf-8') as file:
            # Crear un lector CSV que convierte cada fila en un diccionario
            reader = csv.DictReader(file)

            # Bloque temporal para acumular registros y controlar la memoria
            block = []

            # Iterar sobre cada fila del archivo CSV
            for row in reader:
                # Añadir la fila procesada al bloque temporal
                block.append({
                    'title': row['title'],  
                    'region': region,  
                    'views': int(row['views']),  
                    'likes': int(row['likes']),  
                    'dislikes': int(row['dislikes']) 
                })

                # Si el bloque alcanza el tamaño definido (default 1024), transferir los datos a la lista principal
                if len(block) >= chunk_size:
                    videos.extend(block)  # Agregar los datos del bloque a 'videos'
                    block.clear()  # Vaciar el bloque para liberar memoria

            # Si quedan registros en el bloque después del bucle, procesarlos también
            if block:
                videos.extend(block)

    # Capturar cualquier excepción que ocurra durante la lectura del archivo
    except Exception as e:
        # Imprimir un mensaje de error si hay problemas al leer el archivo
        print(f"Error al leer el archivo {file_path}: {str(e)}")

    # Devolver la lista completa de videos leídos
    return videos

def analyze_data(videos):
    """
    Analiza los videos para encontrar el más y menos popular globalmente y por región.

    Args:
    - videos (list): Lista de videos con su información.

    Returns:
    - Tuple[dict, dict, dict]: Video más popular, menos popular, y estadísticas por región.
    """
    if not videos:
        return None

    most_popular = max(videos, key=lambda x: x['views'])
    least_popular = min(videos, key=lambda x: x['views'])

    regions = defaultdict(list)
    for video in videos:
        regions[video['region']].append(video)

    region_stats = {
        region: {
            "most_popular": max(videos_in_region, key=lambda x: x['views']),
            "least_popular": min(videos_in_region, key=lambda x: x['views'])
        }
        for region, videos_in_region in regions.items()
    }

    return most_popular, least_popular, region_stats

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

def print_results(program_start_time, program_end_time, file_names, start_times, end_times, memory_usage, videos):
    """
    Imprime un resumen con tiempos, memoria utilizada y análisis de los videos.

    Args:
    - program_start_time (float): Tiempo de inicio del programa.
    - program_end_time (float): Tiempo de finalización del programa.
    - file_names (list): Lista de nombres de archivos.
    - start_times (list): Lista de tiempos de inicio de carga de archivos.
    - end_times (list): Lista de tiempos de finalización de carga de archivos.
    - memory_usage (list): Uso de memoria por archivo.
    - videos (list): Lista de videos leídos para el análisis.
    """
    total_time = calculate_total_time(program_start_time, program_end_time)
    headers = ["Nombre", "T. Inicial", "T. Final", "Duración (ms)", "Memoria (MB)"]
    table = []

    for i, file_name in enumerate(file_names):
        start_time = get_formatted_time(start_times[i])
        end_time = get_formatted_time(end_times[i])
        duration = calculate_total_time(start_times[i], end_times[i])
        memory = memory_usage[i] if i < len(memory_usage) else "N/A"
        table.append([file_name, start_time, end_time, duration, memory])

    print(tabulate(table, headers=headers, tablefmt="grid"))
    print(f"\nTiempo total del programa: {total_time / 1000:.2f} segundos\n")

    # Analizar los datos
    most_popular, least_popular, region_stats = analyze_data(videos)

    if most_popular and least_popular:
        print("\nResultados del análisis de videos:")
        print(f"📈 Video más popular del año: '{most_popular['title']}' con {most_popular['views']} vistas.")
        print(f"📉 Video menos popular del año: '{least_popular['title']}' con {least_popular['views']} vistas.")

        print("\nVideos más y menos populares por región:")
        for region, stats in region_stats.items():
            print(f"\n🌎 Región: {region}")
            print(f"  - 📈 Más popular: '{stats['most_popular']['title']}' ({stats['most_popular']['views']} vistas)")
            print(f"  - 📉 Menos popular: '{stats['least_popular']['title']}' ({stats['least_popular']['views']} vistas)")