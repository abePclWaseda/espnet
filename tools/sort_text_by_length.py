# ファイルパスを指定
file_path = 'egs2/librispeech_100/asr1/dump/raw/lm_train.txt'
output_file_path = 'lm_train_sorted.txt'

# ファイルを開き、すべての行をリストとして読み込む
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 各行の長さでソート（降順）
sorted_lines = sorted(lines, key=lambda x: len(x.strip()), reverse=True)

# ソートされた結果を新しいファイルに書き込む
with open(output_file_path, 'w', encoding='utf-8') as file:
    for line in sorted_lines:
        file.write(line)