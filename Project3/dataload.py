import argparse
from load_sequential import load_files_sequential
from load_single_core import load_files_single_core
from load_multi_core import load_files_multi_core

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lector de datos')
    parser.add_argument('-f', '--folder', required=True, help='Directorio en donde se encuentran los datos a procesar')
    parser.add_argument('-s', '--single', action='store_true', help='Procesar los archivos al tiempo cada uno en procesos independientes y en un solo núcleo')
    parser.add_argument('-m', '--multi', action='store_true', help='Procesar los archivos al tiempo cada uno en procesos independientes pero en cualquier núcleo disponible')
    args = parser.parse_args()

    if args.single:
        load_files_single_core(args.folder)
    elif args.multi:
        load_files_multi_core(args.folder)
    else:
        load_files_sequential(args.folder)
