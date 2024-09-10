import matplotlib.pyplot as plt

# ファイルパスの設定
input_file_path = 'lm_train_line_lengths.txt'
output_image_path = 'line_lengths_plot.png'  # 保存する画像ファイルのパス

# テキストファイルを読み込み、データをグラフ化するプログラム
lines = []
lengths = []

try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # "Line X: Length = Y" というフォーマットから番号と長さを抽出
            parts = line.strip().split(": Length = ")
            if len(parts) == 2:
                line_number = parts[0].strip()
                length = int(parts[1].strip())
                lines.append(line_number)
                lengths.append(length)

    # グラフを作成
    plt.figure(figsize=(10, 6))
    plt.plot(lines, lengths, marker='o', linestyle='-', color='b')

    # グラフのタイトルとラベルを設定
    plt.title('Line Lengths')
    plt.xlabel('Line')
    plt.ylabel('Length')

    # グリッドを表示
    plt.grid(True)

    # x軸のラベルを回転させる
    plt.xticks(rotation=90)

    # グラフを保存
    plt.tight_layout()  # レイアウトを調整
    plt.savefig(output_image_path)

    print(f"The plot has been saved as '{output_image_path}'.")

except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
