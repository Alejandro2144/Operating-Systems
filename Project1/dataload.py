import os
import time
import csv

def load_file(folder_path):
    results = []
    time_results = []
    first_file = True
    program_start_time = time.time()
    print("Hora de inicio del programa:", time.strftime('%H:%M:%S', time.localtime(program_start_time)))

    for file_name in os.listdir(folder_path):
            file_start_time = time.time()
            # Si es el primer archivo, se guarda el tiempo de inicio
            if first_file:
                first_file = False
                start_time = file_start_time
                print("Hora de inicio de la carga del primer archivo:", time.strftime('%H:%M:%S', time.localtime(start_time)))
            
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                data_list = list(reader)
                results.append(data_list)

            file_end_time = time.time()
            total_time_file = file_end_time - file_start_time
            time_results.append(total_time_file)
            print("Duración de la carga del archivo", total_time_file)

    end_time = time.time()
    print("Hora de finalización de la carga del último archivo:", time.strftime('%H:%M:%S', time.localtime(end_time)))

    total_time = end_time - start_time
    print(f"Tiempo total del proceso: {total_time:.4f} segundos")

    print("\nTabla de resumen de duración de carga de archivos:")
    for i, duration in enumerate(time_results):
        print(f"Archivo {i+1}: {duration:.4f} segundos")
    
    return results, total_time

load_file("files")

#Hola soy Diego
