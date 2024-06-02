# Handwriting OCR Data Collector

Handwriting OCR Data Collector is a Python application designed to collect and sanitize handwritten character data for training OCR (Optical Character Recognition) models. This tool allows users to input handwritten characters using a touchscreen or stylus, save the data in a structured format, and ensure that only valid samples are kept.

## Features

- **Grid-based Input**: Write multiple samples of characters in a grid layout.
- **Uppercase and Lowercase Support**: Collect data for both uppercase and lowercase letters.
- **Automatic and Manual Character Management**: Automatically prompts the next character or manually set the character to be inputted.
- **State Persistence**: Remembers the last inputted characters and continues from where it left off.
- **Sanitization**: Removes blank or invalid images from the dataset.

## Requirements

- Python 3.x
- tkinter
- Pillow (Python Imaging Library)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Shah-Priyanshu/Handwriting-OCR-Data-Collector.git
    cd Handwriting-OCR-Data-Collector
    ```

2. Install the required packages:
    ```bash
    pip install pillow
    ```

## Usage

1. Run the application:
    ```bash
    python handwriting_ocr_data_collector.py
    ```

2. Use the application to input handwritten characters:
    - Write characters in the grid.
    - Use the **Save** button to save the samples.
    - Use the **Clear** button to clear the grid.
    - Use the **Sanitize** button to remove blank images.

3. The application will automatically prompt the next character to be inputted. You can also manually set the character using the **Manual Input** section.

4. Ensure all lowercase letters are inputted before moving to uppercase letters.

## How It Works

### Grid-based Input

The application displays a grid where users can write multiple samples of a character. The samples are saved as individual image files in a structured directory format.

### State Persistence

The application saves the state of inputted characters in a file (`state.txt`). When restarted, it loads this state and continues from where it left off.

### Sanitization

The application includes a sanitization function that scans through the saved images and deletes blank or invalid images to ensure only valid samples are kept.
