import numpy as np

def reverse_shift_pixels(image):
    pixel_data = np.array(image, dtype=np.int32)
    height, width, channels = pixel_data.shape
    
    # Create shift values using vectorized operations (MUCH faster than loops)
    indices = np.arange(height * width).reshape(height, width)
    shift_vals = (height * width - indices) % 256
    shift_vals = shift_vals[:, :, np.newaxis]  # Add channel dimension
    
    # Apply shift to all pixels at once
    shifted = (pixel_data + shift_vals) % 256
    return shifted.astype(np.uint8)

def reverse_unshift_pixels(image):
    pixel_data = np.array(image, dtype=np.int32)
    height, width, channels = pixel_data.shape
    
    # Create shift values using vectorized operations (MUCH faster than loops)
    indices = np.arange(height * width).reshape(height, width)
    shift_vals = (height * width - indices) % 256
    shift_vals = shift_vals[:, :, np.newaxis]  # Add channel dimension
    
    # Apply unshift to all pixels at once
    unshifted = (pixel_data - shift_vals) % 256
    return unshifted.astype(np.uint8)