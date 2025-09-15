from cryptography.fernet import Fernet
import io
import os
import base64
from PIL import Image
from pixel_shift import reverse_shift_pixels
from key_utils import generate_key_from_pin, get_file_hash, log_event, calculate_entropy, get_file_size_kb

def encrypt_image_web(image_path, pin):
    """
    Web-based image encryption function
    Returns a dictionary with success status and relevant data
    """
    try:
        if not os.path.exists(image_path):
            return {'success': False, 'error': 'Image file not found'}
        
        if not pin:
            return {'success': False, 'error': 'PIN is required'}

        # Load and process image
        image = Image.open(image_path).convert('RGB')
        entropy_before = calculate_entropy(image)
        size_before = get_file_size_kb(image_path)

        # Apply pixel shift
        shifted_img = reverse_shift_pixels(image)
        entropy_after = calculate_entropy(Image.fromarray(shifted_img))

        # Convert to bytes
        buffer = io.BytesIO()
        Image.fromarray(shifted_img).save(buffer, format='PNG')
        img_bytes = buffer.getvalue()

        # Generate hash for integrity
        original_hash = get_file_hash(img_bytes)
        log_event(f"Web encryption - Image: {os.path.basename(image_path)}")
        log_event(f"Pre-encryption SHA256: {original_hash}")

        # Encrypt data
        key = generate_key_from_pin(pin)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(img_bytes)

        # Generate filename for encrypted file
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        encrypted_filename = f"{base_name}_encrypted.enc"
        encrypted_path = os.path.join("uploads", encrypted_filename)
        
        # Save encrypted file
        os.makedirs("uploads", exist_ok=True)
        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)
        
        size_after = get_file_size_kb(encrypted_path)

        # Save meta file
        meta_path = encrypted_path + ".meta"
        with open(meta_path, "w") as meta_file:
            meta_file.write(original_hash)

        log_event(f"Web encryption completed: {encrypted_filename}")
        log_event(f"Hash saved to: {meta_path}")

        return {
            'success': True,
            'encrypted_filename': encrypted_filename,
            'meta_filename': os.path.basename(meta_path),
            'stats': {
                'entropy_before': entropy_before,
                'entropy_after': entropy_after,
                'size_before': size_before,
                'size_after': size_after,
                'original_hash': original_hash
            }
        }

    except Exception as e:
        log_event(f"Web encryption failed: {str(e)}")
        return {'success': False, 'error': str(e)}
