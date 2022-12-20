import numpy as np
from PIL import Image

# Create a grayscale NumPy array with random values
arr = np.random.randint(0, 256, size=(100, 100), dtype=np.uint8)

# Convert the NumPy array to a grayscale image
image = Image.fromarray(arr, 'L')

# Save the image to a JPEG file
image.save('./spells/lumos/Lumos1.jpeg', 'JPEG')