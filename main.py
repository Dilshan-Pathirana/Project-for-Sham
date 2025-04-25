import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pyperclip

def get_clipboard_text():
    return pyperclip.paste()

def browse_source_folder():
    folder = filedialog.askdirectory(title="Select Source Folder")
    if folder:
        source_var.set(folder)

def browse_destination_folder():
    folder = filedialog.askdirectory(title="Select Destination Folder")
    if folder:
        destination_var.set(folder)

def start_filtering():
    source = source_var.get()
    dest = destination_var.get()
    filenames_text = text_input.get("1.0", tk.END).strip()

    if not source or not dest or not filenames_text:
        messagebox.showerror("Missing Information", "Please fill in all fields.")
        return

    filenames = {f.strip() for f in filenames_text.splitlines() if f.strip()}
    found = 0
    copied = 0

    try:
        for file in os.listdir(source):
            file_path = os.path.join(source, file)
            name = os.path.splitext(file)[0]
            if file.endswith('.cr2') and (file in filenames or name in filenames):
                shutil.copy(file_path, dest)
                copied += 1
        messagebox.showinfo("Success", f"{copied} image(s) copied successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("PUPA v1.0 by Dilshan")
root.geometry("600x500")
root.resizable(False, False)

# Fonts and Colors
FONT = ("Segoe UI", 10)

# Source folder
tk.Label(root, text="Source Folder:", font=FONT).pack(pady=(10, 0))
source_frame = tk.Frame(root)
source_frame.pack(padx=10, fill="x")
source_var = tk.StringVar()
tk.Entry(source_frame, textvariable=source_var, font=FONT).pack(side="left", fill="x", expand=True)
tk.Button(source_frame, text="Browse", command=browse_source_folder).pack(side="right", padx=5)

# Destination folder
tk.Label(root, text="Destination Folder:", font=FONT).pack(pady=(10, 0))
dest_frame = tk.Frame(root)
dest_frame.pack(padx=10, fill="x")
destination_var = tk.StringVar()
tk.Entry(dest_frame, textvariable=destination_var, font=FONT).pack(side="left", fill="x", expand=True)
tk.Button(dest_frame, text="Browse", command=browse_destination_folder).pack(side="right", padx=5)

# Clipboard area
tk.Label(root, text="Paste Filenames (from clipboard):", font=FONT).pack(pady=(10, 0))
text_input = scrolledtext.ScrolledText(root, height=10, font=FONT)
text_input.pack(padx=10, pady=5, fill="both", expand=True)

# Paste from clipboard button
tk.Button(root, text="Paste from Clipboard", command=lambda: text_input.insert(tk.END, get_clipboard_text())).pack(pady=5)

# Start button
tk.Button(root, text="Copy Matching Images", command=start_filtering, height=2, bg="#2e8b57", fg="white", font=("Segoe UI", 11, "bold")).pack(pady=10)

root.mainloop()
