from PIL import Image, ImageDraw, ImageFont

# Create a blank image (RGB) with white background
width, height = 800, 400
image = Image.new("RGB", (width, height), color="white")

# Get a drawing context
draw = ImageDraw.Draw(image)

# Draw shapes
draw.rectangle([50, 50, 200, 200], fill="skyblue", outline="black", width=3)
draw.ellipse([300, 50, 450, 200], fill="lightgreen", outline="black", width=3)
draw.line([500, 100, 700, 100], fill="red", width=5)

# Add text (using default font)
text = "Hello from Python!"
draw.text((50, 250), text, fill="black")

# Save the image
image_path = "my_digital_art.png"
image.save(image_path)

print(f"Image saved as {image_path}")
