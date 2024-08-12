import subprocess
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt

# ログファイルのパスを指定
log_file = 'gpu_usage_log.csv'
graph_file = 'gpu_memory_usage_plot.png'

# ログファイルのヘッダーを書き込み
with open(log_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'GPU ID', 'Memory Used (MiB)'])

# nvidia-smi コマンドを実行して GPU のメモリ使用量を取得
def get_gpu_memory_usage():
    utilization_result = subprocess.run(['nvidia-smi', '--query-gpu=index,memory.used', '--format=csv,noheader,nounits'],
                                        stdout=subprocess.PIPE, text=True)
    utilization_lines = utilization_result.stdout.strip().split('\n')
    
    gpu_data = []
    
    for line in utilization_lines:
        data = line.split(',')
        gpu_id = data[0].strip()
        memory_used = data[1].strip()
        gpu_data.append([gpu_id, memory_used])
    
    return gpu_data

# メモリ使用量を時間ごとにログに記録し、プロット
def log_and_plot_gpu_memory_usage(interval=60):
    timestamps = []
    memory_usage = []

    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gpu_data = get_gpu_memory_usage()

        # ログファイルに書き込み
        with open(log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for data in gpu_data:
                writer.writerow([timestamp] + data)

        # データをリストに保存（ここでは最初のGPUのみをプロット）
        timestamps.append(timestamp)
        memory_usage.append(float(gpu_data[0][1]))  # 最初のGPUのメモリ使用量を使用

        # プロットを更新
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, memory_usage, marker='o')
        plt.title('GPU Memory Usage Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Memory Used (MiB)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # グラフを保存
        plt.savefig(graph_file)

        # 指定された間隔で待機
        time.sleep(interval)

if __name__ == '__main__':
    log_and_plot_gpu_memory_usage(interval=20)  # 60秒ごとにログとプロットを更新
