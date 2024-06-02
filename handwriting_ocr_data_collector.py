import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw
import os
import string

# Create a directory to save the images
if not os.path.exists('handwriting_samples'):
    os.makedirs('handwriting_samples')

class DataColletor:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwriting Data Collector")
        
        self.is_uppercase = tk.BooleanVar()
        self.current_char = 'a'
        self.cell_counter = 0
        self.grid_size = 6  # 6x6 grid
        self.cell_width = 100
        self.cell_height = 80
        
        self.uppercase_toggle = tk.Checkbutton(root, text="Uppercase", variable=self.is_uppercase, command=self.update_case)
        self.uppercase_toggle.pack()

        self.label = tk.Label(root, text=f"Current Character: {self.current_char}")
        self.label.pack()

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=400, bg='white')
        self.canvas.pack()
        
        self.label_instruction = tk.Label(root, text="WRITE SAMPLE")
        self.label_instruction.pack()

        self.draw_grid()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)

        self.canvas.bind("<B1-Motion>", self.paint)

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def draw_grid(self):
        for i in range(self.grid_size + 1):
            self.canvas.create_line(0, i*self.cell_height, 600, i*self.cell_height, fill='orange')
            self.canvas.create_line(i*self.cell_width, 0, i*self.cell_width, 400, fill='orange')

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="purple", width=5)
        self.draw.line([x1, y1, x2, y2], fill="purple", width=5)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.cell_counter = 0
        self.increment_character()
        self.label.config(text=f"Current Character: {self.current_char}")

    def save_image(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0, y0 = j*self.cell_width, i*self.cell_height
                x1, y1 = (j+1)*self.cell_width, (i+1)*self.cell_height
                cell_image = self.image.crop((x0, y0, x1, y1))
                
                save_path = f'handwriting_samples/{self.current_char}'
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                
                cell_count = len(os.listdir(save_path))
                cell_image.save(f"{save_path}/{self.current_char}_{cell_count + 1}.png")
        
        self.clear_canvas()

    def increment_character(self):
        if self.is_uppercase.get():
            if self.current_char == 'Z':
                self.current_char = 'A'
            else:
                self.current_char = chr(ord(self.current_char) + 1)
        else:
            if self.current_char == 'z':
                self.current_char = 'a'
            else:
                self.current_char = chr(ord(self.current_char) + 1)
    
    def update_case(self):
        self.current_char = 'A' if self.is_uppercase.get() else 'a'
        self.label.config(text=f"Current Character: {self.current_char}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataColletor(root)
    root.mainloop()
