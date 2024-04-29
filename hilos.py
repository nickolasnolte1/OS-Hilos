import os
import pandas as pd
import psutil
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

def run_sequential(files):
    results = []
    for file in files:
        result = process_file(file)
        results.append(result)
    return results

def run_parallel(files, num_workers):
    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_file = {executor.submit(process_file, file): file for file in files}
        for future in as_completed(future_to_file):
            results.append(future.result())
    return results

def main(mode, num_workers):
    directory_path = '/app/so_data'
    start_time = time.time()
    
    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_percent(interval=None)

    files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.csv')]
    results = []

    if mode == 'sequential':
        results = run_sequential(files)
    elif mode == 'parallel':
        results = run_parallel(files, num_workers)

    end_time = time.time()
    cpu_end = process.cpu_percent(interval=None)
    cpu_usage = (cpu_end - cpu_start) / psutil.cpu_count()

    total_time = end_time - start_time
    print(f"Processed completed in {total_time} seconds. Results saved in: {results}")

    perf_data = {
        'Mode': [mode],
        'Total Time (s)': [total_time],
        'Average CPU Usage (%)': [cpu_usage],
        'Number of Workers': [num_workers] if mode == 'parallel' else [1]
    }
    pd.DataFrame(perf_data).to_csv('performance_metrics.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('mode', choices=['sequential', 'parallel'], help='Execution mode')
    parser.add_argument('num_workers', type=int, help='The number of worker threads')
    args = parser.parse_args()

    main(args.mode, args.num_workers)


