import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageDraw
import os

# Create a directory to save the images
if not os.path.exists('handwriting_samples'):
    os.makedirs('handwriting_samples')

class DataCollector:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwriting Data Collector")
        
        self.char_var = tk.StringVar()
        
        self.label = tk.Label(root, text="ENTER THE CHAR:")
        self.label.pack()
        
        self.entry = tk.Entry(root, textvariable=self.char_var)
        self.entry.pack()
        
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
        for i in range(6):
            self.canvas.create_line(0, i*80, 600, i*80, fill='orange')
            self.canvas.create_line(i*100, 0, i*100, 400, fill='orange')

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

    def save_image(self):
        letter = self.char_var.get()
        if letter:
            save_path = f'handwriting_samples/{letter}'
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            image_count = len(os.listdir(save_path))
            self.image.save(f"{save_path}/{letter}_{image_count + 1}.png")
            self.clear_canvas()
        else:
            messagebox.showerror("Error", "Please enter a character before saving.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataCollector(root)
    root.mainloop()
