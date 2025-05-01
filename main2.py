from tkinter import ttk
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
root.title("Fortune Lilies")
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
    bg="#000000", fg="#FFFFFF", font=("Arial", 11)
)

# 現在の名言と発言者を保存する変数
current_quote = ""
current_author = ""

# 名言収集処理
def save_to_library(quote_obj):
    try:
        with open("library.json", "r", encoding="utf-8") as f:
            library = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        library = []

    if quote_obj not in library:
        library.append(quote_obj)
        with open("library.json", "w", encoding="utf-8") as f:
            json.dump(library, f, ensure_ascii=False, indent=2)

def open_library():
    # データ読み込み
    try:
        with open("quotes.json", "r", encoding="utf-8") as f:
            all_quotes = json.load(f)
        try:
            with open("library.json", "r", encoding="utf-8") as f:
                collected = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            collected = []
    except Exception as e:
        messagebox.showerror("エラー", f"ライブラリの読み込みに失敗しました\n{str(e)}")
        return

    # 発言者・出典リスト作成（"すべて"を先頭に追加）
    authors = sorted(set(item["author"] for item in all_quotes))
    authors.insert(0, "All")

    sources = sorted(set(item.get("source", "不明") for item in all_quotes))
    sources.insert(0, "All")

    # ポップアップウィンドウ
    popup = tk.Toplevel(root)
    popup.title("ライブラリ")
    popup.geometry("520x450")
    popup.configure(bg="#FFF0F5")

    # テキスト表示
    text_widget = tk.Text(popup, wrap="word", font=("Arial", 11), bg="#FFF0F5", borderwidth=0)
    text_widget.pack(expand=True, fill="both", padx=10, pady=(80, 10))

    # 絞り込み状態
    selected_author = tk.StringVar(value=authors[0])
    selected_source = tk.StringVar(value=sources[0])

    # 表示更新関数
    def update_display(*args):
        author_filter = selected_author.get()
        source_filter = selected_source.get()

        filtered = []
        for q in all_quotes:
            if (author_filter != "All" and q["author"] != author_filter):
                continue
            if (source_filter != "All" and q.get("source", "不明") != source_filter):
                continue
            filtered.append(q)

        collected_set = set((c["quote"], c["author"]) for c in collected)

        lines = []
        for q in filtered:
            if (q["quote"], q["author"]) in collected_set:
                line = f"{q['quote']}\n― {q['author']}"
            else:
                line = f"？？？\n― {q['author']}"
            lines.append(line)

        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", "\n\n".join(lines) if lines else "該当なし")
        text_widget.config(state="disabled")

    # プルダウン（Combobox）設置
    from tkinter import ttk

    ttk.Label(popup, text="発言者：", background="#FFF0F5").place(x=10, y=10)
    author_combo = ttk.Combobox(popup, textvariable=selected_author, values=authors, state="readonly", font=("Arial", 10), width=25)
    author_combo.place(x=70, y=10)
    author_combo.bind("<<ComboboxSelected>>", update_display)

    ttk.Label(popup, text="出典：", background="#FFF0F5").place(x=10, y=40)
    source_combo = ttk.Combobox(popup, textvariable=selected_source, values=sources, state="readonly", font=("Arial", 10), width=25)
    source_combo.place(x=70, y=40)
    source_combo.bind("<<ComboboxSelected>>", update_display)

    update_display()  # 初期表示
    
# 名言表示処理
def show_quote():
    global current_quote, current_author
    title_label.place_forget()

    quote_label.place(relx=0.5, rely=0.28, anchor="center")
    author_label.place(relx=0.5, rely=0.43, anchor="center")
    source_label.place(relx=0.5, rely=0.48, anchor="center")
    button.place(relx=0.5, rely=0.55, anchor="center")
    share_button.place(relx=0.5, rely=0.65, anchor="center")  # シェアボタンを表示

    selected = random.choice(quotes)
    save_to_library(selected)
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

library_button = tk.Button(root, text="ライブラリを見る", command=open_library, bg="#FFFFFF", fg="#000000", font=("Arial", 10))
library_button.place(relx=0.95, rely=0.95, anchor="se")  # 画面右下に配置


# アプリ起動
root.mainloop()
