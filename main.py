import os
import shutil
import pyperclip
import threading
import logging
from pathlib import Path
from tkinter import Tk, Label, Text, Button, filedialog, END, messagebox, Scrollbar
import tkinter.ttk as ttk


# Configure logging
logging.basicConfig(filename="file_copy.log", level=logging.DEBUG, format='%(asctime)s - %(message)s')


class CR2FilterApp:
    def __init__(self, root):
        self.root = root
        root.title("CR2 Image Filter & Copier")
        root.geometry("700x600")

        # --- UI Elements ---
        Label(root, text="Paste Filenames (with or without extension):", font=("Segoe UI", 11)).pack(pady=(10, 0))

        self.text_area = Text(root, height=10, font=("Segoe UI", 10))
        self.text_area.pack(fill="x", padx=20, pady=(0, 10))

        Button(root, text="📋 Paste from Clipboard", command=self.paste_clipboard).pack(pady=5)
        Button(root, text="📂 Select Source Folder", command=self.select_source).pack(pady=5)
        Button(root, text="📁 Select Destination Folder", command=self.select_dest).pack(pady=5)
        Button(root, text="🚀 Copy Matching .cr2 Files", command=self.copy_files).pack(pady=10)

        Label(root, text="Log:", font=("Segoe UI", 11)).pack()
        self.log_area = Text(root, height=10, font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(pady=10)

        # State
        self.source_folder = None
        self.dest_folder = None

    def paste_clipboard(self):
        try:
            clipboard_text = pyperclip.paste()
            if not clipboard_text.strip():
                messagebox.showwarning("Clipboard Empty", "Clipboard is empty. Please copy filenames.")
                return
            self.text_area.delete("1.0", END)
            self.text_area.insert("1.0", clipboard_text)
            logging.info("Pasted clipboard content.")
        except Exception as e:
            messagebox.showerror("Clipboard Error", f"Failed to access clipboard.\n{e}")

    def select_source(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_folder = Path(folder)
            logging.info(f"Source folder selected: {self.source_folder}")
            self.log(f"Source folder selected: {self.source_folder}")

    def select_dest(self):
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_folder = Path(folder)
            logging.info(f"Destination folder selected: {self.dest_folder}")
            self.log(f"Destination folder selected: {self.dest_folder}")

    def copy_files(self):
        if not self.source_folder or not self.dest_folder:
            messagebox.showwarning("Missing Folders", "Please select both source and destination folders.")
            return

        filenames = [line.strip() for line in self.text_area.get("1.0", END).splitlines() if line.strip()]
        if not filenames:
            messagebox.showwarning("No Filenames", "No filenames provided in the clipboard.")
            return

        # Start the progress bar
        self.progress.start()

        # Start the copying process in a separate thread
        threading.Thread(target=self.copy_files_thread, args=(filenames,)).start()

    def copy_files_thread(self, filenames):
        source_files = set(file.name.lower() for file in self.source_folder.glob("*.cr2"))
        copied = 0
        not_found = []

        for name in filenames:
            # If the file has the .cr2 extension, strip it
            if not name.lower().endswith(".cr2"):
                name = f"{name}.cr2"

            file_path = self.source_folder / name.lower()  # Ensure case-insensitivity
            if file_path.name.lower() in source_files:
                try:
                    shutil.copy2(file_path, self.dest_folder)
                    self.log(f"✅ Copied: {file_path.name}")
                    logging.info(f"Copied: {file_path.name}")
                    copied += 1
                except Exception as e:
                    self.log(f"❌ Error copying {file_path.name}: {e}")
                    logging.error(f"Error copying {file_path.name}: {e}")
            else:
                not_found.append(name)

        # Stop the progress bar and show message
        self.progress.stop()
        self.show_results(copied, not_found)

    def show_results(self, copied, not_found):
        if copied:
            messagebox.showinfo("Done", f"{copied} file(s) copied successfully.")
        if not_found:
            messagebox.showwarning("Files Not Found", f"Could not find the following files:\n" + "\n".join(not_found))
        
        # Log results
        logging.info(f"Total files copied: {copied}")
        if not_found:
            logging.warning(f"Files not found: {', '.join(not_found)}")

    def log(self, message):
        self.log_area.insert(END, message + "\n")
        self.log_area.see(END)


# Run the GUI app
if __name__ == "__main__":
    root = Tk()
    app = CR2FilterApp(root)
    root.mainloop()
