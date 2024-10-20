import time
import os
import psutil
import csv
from collections import defaultdict
from tabulate import tabulate
from rich.table import Table
import chardet

# Funciones de tiempo
def get_formatted_time(time_in_seconds):
    """
    Convierte un tiempo en segundos a un formato de H-M-S-MS.
    """
    milliseconds = (time_in_seconds - int(time_in_seconds)) * 1000
    formatted_time = time.strftime('%H:%M:%S', time.localtime(time_in_seconds))
    string_output = formatted_time + f".{int(milliseconds):03}"
    return string_output

def calculate_total_time(start_time, end_time):
    """
    Calcula el tiempo total de carga de los archivos en milisegundos.
    """
    total_time = (end_time - start_time) * 1000
    return total_time

# Funciones de archivos
def get_file_paths(folder_path):
    """
    Genera una lista de rutas de archivos en un directorio dado.
    """
    return [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]

def detect_encoding(file_path):
    """
    Detecta la codificación de un archivo.
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read(100000)
    result = chardet.detect(raw_data)
    return result['encoding']

def read_file_in_chunks(file_path, chunk_size=1024):
    """
    Lee un archivo CSV en fragmentos para optimizar el uso de memoria.

    Args:
        file_path (str): La ruta del archivo CSV a leer.
        chunk_size (int): El tamaño del fragmento en el que se leerá el archivo. Por defecto es 1024.

    Returns:
        list: Una lista de diccionarios que contienen los datos de los videos.
    """
    videos = []
    # Extrae la región del nombre del archivo
    region = os.path.basename(file_path).split('_')[0].upper()

    try:
        # Detecta la codificación del archivo para leerlo correctamente
        encoding = detect_encoding(file_path)
        print(f"Detectando codificación para {file_path}: {encoding}")

        # Abre el archivo con la codificación detectada
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            reader = csv.DictReader(file)
            block = []

            for row in reader:
                try:
                    # Convierte las columnas relevantes a los tipos de datos apropiados y agrega a la lista temporal
                    block.append({
                        'title': row['title'],
                        'region': region,
                        'views': int(row['views']),
                        'likes': int(row['likes']),
                        'dislikes': int(row['dislikes'])
                    })
                except ValueError as ve:
                    # Maneja errores de conversión de datos numéricos
                    print(f"Error al convertir datos numéricos en {file_path}: {ve}")
                    continue

                # Si el bloque alcanza el tamaño del fragmento, se agrega a la lista principal y se limpia el bloque
                if len(block) >= chunk_size:
                    videos.extend(block)
                    block.clear()

            # Agrega cualquier dato restante en el bloque a la lista principal
            if block:
                videos.extend(block)

    except Exception as e:
        # Maneja cualquier error que ocurra durante la lectura del archivo
        print(f"Error al leer el archivo {file_path}: {str(e)}")

    return videos

# Funciones de monitoreo
def monitor_memory():
    """
    Monitorea y devuelve el uso de memoria en MB.
    """
    proc_memory = psutil.Process().memory_info()
    return round(proc_memory.rss / (1024 ** 2), 2)

def generate_table():
    """
    Genera una tabla con el uso de CPU por núcleo.
    """
    cpu_usages = psutil.cpu_percent(interval=None, percpu=True)
    table = Table(title="Uso de CPU por Núcleo")

    table.add_column("Núcleo", justify="right", style="cyan", no_wrap=True)
    table.add_column("Uso (%)", justify="right", style="magenta")

    for i, usage in enumerate(cpu_usages):
        table.add_row(f"Núcleo {i}", f"{usage:.2f}%")

    return table

# Funciones de análisis de datos
def analyze_data(videos):
    """
    Analiza los datos de los videos.
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

# Función para imprimir resultados
def print_results(program_start_time, program_end_time, file_names, start_times, end_times, memory_usage, videos):
    """
    Imprime los resultados del análisis de videos.
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
