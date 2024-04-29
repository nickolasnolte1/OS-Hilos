import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse

def process_file(file_path):
    try:
        data = pd.read_csv(file_path)
        stats = {
            'mean_open': data['Open'].mean(),
            'std_open': data['Open'].std(),
            'min_open': data['Open'].min(),
            'max_open': data['Open'].max(),
            'count': data['Open'].count()
        }
        output_filename = f"{file_path[:-4]}_out.csv"
        pd.DataFrame([stats]).to_csv(output_filename, index=False)
        return output_filename
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"

def main(num_workers):
    directory_path = '/app/so_data'  # Updated path to the data directory
    start_time = time.time()
    files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.csv')]
    results = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_file = {executor.submit(process_file, file): file for file in files}
        for future in as_completed(future_to_file):
            results.append(future.result())

    end_time = time.time()
    print(f"Processed completed in {end_time - start_time} seconds. Results saved in: {results}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('num_workers', type=int, help='The number of worker threads')
    args = parser.parse_args()

    main(args.num_workers)
