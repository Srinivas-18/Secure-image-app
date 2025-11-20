import numpy as np

def reverse_shift_pixels(image):
    pixel_data = np.array(image, dtype=np.int32)  # Use int32 to avoid overflow
    height, width, channels = pixel_data.shape
    shifted = np.zeros_like(pixel_data, dtype=np.uint8)  # Result as uint8
    for i in range(height):
        for j in range(width):
            shift_val = (height * width - (i * width + j)) % 256
            shifted[i, j] = (pixel_data[i, j] + shift_val) % 256
    return shifted

def reverse_unshift_pixels(image):
    pixel_data = np.array(image, dtype=np.int32)  # Use int32 to avoid overflow
    height, width, channels = pixel_data.shape
    unshifted = np.zeros_like(pixel_data, dtype=np.uint8)  # Result as uint8
    for i in range(height):
        for j in range(width):
            shift_val = (height * width - (i * width + j)) % 256
            unshifted[i, j] = (pixel_data[i, j] - shift_val) % 256
    return unshifted