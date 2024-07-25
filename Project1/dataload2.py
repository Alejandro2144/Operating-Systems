import os
import time
import csv

def load_file(folder_path):

    results = []
    time_results = []
    first_file = True
    program_start_time = time.time()
    print("\nHora de inicio del programa:", time.strftime('%H:%M:%S', time.localtime(program_start_time)), '\n')

    for file_name in os.listdir(folder_path):
        file_start_time = time.time()
        pid = os.fork()
        print(pid)

        if pid == 0:  # This block will be run by the child process
            try:

                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    data_list = list(reader)
                    results.append(data_list)

                file_end_time = time.time()
                total_time_file = file_end_time - file_start_time
                time_results.append(total_time_file)

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
                os._exit(1)

            os._exit(0)  # Child process ends here

        else:  # This block will be run by the parent process
            if first_file:
                first_file = False 
                start_time = file_start_time
                # If it's the first file, save the start time
                print("Hora de inicio de la carga del primer archivo:", time.strftime('%H:%M:%S', time.localtime(start_time)), '\n')

            _, status = os.wait() # Wait for the child process to finish
            if os.WIFEXITED(status):
                if os.WEXITSTATUS(status) != 0:
                    print(f"Child process for file {file_name} exited with an error")

    end_time = time.time()
    print("Hora de finalización de la carga del último archivo:", time.strftime('%H:%M:%S', time.localtime(end_time)), '\n')

    total_time = (end_time - start_time)*1000
    print(f"Tiempo total del proceso: {total_time:.2f} milisegundos", '\n')

    """Esta tabla no imprime nada debido a que los procesos hijos no comparten memoria con el proceso padre, por lo que no se pueden compartir variables entre ellos"""
    print("\nTabla de resumen de duración de carga de archivos:", '\n')
    for i, duration in enumerate(time_results):
        duration_ms = duration * 1000
        print(f"Archivo {i+1}: {duration_ms:.4f} milisegundos")
    print('\n')

    return results, total_time

load_file('./Project1/files')