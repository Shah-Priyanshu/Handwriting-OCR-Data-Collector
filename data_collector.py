import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageOps
import os

# Directory to save the images
SAVE_DIR = 'handwriting_samples'
STATE_FILE = 'state.txt'

# Create directories if they don't exist
folders = ['single_lowercase', 'single_uppercase', 'bi_lowercase', 'bi_mixedcase']
for folder in folders:
    folder_path = os.path.join(SAVE_DIR, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

class DataCollector:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.grid_size = 6  # 6x6 grid
        self.cell_width = 100
        self.cell_height = 80
        
        self.is_erasing = tk.BooleanVar()
        self.inputted_chars = self.load_state()
        self.current_char = self.get_next_char()
        self.pen_size = 5
        
        self.setup_ui()
        
        self.image = Image.new("RGB", (600, 480), "white")
        self.draw = ImageDraw.Draw(self.image)

    def setup_ui(self):
        self.title = tk.Label(self.root, text="Data Collector", font=("Helvetica", 16))
        self.title.pack(pady=20)

        self.eraser_toggle = tk.Checkbutton(self.root, text="Eraser", variable=self.is_erasing, command=self.toggle_eraser)
        self.eraser_toggle.pack()

        self.label = tk.Label(self.root, text=f"Current Character: {self.current_char}")
        self.label.pack()

        self.manual_input_label = tk.Label(self.root, text="Manual Input:")
        self.manual_input_label.pack()

        self.manual_input_entry = tk.Entry(self.root)
        self.manual_input_entry.pack()

        self.manual_input_button = tk.Button(self.root, text="Set Character", command=self.set_manual_character)
        self.manual_input_button.pack()

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()

        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=480, bg='white')
        self.canvas.pack(side=tk.LEFT)
        
        self.label_instruction = tk.Label(self.root, text="WRITE SAMPLES")
        self.label_instruction.pack()

        self.draw_grid()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_and_increment_character)
        self.save_button.pack(side=tk.LEFT)

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.back_callback)
        self.back_button.pack(side=tk.LEFT)

        self.canvas.bind("<B1-Motion>", self.paint_or_erase)

    def draw_grid(self):
        for i in range(self.grid_size + 1):
            self.canvas.create_line(0, i*self.cell_height, 600, i*self.cell_height, fill='orange')
            self.canvas.create_line(i*self.cell_width, 0, i*self.cell_width, 480, fill='orange')

    def paint_or_erase(self, event):
        self.update_pen_size(event.y)
        if self.is_erasing.get():
            self.erase(event)
        else:
            self.paint(event)

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="purple", width=self.pen_size)
        self.draw.line([x1, y1, x2, y2], fill="purple", width=self.pen_size)

    def erase(self, event):
        col = event.x // self.cell_width
        row = event.y // self.cell_height
        x0, y0 = col * self.cell_width, row * self.cell_height
        x1, y1 = (col + 1) * self.cell_width, (row + 1) * self.cell_height
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="orange")
        self.draw.rectangle([x0, y0, x1, y1], fill="white")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.image = Image.new("RGB", (600, 480), "white")
        self.draw = ImageDraw.Draw(self.image)

    def is_cell_empty(self, cell_image):
        gray_image = ImageOps.grayscale(cell_image)
        pixel_data = list(gray_image.getdata())
        total_pixels = cell_image.width * cell_image.height
        sum_pixel_values = sum(pixel_data)
        sum_white_pixels = 255 * total_pixels
        return sum_pixel_values == sum_white_pixels

    def save_image(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0, y0 = j*self.cell_width, i*self.cell_height
                x1, y1 = (j+1)*self.cell_width, (i+1)*self.cell_height
                cell_image = self.image.crop((x0, y0, x1, y1))
                
                if not self.is_cell_empty(cell_image):
                    folder_name = self.get_folder_name()
                    save_path = os.path.join(SAVE_DIR, folder_name, self.current_char)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    
                    cell_count = len(os.listdir(save_path))
                    cell_image.save(f"{save_path}/{self.current_char}_{cell_count + 1}.png")

    def get_folder_name(self):
        if len(self.current_char) == 1:
            if self.current_char.islower():
                return 'single_lowercase'
            elif self.current_char.isupper():
                return 'single_uppercase'
        elif len(self.current_char) == 2:
            if self.current_char.islower():
                return 'bi_lowercase'
            elif self.current_char[0].isupper() and self.current_char[1].islower():
                return 'bi_mixedcase'
        return 'unknown'

    def save_and_increment_character(self):
        self.save_image()
        self.inputted_chars.add(self.current_char)
        self.save_state()
        self.current_char = self.get_next_char()
        self.clear_canvas()
        self.label.config(text=f"Current Character: {self.current_char}")

    def get_next_char(self):
        alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
        alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for char in alphabet_lower:
            if char not in self.inputted_chars:
                return char
        for char in alphabet_upper:
            if char not in self.inputted_chars:
                return char
        for char1 in alphabet_lower:
            for char2 in alphabet_lower:
                bi_char = char1 + char2
                if bi_char not in self.inputted_chars:
                    return bi_char
        for char1 in alphabet_upper:
            for char2 in alphabet_lower:
                bi_char = char1 + char2
                if bi_char not in self.inputted_chars:
                    return bi_char
        return 'a'

    def toggle_eraser(self):
        if self.is_erasing.get():
            self.canvas.config(cursor="dotbox")
        else:
            self.canvas.config(cursor="pencil")

    def set_manual_character(self):
        manual_char = self.manual_input_entry.get()
        if manual_char and len(manual_char) == 1 and manual_char.isalpha():
            self.current_char = manual_char
            self.label.config(text=f"Current Character: {self.current_char}")
            self.inputted_chars.add(manual_char)
            self.save_state()
        elif manual_char and len(manual_char) == 2 and ((manual_char[0].islower() and manual_char[1].islower()) or (manual_char[0].isupper() and manual_char[1].islower())):
            self.current_char = manual_char
            self.label.config(text=f"Current Character: {self.current_char}")
            self.inputted_chars.add(manual_char)
            self.save_state()
        else:
            messagebox.showerror("Error", "Please enter a valid character (single or bi-character).")

    def update_pen_size(self, y):
        row = y // self.cell_height
        self.pen_size = max(1, row)

    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as file:
                return set(file.read().strip().split())
        return set()

    def save_state(self):
        with open(STATE_FILE, 'w') as file:
            file.write(' '.join(sorted(self.inputted_chars)))

    def sanitize_images(self):
        for root, dirs, files in os.walk(SAVE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                image = Image.open(file_path)
                if self.is_cell_empty(image):
                    os.remove(file_path)
                    print(f"Removed empty image: {file_path}")
                else:
                    print(f"Kept non-empty image: {file_path}")