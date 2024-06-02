import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageOps
import os

# Directory to save the images
SAVE_DIR = 'handwriting_samples'
STATE_FILE = 'state.txt'

# Create directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class DataColletor:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwriting Data Collector")
        
        self.is_uppercase = tk.BooleanVar()
        self.inputted_chars = self.load_state()
        self.current_char = self.get_next_char()
        self.grid_size = 6  # 6x6 grid
        self.cell_width = 100
        self.cell_height = 80
        
        self.uppercase_toggle = tk.Checkbutton(root, text="Uppercase", variable=self.is_uppercase, command=self.toggle_case)
        self.uppercase_toggle.pack()

        self.label = tk.Label(root, text=f"Current Character: {self.current_char}")
        self.label.pack()

        self.manual_input_label = tk.Label(root, text="Manual Input:")
        self.manual_input_label.pack()

        self.manual_input_entry = tk.Entry(root)
        self.manual_input_entry.pack()

        self.manual_input_button = tk.Button(root, text="Set Character", command=self.set_manual_character)
        self.manual_input_button.pack()

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=480, bg='white')
        self.canvas.pack()
        
        self.label_instruction = tk.Label(root, text="WRITE SAMPLE")
        self.label_instruction.pack()

        self.draw_grid()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_and_increment_character)
        self.save_button.pack(side=tk.LEFT)

        # self.sanitize_button = tk.Button(self.button_frame, text="Sanitize", command=self.sanitize_images)
        # self.sanitize_button.pack(side=tk.LEFT)

        self.canvas.bind("<B1-Motion>", self.paint)

        self.image = Image.new("RGB", (600, 480), "white")
        self.draw = ImageDraw.Draw(self.image)

    def draw_grid(self):
        for i in range(self.grid_size + 1):
            self.canvas.create_line(0, i*self.cell_height, 600, i*self.cell_height, fill='orange')
            self.canvas.create_line(i*self.cell_width, 0, i*self.cell_width, 480, fill='orange')

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="purple", width=5)
        self.draw.line([x1, y1, x2, y2], fill="purple", width=5)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.image = Image.new("RGB", (600, 480), "white")
        self.draw = ImageDraw.Draw(self.image)

    def is_cell_empty(self, cell_image):
        # Convert the image to grayscale
        gray_image = ImageOps.grayscale(cell_image)
        # Get the histogram of the grayscale image
        hist = gray_image.histogram()
        # Calculate the number of white pixels (intensity 255)
        white_pixels = hist[255]
        # Calculate the total number of pixels
        total_pixels = self.cell_width * self.cell_height
        # Determine if the image is mostly white
        return white_pixels / total_pixels > 0.99

    def save_image(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0, y0 = j*self.cell_width, i*self.cell_height
                x1, y1 = (j+1)*self.cell_width, (i+1)*self.cell_height
                cell_image = self.image.crop((x0, y0, x1, y1))
                
                # Check if the cell is not empty
                if not self.is_cell_empty(cell_image):
                    save_path = f'{SAVE_DIR}/{self.current_char}'
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    
                    cell_count = len(os.listdir(save_path))
                    cell_image.save(f"{save_path}/{self.current_char}_{cell_count + 1}.png")

    def save_and_increment_character(self):
        self.save_image()
        self.inputted_chars.add(self.current_char)
        self.save_state()
        self.current_char = self.get_next_char()
        self.clear_canvas()
        self.label.config(text=f"Current Character: {self.current_char}")

    def get_next_char(self):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char not in self.inputted_chars:
                return char
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if char not in self.inputted_chars:
                return char
        return 'a'

    def toggle_case(self):
        if not self.all_lowercase_inputted() and self.is_uppercase.get():
            messagebox.showerror("Error", "Please input all lowercase letters first.")
            self.is_uppercase.set(False)
            return
        self.current_char = self.get_next_char()
        self.label.config(text=f"Current Character: {self.current_char}")

    def all_lowercase_inputted(self):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char not in self.inputted_chars:
                return False
        return True

    def set_manual_character(self):
        manual_char = self.manual_input_entry.get()
        if manual_char and len(manual_char) == 1 and manual_char.isalpha():
            if manual_char.isupper() and not self.all_lowercase_inputted():
                messagebox.showerror("Error", "Please input all lowercase letters first.")
                return
            self.current_char = manual_char
            self.label.config(text=f"Current Character: {self.current_char}")
            self.inputted_chars.add(manual_char)
            self.save_state()
        else:
            messagebox.showerror("Error", "Please enter a single alphabet character.")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = DataColletor(root)
    root.mainloop()
