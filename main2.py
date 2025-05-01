import tkinter as tk
import random
import webbrowser
import json

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
    root, text="", wraplength=460, justify="center",
    font=("Arial", 14, "bold"), bg="#FFF0F5"
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

# 名言表示処理
def show_quote():
    title_label.place_forget()

    quote_label.place(relx=0.5, rely=0.35, anchor="center")
    author_label.place(relx=0.5, rely=0.43, anchor="center")
    source_label.place(relx=0.5, rely=0.48, anchor="center")
    button.place(relx=0.5, rely=0.55, anchor="center")

    selected = random.choice(quotes)
    quote_label.config(text=selected["quote"])
    author_label.config(text=f"— {selected['author']}")
    author_label.author = selected["author"]

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

# アプリ起動
root.mainloop()
