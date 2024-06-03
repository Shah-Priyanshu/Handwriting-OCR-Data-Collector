import tkinter as tk
import os
import subprocess

# Directory to save the images
SAVE_DIR = 'handwriting_samples'

class CombinedProgressData:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.setup_ui()

    def setup_ui(self):
        self.title = tk.Label(self.root, text="Progress and Collected Data", font=("Helvetica", 16))
        self.title.pack(pady=20)

        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack()

        self.draw_progress_table()

        self.back_button = tk.Button(self.root, text="Back", command=self.back_callback)
        self.back_button.pack(pady=10)

    def draw_progress_table(self):
        alphabets = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, char in enumerate(alphabets):
            count = self.get_sample_count(char)
            color = self.get_color_based_on_count(count)
            button = tk.Button(self.progress_frame, text=f"{char}: {count}", bg=color, command=lambda c=char: self.open_folder(c))
            button.grid(row=i // 4, column=i % 4, padx=10, pady=5, sticky="ew")

    def get_sample_count(self, char):
        folder_name = "uppercase" if char.isupper() else "lowercase"
        char_path = os.path.join(SAVE_DIR, folder_name, char)
        if os.path.exists(char_path):
            return len(os.listdir(char_path))
        return 0

    def get_color_based_on_count(self, count):
        if count < 18:
            return "red"
        elif 18 <= count <= 35:
            return "yellow"
        else:
            return "green"

    def open_folder(self, char):
        folder_name = "uppercase" if char.isupper() else "lowercase"
        char_path = os.path.join(SAVE_DIR, folder_name, char)
        if os.path.exists(char_path) and os.listdir(char_path):
            if os.name == 'nt':  # Windows
                os.startfile(char_path)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.call(['open', char_path])
        else:
            tk.messagebox.showinfo("No Data", f"No data found for character '{char}'")

# This script is intended to be imported as a module in main.py
