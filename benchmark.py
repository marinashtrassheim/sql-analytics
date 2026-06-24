import os
import time
import re
import pandas as pd
import clickhouse_connect
from pathlib import Path

HOST = os.getenv('CLICKHOUSE_HOST', 'clickhouse')
PORT = int(os.getenv('CLICKHOUSE_PORT', 8123))
USER = os.getenv('CLICKHOUSE_USER', 'default')
PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', 'clickhouse')

client = clickhouse_connect.get_client(host=HOST, port=PORT, user=USER, password=PASSWORD)

QUERIES_DIR = Path('/app/queries')
RESULTS_FILE = 'benchmark_results.csv'
RUNS = 5


def extract_read_stats(explain_output):
    rows = None
    bytes_ = None
    for line in explain_output.split('\n'):
        if 'ReadRows' in line:
            match = re.search(r'ReadRows:\s*(\d+)', line)
            if match:
                rows = int(match.group(1))
        if 'ReadBytes' in line:
            match = re.search(r'ReadBytes:\s*(\d+)', line)
            if match:
                bytes_ = int(match.group(1))
    return rows, bytes_


def run_benchmark():
    results = []
    for sql_file in sorted(QUERIES_DIR.glob('*.sql')):
        query_name = sql_file.stem
        with open(sql_file, 'r') as f:
            sql = f.read()

        print(f"Benchmarking {query_name}...")
        explain_str = None
        read_rows = read_bytes = None

        for run in range(RUNS + 1):
            start = time.perf_counter()
            client.query(sql)
            elapsed = time.perf_counter() - start
            if run == 0:
                continue
            if run == 1:
                explain_result = client.query(f"EXPLAIN {sql}")
                explain_str = '\n'.join([row[0] for row in explain_result.result_rows])
                read_rows, read_bytes = extract_read_stats(explain_str)
                with open(f"{query_name}_explain.txt", 'w') as f:
                    f.write(explain_str)
            results.append({
                'query': query_name,
                'run': run,
                'time_sec': elapsed,
                'read_rows': read_rows,
                'read_bytes': read_bytes
            })

    df = pd.DataFrame(results)
    df.to_csv(RESULTS_FILE, index=False)
    print(f"\nResults saved to {RESULTS_FILE}")

    agg = df.groupby('query').agg({
        'time_sec': ['median', 'min', 'max'],
        'read_rows': 'first',
        'read_bytes': 'first'
    }).reset_index()
    agg.columns = ['query', 'median_time', 'min_time', 'max_time', 'read_rows', 'read_bytes']
    print("\n=== Performance Summary ===")
    print(agg.to_string(index=False))


if __name__ == '__main__':
    run_benchmark()