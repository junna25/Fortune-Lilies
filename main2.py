import tkinter as tk
import random
import webbrowser
import json
import urllib.parse

# 名言データを読み込み
with open("quotes.json", encoding="utf-8") as f:
    quotes = json.load(f)

# GUI設定
root = tk.Tk()
root.title("Fortune")
root.geometry("500x500")
root.configure(bg="#FFF0F5")
root.resizable(False, False)

# タイトルラベル（少し下に）
title_label = tk.Label(
    root, text="Fortune Lilies", font=("Arial", 30, "bold"), bg="#FFF0F5", fg="#000000"
)
title_label.place(relx=0.5, rely=0.34, anchor="center")

# 名言ラベル
quote_label = tk.Label(
    root, text="", wraplength=490, justify="center",
    font=("Yu Gothic UI", 14, "bold"), bg="#FFF0F5"
)

# 発言者ラベル
author_label = tk.Label(root, text="", fg="blue", cursor="hand2", font=("Arial", 11), bg="#FFF0F5")
author_label.bind("<Button-1>", lambda e: search_author())

# 出典ラベル
source_label = tk.Label(root, text="", font=("Arial", 9), fg="#888888", bg="#FFF0F5")

# 表示ボタン（初期文言）
button = tk.Button(
    root, text="やってみる？", command=lambda: show_quote(),
    bg="#FFFFFF", fg="#000000", font=("Arial", 11)
)
button.place(relx=0.5, rely=0.60, anchor="center")

# Xでシェアボタン
share_button = tk.Button(
    root, text="Xでシェア", command=lambda: share_on_x(),
    bg="#1DA1F2", fg="#FFFFFF", font=("Arial", 11)
)

# 現在の名言と発言者を保存する変数
current_quote = ""
current_author = ""

# 名言表示処理
def show_quote():
    global current_quote, current_author
    title_label.place_forget()

    quote_label.place(relx=0.5, rely=0.3, anchor="center")
    author_label.place(relx=0.5, rely=0.43, anchor="center")
    source_label.place(relx=0.5, rely=0.48, anchor="center")
    button.place(relx=0.5, rely=0.55, anchor="center")
    share_button.place(relx=0.5, rely=0.65, anchor="center")  # シェアボタンを表示

    selected = random.choice(quotes)
    current_quote = selected["quote"]  # 現在の名言を保存
    current_author = selected["author"]  # 現在の発言者を保存
    
    quote_label.config(text=current_quote)
    author_label.config(text=f"— {current_author}")
    author_label.author = current_author

    if "source" in selected:
        source_label.config(text=f"出典：{selected['source']}")
    else:
        source_label.config(text="")

    button.config(text="もう一回！")

# 検索処理
def search_author():
    if hasattr(author_label, "author"):
        query = author_label.author
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

# Xでシェアする処理
def share_on_x():
    if current_quote and current_author:
        # シェアするテキストを作成
        share_text = f'"{current_quote}" — {current_author} #FortuneLilies'
        # URLエンコードしてXのシェアURLを作成
        encoded_text = urllib.parse.quote(share_text)
        x_url = f"https://x.com/intent/tweet?text={encoded_text}"
        # ブラウザでURLを開く
        webbrowser.open(x_url)

# アプリ起動
root.mainloop()
