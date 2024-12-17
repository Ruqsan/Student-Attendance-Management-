from PIL import Image
import matplotlib.pyplot as plt

# Load the image
image_path = "C:/Users/Ruqsan/Desktop/Temporary files/line.jpg"  # Replace with your image path
img = Image.open(image_path)

# Display the image and get coordinates for colors
def onclick(event):
    x, y = int(event.xdata), int(event.ydata)
    pixel_color = img.getpixel((x, y))
    hex_color = "#{:02x}{:02x}{:02x}".format(*pixel_color[:3])
    print(f"RGB: {pixel_color}, HEX: {hex_color}")

print("Click on the image to get the color codes (RGB and HEX).")
fig, ax = plt.subplots()
ax.imshow(img)
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
