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
    global current_author

    title_label.place_forget()  # タイトルを非表示にする

    selected = random.choice(quotes)
    quote = selected["quote"]
    author = selected["author"]
    source = selected.get("source", "")

    current_author = author

    quote_label.config(text=quote)
    root.update_idletasks()
    quote_height = quote_label.winfo_height()

    # quote_height に応じて base_y を調整（最大50pxまで上へ）
    offset = min((quote_height - 60), 50)
    base_y = 120 - offset if offset > 0 else 120

    quote_label.place(relx=0.5, y=base_y, anchor="n")
    author_label.config(text=f"― {author}")
    author_label.place(relx=0.5, y=base_y + quote_height + 10, anchor="n")

    source_label.config(text=f"{source}")
    source_label.place(relx=0.5, y=base_y + quote_height + 30, anchor="n")

    show_quote_button.place(relx=0.5, y=base_y + quote_height + 70, anchor="n")
    search_button.place(relx=0.5, y=base_y + quote_height + 100, anchor="n")

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
