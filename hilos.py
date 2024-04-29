import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_file(file_path):
    data = pd.read_csv(file_path)
    stats = {
        'mean_open': data['Open'].mean(),
        'std_open': data['Open'].std(),
        'min_open': data['Open'].min(),
        'max_open': data['Open'].max(),
        'count': data['Open'].count()
    }
    # Preparar el nombre del archivo de salida
    output_filename = f"{file_path[:-4]}_out.csv"
    # Convertir el diccionario en DataFrame para exportar a CSV
    pd.DataFrame([stats]).to_csv(output_filename, index=False)
    return output_filename

def main(directory_path, num_workers):
    start_time = time.time()
    files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.csv')]
    results = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_file = {executor.submit(process_file, file): file for file in files}
        for future in as_completed(future_to_file):
            results.append(future.result())

    end_time = time.time()
    print(f"Procesado completado en {end_time - start_time} segundos. Resultados guardados en: {results}")

if __name__ == "__main__":
    # Cambia 'path_to_directory' al directorio donde tienes tus archivos CSV
    path_to_directory = "/Users/nickolasnolte/Desktop/   /COMPUTER SCIENCE/NOVENO SEMESTRE/SISTEMAS OPERATIVOS/proyectohilos(2)/so_data"
    # Configura el número de trabajadores según tu configuración de paralelismo
    main(path_to_directory, num_workers=4)  # Ajusta num_workers según el escenario de ejecución