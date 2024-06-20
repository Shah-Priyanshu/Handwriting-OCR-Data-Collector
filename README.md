# Handwriting OCR Data Collector

Handwriting OCR Data Collector is a Python application designed to collect and manage handwriting samples for OCR (Optical Character Recognition) training. This tool allows users to input handwritten characters, save them, and view their progress. It supports both uppercase and lowercase letters, storing them in separate directories.

## Features

- **Data Collection**: Input handwritten samples using a touchscreen or stylus.
- **Auto-Increment Character**: Automatically moves to the next character after saving samples.
- **Manual Character Input**: Manually select which character to input.
- **Uppercase/Lowercase Toggle**: Toggle between uppercase and lowercase characters.
- **Eraser Functionality**: Erase specific cells in the grid.
- **Progress and Collected Data Viewer**: View the number of samples collected for each character and click on characters to open folders containing collected samples.
- **Sanitization**: Remove empty images from the saved samples.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Shah-Priyanshu/Handwriting-OCR-Data-Collector.git
    cd Handwriting-OCR-Data-Collector
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python main.py
    ```

## Usage

### Data Collection

1. Launch the application and select "Data Collector".
2. Use the canvas to write the character. The grid will help you align your writing.
3. Use the "Clear" button to clear the canvas.
4. Use the "Save" button to save the current samples and move to the next character.
5. Toggle between uppercase and lowercase using the checkbox.
6. Use the "Eraser" checkbox to enable erasing mode. Click on the cell you want to erase.
7. Manually select a character by entering it in the input field and clicking "Set Character".

### Progress and Collected Data

1. Select "Progress and Collected Data" from the main menu.
2. View your progress for each character. The grid shows the number of samples collected, color-coded:
    - Red: Less than 18 samples
    - Yellow: 18 to 35 samples
    - Green: 36 or more samples
3. Click on a character to open the folder containing the collected samples for that character. If no data is found, a message will be displayed.

### Sanitization

1. Use the "Sanitize" button in the Data Collector interface to remove empty images from the saved samples (currently commented out in your code).

## File Structure

- `main.py`: Main application entry point.
- `data_collector.py`: Handles the data collection interface and functionality.
- `progress.py`: Combines progress tracking and collected data viewing.
- `handwriting_samples/`: Directory where handwriting samples are stored.
  - `single_lowercase/`: Contains folders for each lowercase character.
  - `single_uppercase/`: Contains folders for each uppercase character.
  - `bi_lowercase/` : Contains folders for each combination of (lowercase_lowercase) characters. 
  - `bi_mixedcase/` : Contains folders for each combination of (uppercase_lowercase) characters. 