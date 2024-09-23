# ファイルパスの設定
input_file_path = 'lm_train_filtered.txt'
output_file_path = 'lm_train_filtered_line_lengths.txt'

# 各行の長さをファイルに書き込むプログラム
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 結果を出力ファイルに書き込む
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for index, line in enumerate(lines):
            line_length = len(line.strip())
            output_file.write(f"Line {index + 1}: Length = {line_length}\n")

    print(f"The lengths of each line have been written to '{output_file_path}'.")

except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
