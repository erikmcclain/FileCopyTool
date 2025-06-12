from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import json
from pathlib import Path

APP_NAME = "LSCopyTool"
HISTORY_FILE = Path(os.getenv('APPDATA')) / APP_NAME / "folder_history.json"
MAX_HISTORY = 10

def ensure_appdata():
    if not HISTORY_FILE.parent.exists():
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_history():
    ensure_appdata()
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {"source": [], "destination": []}

def save_history():
    ensure_appdata()
    with open(HISTORY_FILE, 'w') as f:
        json.dump(folder_history, f)

def update_history(key, new_path):
    if new_path in folder_history[key]:
        folder_history[key].remove(new_path)
    folder_history[key].insert(0, new_path)
    folder_history[key] = folder_history[key][:MAX_HISTORY]
    save_history()
    refresh_dropdowns()

def select_folder(key, var):
    folder = filedialog.askdirectory()
    if folder:
        var.set(folder)
        update_history(key, folder)

def handle_drop(event, var, key):
    path = event.data.strip().strip('{}').split()[0]
    if os.path.isdir(path):
        var.set(path)
        update_history(key, path)

def refresh_dropdowns():
    source_menu['menu'].delete(0, 'end')
    dest_menu['menu'].delete(0, 'end')
    for s in folder_history["source"]:
        source_menu['menu'].add_command(label=s, command=tk._setit(source_var, s))
    for d in folder_history["destination"]:
        dest_menu['menu'].add_command(label=d, command=tk._setit(destination_var, d))

def copy_and_filter():
    source = source_var.get()
    destination = destination_var.get()
    extensions = [ext.strip().lower() for ext in extension_var.get().split(',')]
    keywords = [kw.strip() for kw in keyword_var.get().split(',') if kw.strip()]
    delete_enabled = delete_var.get()
    preview_mode = preview_var.get()

    if not source or not destination:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return

    update_history("source", source)
    update_history("destination", destination)

    if not os.path.exists(destination):
        os.makedirs(destination)

    copied = []
    deleted = []

    for filename in os.listdir(source):
        if any(filename.lower().endswith(ext) for ext in extensions):
            src_path = os.path.join(source, filename)
            dst_path = os.path.join(destination, filename)
            shutil.copy2(src_path, dst_path)
            copied.append(filename)

    if delete_enabled:
        for filename in os.listdir(destination):
            for keyword in keywords:
                if keyword in filename:
                    deleted.append(filename)
                    if not preview_mode:
                        os.remove(os.path.join(destination, filename))
                    break

    result_text = f"Copied {len(copied)} file(s):\n" + "\n".join(copied) + "\n\n"
    if delete_enabled:
        if preview_mode:
            result_text += f"Preview: {len(deleted)} file(s) would be deleted:\n" + "\n".join(deleted)
        else:
            result_text += f"Deleted {len(deleted)} file(s):\n" + "\n".join(deleted)
    else:
        result_text += "(Deletion step was skipped)"

    result_box.config(state='normal')
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, result_text)
    result_box.config(state='disabled')

folder_history = load_history()

root = TkinterDnD.Tk()
root.title("Copy and Filter Files with Drag-and-Drop, History, and Preview")

source_var = tk.StringVar(value=folder_history["source"][0] if folder_history["source"] else "")
destination_var = tk.StringVar(value=folder_history["destination"][0] if folder_history["destination"] else "")
extension_var = tk.StringVar(value=".ls")
keyword_var = tk.StringVar()
delete_var = tk.BooleanVar(value=True)
preview_var = tk.BooleanVar(value=False)

tk.Label(root, text="Source Folder:").grid(row=0, column=0, sticky='e')
source_menu = ttk.OptionMenu(root, source_var, source_var.get(), *folder_history["source"])
source_menu.grid(row=0, column=1, sticky='ew')
tk.Button(root, text="Browse", command=lambda: select_folder("source", source_var)).grid(row=0, column=2)
source_menu.bind('<<Drop>>', lambda e: handle_drop(e, source_var, "source"))

tk.Label(root, text="Destination Folder:").grid(row=1, column=0, sticky='e')
dest_menu = ttk.OptionMenu(root, destination_var, destination_var.get(), *folder_history["destination"])
dest_menu.grid(row=1, column=1, sticky='ew')
tk.Button(root, text="Browse", command=lambda: select_folder("destination", destination_var)).grid(row=1, column=2)
dest_menu.bind('<<Drop>>', lambda e: handle_drop(e, destination_var, "destination"))

tk.Label(root, text="File extensions to copy (comma-separated):").grid(row=2, column=0, sticky='e')
tk.Entry(root, textvariable=extension_var, width=50).grid(row=2, column=1, columnspan=2)

tk.Label(root, text="Delete if name contains (comma-separated):").grid(row=3, column=0, sticky='e')
tk.Entry(root, textvariable=keyword_var, width=50).grid(row=3, column=1, columnspan=2)

tk.Checkbutton(root, text="Enable deletion step", variable=delete_var).grid(row=4, column=1, sticky='w')
tk.Checkbutton(root, text="Preview deletions (don't delete)", variable=preview_var).grid(row=4, column=2, sticky='w')

tk.Button(root, text="Copy and Filter Files", command=copy_and_filter).grid(row=5, column=0, columnspan=3, pady=10)

result_box = tk.Text(root, height=15, width=80, state='disabled')
result_box.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

refresh_dropdowns()
root.mainloop()
