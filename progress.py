import tkinter as tk
import os
import subprocess

# Directory to save the images
SAVE_DIR = 'handwriting_samples'

class ProgressData:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.setup_ui()

    def setup_ui(self):
        self.title = tk.Label(self.root, text="Progress and Collected Data", font=("Helvetica", 16))
        self.title.pack(pady=20)

        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack()

        self.draw_main_menu()

        self.back_button = tk.Button(self.root, text="Back", command=self.back_callback)
        self.back_button.pack(pady=10)

    def draw_main_menu(self):
        buttons = [
            ("Single Lowercase", self.open_single_lowercase),
            ("Single Uppercase", self.open_single_uppercase),
            ("Bi-Lowercase", self.open_bi_lowercase),
            ("Bi-Mixedcase", self.open_bi_mixedcase),
        ]
        for i, (text, command) in enumerate(buttons):
            button = tk.Button(self.progress_frame, text=text, command=command)
            button.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

    def open_single_lowercase(self):
        self.clear_window()
        CharacterProgress(self.root, self.back_callback, 'single_lowercase', 'abcdefghijklmnopqrstuvwxyz')

    def open_single_uppercase(self):
        self.clear_window()
        CharacterProgress(self.root, self.back_callback, 'single_uppercase', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def open_bi_lowercase(self):
        self.clear_window()
        BiCharacterProgress(self.root, self.back_callback, 'bi_lowercase')

    def open_bi_mixedcase(self):
        self.clear_window()
        BiCharacterProgress(self.root, self.back_callback, 'bi_mixedcase')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class CharacterProgress:
    def __init__(self, root, back_callback, char_type, chars):
        self.root = root
        self.back_callback = back_callback
        self.char_type = char_type
        self.chars = chars

        self.setup_ui()

    def setup_ui(self):
        self.title = tk.Label(self.root, text=f"Progress: {self.char_type.replace('_', ' ').title()}", font=("Helvetica", 16))
        self.title.pack(pady=20)

        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack()

        self.draw_progress_table()

        self.back_button = tk.Button(self.root, text="Back", command=self.back_callback)
        self.back_button.pack(pady=10)

    def draw_progress_table(self):
        for i, char in enumerate(self.chars):
            count = self.get_sample_count(char)
            color = self.get_color_based_on_count(count)
            button = tk.Button(self.progress_frame, text=f"{char}: {count}", bg=color, command=lambda c=char: self.open_folder(c))
            button.grid(row=i // 4, column=i % 4, padx=10, pady=5, sticky="ew")

    def get_sample_count(self, char):
        char_path = os.path.join(SAVE_DIR, self.char_type, char)
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
        char_path = os.path.join(SAVE_DIR, self.char_type, char)
        if os.path.exists(char_path) and os.listdir(char_path):
            if os.name == 'nt':  # Windows
                os.startfile(char_path)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.call(['open', char_path])
        else:
            tk.messagebox.showinfo("No Data", f"No data found for character '{char}'")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class BiCharacterProgress:
    def __init__(self, root, back_callback, char_type):
        self.root = root
        self.back_callback = back_callback
        self.char_type = char_type

        self.setup_ui()

    def setup_ui(self):
        self.title = tk.Label(self.root, text=f"Bi-Character Progress: {self.char_type.replace('_', ' ').title()}", font=("Helvetica", 16))
        self.title.pack(pady=20)

        self.bi_char_frame = tk.Frame(self.root)
        self.bi_char_frame.pack()

        self.draw_bi_char_table()

        self.back_button = tk.Button(self.root, text="Back", command=self.back_callback)
        self.back_button.pack(pady=10)

    def draw_bi_char_table(self):
        alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, char in enumerate(alphabets):
            button = tk.Button(self.bi_char_frame, text=char, command=lambda c=char: self.open_bi_char_subtable(c))
            button.grid(row=i // 4, column=i % 4, padx=10, pady=5, sticky="ew")

    def open_bi_char_subtable(self, char):
        self.clear_window()
        BiCharacterSubProgress(self.root, self.back_callback, self.char_type, char)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class BiCharacterSubProgress:
    def __init__(self, root, back_callback, char_type, parent_char):
        self.root = root
        self.back_callback = back_callback
        self.char_type = char_type
        self.parent_char = parent_char

        self.setup_ui()

    def setup_ui(self):
        self.title = tk.Label(self.root, text=f"Bi-Character Progress: {self.parent_char} ({self.char_type.replace('_', ' ').title()})", font=("Helvetica", 16))
        self.title.pack(pady=20)

        self.bi_char_frame = tk.Frame(self.root)
        self.bi_char_frame.pack()

        self.draw_bi_char_subtable()

        self.back_button = tk.Button(self.root, text="Back", command=self.back_callback)
        self.back_button.pack(pady=10)

    def draw_bi_char_subtable(self):
        alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
        for i, char in enumerate(alphabet_lower):
            bi_char = self.parent_char + char if self.char_type == 'bi_mixedcase' else self.parent_char.lower() + char
            count = self.get_sample_count(bi_char)
            color = self.get_color_based_on_count(count)
            button = tk.Button(self.bi_char_frame, text=f"{bi_char}: {count}", bg=color, command=lambda c=bi_char: self.open_folder(c))
            button.grid(row=i // 4, column=i % 4, padx=10, pady=5, sticky="ew")

    def get_sample_count(self, char):
        char_path = os.path.join(SAVE_DIR, self.char_type, char)
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
        char_path = os.path.join(SAVE_DIR, self.char_type, char)
        if os.path.exists(char_path) and os.listdir(char_path):
            if os.name == 'nt':  # Windows
                os.startfile(char_path)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.call(['open', char_path])
        else:
            tk.messagebox.showinfo("No Data", f"No data found for character '{char}'")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# This script is intended to be imported as a module in main.py
