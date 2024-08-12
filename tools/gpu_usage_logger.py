import subprocess
import time
import csv
from datetime import datetime

# ログファイルのパスを指定
log_file = 'gpu_usage_log.csv'

# ログファイルのヘッダーを書き込み
with open(log_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'GPU Utilization (%)', 'Memory Utilization (%)'])

# nvidia-smi コマンドを実行して GPU の使用率を取得
def get_gpu_usage():
    result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,utilization.memory', '--format=csv,noheader,nounits'],
                            stdout=subprocess.PIPE, text=True)
    usage = result.stdout.strip().split(',')
    gpu_utilization = usage[0].strip()
    memory_utilization = usage[1].strip()
    return gpu_utilization, memory_utilization

# 定期的にGPU使用率をログに記録
def log_gpu_usage(interval=60):
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gpu_utilization, memory_utilization = get_gpu_usage()

        # ログファイルに書き込み
        with open(log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, gpu_utilization, memory_utilization])

        # 指定された間隔で待機
        time.sleep(interval)

if __name__ == '__main__':
    log_gpu_usage(interval=10)  # 10秒ごとにログを記録
