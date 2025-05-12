import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
from typing import List, Tuple, Optional

class ImageAnalyzer:
    """
    A GUI application for analyzing image regions by comparing their average pixel values.
    
    This application allows users to:
    1. Load an image
    2. Draw multiple rectangles on the image
    3. Calculate and display the average pixel values for each region
    4. Compare other regions against a reference region
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the ImageAnalyzer application.
        
        Args:
            root: The main Tkinter window
        """
        self.root = root
        self.root.title("Image Region Analyzer")
        
        # Initialize variables
        self.image: Optional[Image.Image] = None
        self.photo: Optional[ImageTk.PhotoImage] = None
        self.rectangles: List[Tuple[int, int, int, int, str, int]] = []  # (x1, y1, x2, y2, color, canvas_id)
        self.current_rect: Optional[int] = None
        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple']
        self.current_color_index = 0
        self.reference_rect_id: Optional[int] = None  # Store the canvas ID of the reference rectangle
        self.reference_avg: Optional[float] = None  # Store the average value of the reference rectangle
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create canvas for image
        self.canvas = tk.Canvas(self.main_frame, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create control panel
        self.control_panel = ttk.Frame(self.main_frame)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        # Add buttons
        ttk.Button(self.control_panel, text="Load Image", command=self.load_image).pack(pady=5)
        ttk.Button(self.control_panel, text="Clear Rectangles", command=self.clear_rectangles).pack(pady=5)
        
        # Add results frame
        self.results_frame = ttk.LabelFrame(self.control_panel, text="Average Pixel Values")
        self.results_frame.pack(fill=tk.X, pady=5)
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
    def load_image(self):
        """Load an image file and display it on the canvas."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.clear_rectangles()
    
    def on_press(self, event):
        """Handle mouse press event to start drawing a rectangle."""
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline=self.colors[self.current_color_index]
        )
    
    def on_drag(self, event):
        """Handle mouse drag event to update rectangle size."""
        if self.current_rect:
            cur_x = self.canvas.canvasx(event.x)
            cur_y = self.canvas.canvasy(event.y)
            self.canvas.coords(self.current_rect, self.start_x, self.start_y, cur_x, cur_y)
    
    def on_release(self, event):
        """Handle mouse release event to finalize rectangle."""
        if self.current_rect:
            end_x = self.canvas.canvasx(event.x)
            end_y = self.canvas.canvasy(event.y)
            
            # If this is the first rectangle, make it the reference
            if not self.rectangles:
                self.reference_rect_id = self.current_rect
                # Add "Reference" text above the rectangle
                x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
                self.canvas.create_text(x1, y1 - 10, text=
                """
                Пример
                свободного
                места
                """, fill="red", anchor="sw")
            
            self.rectangles.append((
                min(self.start_x, end_x),
                min(self.start_y, end_y),
                max(self.start_x, end_x),
                max(self.start_y, end_y),
                self.colors[self.current_color_index],
                self.current_rect
            ))
            self.current_rect = None
            self.update_averages()
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
    
    def clear_rectangles(self):
        """Clear all rectangles and their average value displays."""
        for rect in self.rectangles:
            self.canvas.delete(rect[5])  # Delete using canvas_id
        self.rectangles = []
        self.reference_rect_id = None
        self.reference_avg = None
        self.update_averages()

        self.canvas.delete("text")
    
    def update_averages(self):
        """Calculate and display average pixel values for all rectangles."""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not self.image or not self.rectangles:
            return
        
        # Convert image to numpy array
        img_array = np.array(self.image)
        
        # First, calculate reference average if it exists
        if self.reference_rect_id:
            ref_rect = next((r for r in self.rectangles if r[5] == self.reference_rect_id), None)
            if ref_rect:
                x1, y1, x2, y2 = ref_rect[0:4]
                x1, y1 = max(0, int(x1)), max(0, int(y1))
                x2, y2 = min(img_array.shape[1], int(x2)), min(img_array.shape[0], int(y2))
                ref_region = img_array[y1:y2, x1:x2]
                self.reference_avg = np.mean(ref_region)
                
                # Display reference average
                ref_text = f"Reference Region: {self.reference_avg:.2f}"
                ref_label = ttk.Label(self.results_frame, text=ref_text, foreground="red")
                ref_label.pack(pady=2)
        
        # Calculate and display averages for all rectangles
        for i, (x1, y1, x2, y2, color, canvas_id) in enumerate(self.rectangles):
            # Skip reference rectangle as it's already displayed
            if canvas_id == self.reference_rect_id:
                continue
                
            # Ensure coordinates are within image bounds
            x1, y1 = max(0, int(x1)), max(0, int(y1))
            x2, y2 = min(img_array.shape[1], int(x2)), min(img_array.shape[0], int(y2))
            
            # Calculate average
            region = img_array[y1:y2, x1:x2]
            avg_value = np.mean(region)

            # Create result label with comparison to reference
            if self.reference_avg is not None:
                diff = abs(avg_value - self.reference_avg)
                result_text = f"Region {i+1} ({color}): {avg_value:.2f} (diff: {diff:.2f})"
                
                # Add "свободно" text if difference is less than 3
                if diff < 3:
                    self.canvas.create_text(x1, y1 - 10, text="свободно", fill="green", anchor="sw")
                else:
                    self.canvas.create_text(x1, y1 - 10, text="занято", fill="red", anchor="sw")
            else:
                result_text = f"Region {i+1} ({color}): {avg_value:.2f}"
            
            ttk.Label(self.results_frame, text=result_text).pack(pady=2)

def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = ImageAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 