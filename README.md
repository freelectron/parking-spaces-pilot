# Image Region Analyzer

A Python application for analyzing and comparing regions in images by their average pixel values. This tool is particularly useful for comparing different areas of an image and determining their similarity based on pixel intensity.

## Features

- Load and display images (supports JPG, JPEG, PNG, BMP, GIF)
- Draw multiple rectangular regions on the image
- Calculate average pixel values for each region
- Compare regions against a reference region
- Visual indicators for region status (free/occupied)
- Color-coded results and labels

## Installation

1. Ensure you have Python 3.9 or higher installed
2. Make sure you have the required dependencies:
   ```bash
   pip install Pillow numpy
   ```
   Or using Poetry:
   ```bash
   poetry install
   ```

## Usage

1. Run the application:
   ```bash
   python image_analyzer.py
   ```

2. Using the Application:
   - Click "Load Image" to select an image file
   - Draw rectangles on the image by clicking and dragging:
     - The first rectangle you draw becomes the reference rectangle
     - Subsequent rectangles will be compared against the reference
   - The results panel on the right shows:
     - Reference region's average pixel value (in red)
     - Other regions' average values and their difference from the reference
   - Visual indicators appear above each rectangle:
     - Reference rectangle shows "Пример свободного места" in red
     - Other rectangles show:
       - "свободно" in green if the difference from reference is less than 3
       - "занято" in red if the difference is 3 or more
   - Use "Clear Rectangles" to start over

## Technical Details

### Main Components

1. **ImageAnalyzer Class**
   - Handles the main application logic
   - Manages the GUI elements and user interactions
   - Processes image data and calculations

2. **Key Methods**:
   - `load_image()`: Loads and displays the selected image
   - `on_press()`, `on_drag()`, `on_release()`: Handle rectangle drawing
   - `update_averages()`: Calculates and displays pixel value comparisons
   - `clear_rectangles()`: Resets the application state

3. **Data Structures**:
   - `rectangles`: List of tuples containing rectangle data (x1, y1, x2, y2, color, canvas_id)
   - `reference_rect_id`: Tracks the reference rectangle
   - `reference_avg`: Stores the reference region's average pixel value

### How It Works

1. **Image Loading**:
   - Uses PIL (Python Imaging Library) to load and process images
   - Converts images to a format suitable for display and analysis

2. **Rectangle Drawing**:
   - First rectangle becomes the reference
   - Each rectangle is assigned a unique color
   - Rectangle coordinates are stored for later analysis

3. **Pixel Analysis**:
   - Converts image regions to numpy arrays for efficient processing
   - Calculates average pixel values for each region
   - Compares values against the reference region

4. **Visual Feedback**:
   - Color-coded labels indicate region status
   - Results panel shows numerical comparisons
   - Text labels appear above rectangles showing their status

## Dependencies

- `tkinter`: For the GUI (included in Python standard library)
- `Pillow`: For image processing
- `numpy`: For numerical computations

## Notes

- The application uses a threshold of 3 units difference to determine if a region is "free" or "occupied"
- All rectangles are drawn with different colors for easy identification
- The reference rectangle is always the first one drawn
- The application automatically handles image boundaries and invalid coordinates 