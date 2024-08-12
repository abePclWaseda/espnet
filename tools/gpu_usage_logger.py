import subprocess
import time
import csv
from datetime import datetime

# ログファイルのパスを指定
log_file = 'gpu_usage_log.csv'

# ログファイルのヘッダーを書き込み
with open(log_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'GPU ID', 'GPU Utilization (%)', 'Memory Utilization (%)', 'Memory Used (MiB)', 'Memory Capacity (MiB)'])

# nvidia-smi コマンドを実行して GPU の使用率、メモリの使用率、メモリの使用量、総容量を取得
def get_gpu_usage_and_memory():
    # GPU ID, GPU の使用率とメモリ使用率を取得
    utilization_result = subprocess.run(['nvidia-smi', '--query-gpu=index,utilization.gpu,utilization.memory', '--format=csv,noheader,nounits'],
                                        stdout=subprocess.PIPE, text=True)
    utilization_lines = utilization_result.stdout.strip().split('\n')
    
    gpu_data = []
    
    for line in utilization_lines:
        data = line.split(',')
        gpu_id = data[0].strip()
        gpu_utilization = data[1].strip()
        memory_utilization = data[2].strip()
        
        # GPU メモリの使用量と総容量を取得
        memory_result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits', '--id={}'.format(gpu_id)],
                                       stdout=subprocess.PIPE, text=True)
        memory = memory_result.stdout.strip().split(',')
        memory_used = memory[0].strip()
        memory_capacity = memory[1].strip()
        
        gpu_data.append([gpu_id, gpu_utilization, memory_utilization, memory_used, memory_capacity])
    
    return gpu_data

# 定期的にGPU使用率とメモリ情報をログに記録
def log_gpu_usage(interval=60):
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gpu_data = get_gpu_usage_and_memory()
        
        # ログファイルに書き込み
        with open(log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for data in gpu_data:
                writer.writerow([timestamp] + data)

        # 指定された間隔で待機
        time.sleep(interval)

if __name__ == '__main__':
    log_gpu_usage(interval=30)  # 30秒ごとにログを記録
