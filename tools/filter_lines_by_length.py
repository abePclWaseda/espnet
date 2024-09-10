# ファイルパスの設定
input_file_path = 'lm_train_sorted.txt'
output_file_path = 'lm_train_filtered.txt'  # フィルタリングした後の元のテキストを記録する新しいファイル

# 各行の長さをフィルタリングして元のテキストをファイルに書き込むプログラム
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # フィルタリングした行を出力ファイルに書き込む（長さが4000以下のもののみ）
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in lines:
            line_length = len(line.strip())
            if line_length <= 4000:  # 長さが4000以下のものをフィルタリング
                output_file.write(line)

    print(f"Lines with 4000 or fewer characters have been written to '{output_file_path}'.")

except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
