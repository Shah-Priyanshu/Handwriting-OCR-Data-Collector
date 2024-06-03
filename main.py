import tkinter as tk
from data_collector import DataCollector
from progress import Progress
from collected_data import CollectedData

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwriting Data Collector")

        self.main_menu()

    def main_menu(self):
        self.clear_window()

        self.title = tk.Label(self.root, text="Handwriting Data Collector", font=("Helvetica", 16))
        self.title.pack(pady=20)

        self.data_collector_button = tk.Button(self.root, text="Data Collector", command=self.open_data_collector)
        self.data_collector_button.pack(pady=10)

        self.progress_button = tk.Button(self.root, text="Progress", command=self.open_progress)
        self.progress_button.pack(pady=10)

        self.collected_data_button = tk.Button(self.root, text="Collected Data", command=self.open_collected_data)
        self.collected_data_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def open_data_collector(self):
        self.clear_window()
        DataCollector(self.root, self.back_to_main_menu)

    def open_progress(self):
        self.clear_window()
        Progress(self.root, self.back_to_main_menu)

    def open_collected_data(self):
        self.clear_window()
        CollectedData(self.root, self.back_to_main_menu)

    def back_to_main_menu(self):
        self.main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
