import os
import pandas as pd
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse

def calculate_statistic(data, stat):
    if stat == 'mean_open':
        return data['Open'].mean()
    elif stat == 'std_open':
        return data['Open'].std()
    elif stat == 'min_open':
        return data['Open'].min()
    elif stat == 'max_open':
        return data['Open'].max()
    elif stat == 'count':
        return data['Open'].count()

def process_file(file_path, num_workers):
    try:
        data = pd.read_csv(file_path)
        stats = ['mean_open', 'std_open', 'min_open', 'max_open', 'count']
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_stat = {executor.submit(calculate_statistic, data, stat): stat for stat in stats}
            results = {future_to_stat[future]: future.result() for future in as_completed(future_to_stat)}
        
        output_filename = f"{file_path[:-4]}_out.csv"
        pd.DataFrame([results]).to_csv(output_filename, index=False)
        return output_filename
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"

def run_sequential(files, num_workers):
    results = []
    for file in files:
        result = process_file(file, num_workers)
        results.append(result)
    return results

def run_parallel(files, num_workers):
    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_file = {executor.submit(process_file, file, num_workers): file for file in files}
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
        results = run_sequential(files, num_workers)
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
        'Number of Workers': [num_workers]
    }
    pd.DataFrame(perf_data).to_csv('performance_metrics.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('mode', choices=['sequential', 'parallel'], help='Execution mode')
    parser.add_argument('num_workers', type=int, help='The number of worker threads')
    args = parser.parse_args()

    main(args.mode, args.num_workers)
