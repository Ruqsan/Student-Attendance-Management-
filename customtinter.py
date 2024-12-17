import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Specific Image Background")
root.geometry("800x600")  # Window size (can be adjusted)

# Path to the specific background image
background_image_path = "path/to/your/specific_image.jpg"  # Update with your image path

# Open the image and resize it to fit the window size
bg_image = Image.open(r"C:/Users/Ruqsan/Desktop/110832.jpg")
bg_image = bg_image.resize((800, 600))  # Resize image to fit window

# Convert the image to a Tkinter-compatible format
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to hold the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Fill the entire window

# Start the Tkinter event loop
root.mainloop()
