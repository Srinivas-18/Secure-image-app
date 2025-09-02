from cryptography.fernet import Fernet
from PIL import Image, UnidentifiedImageError
import io
import os
import base64
from pixel_shift import reverse_unshift_pixels
from key_utils import generate_key_from_pin, get_file_hash, get_file_size_kb, log_event, calculate_entropy

def decrypt_image_web(encrypted_file_path, pin):
    """
    Web-based image decryption function
    Returns a dictionary with success status and relevant data
    """
    try:
        # Handle both absolute and relative paths
        if not os.path.isabs(encrypted_file_path):
            # If relative path, check in uploads directory first
            uploads_path = os.path.join("backend/uploads", encrypted_file_path)
            if os.path.exists(uploads_path):
                encrypted_file_path = uploads_path
        
        if not os.path.exists(encrypted_file_path):
            return {'success': False, 'error': f'Encrypted file not found: {encrypted_file_path}'}
        
        if not pin:
            return {'success': False, 'error': 'PIN is required'}

        # Generate key from PIN
        key = generate_key_from_pin(pin)
        fernet = Fernet(key)

        # Read encrypted file
        with open(encrypted_file_path, "rb") as f:
            encrypted_data = f.read()

        size_before = get_file_size_kb(encrypted_file_path)

        # Decrypt data
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception as decrypt_error:
            log_event(f"Fernet decryption failed: {str(decrypt_error)}")
            return {'success': False, 'error': f'Decryption failed - wrong PIN or corrupted file: {str(decrypt_error)}'}
        
        decrypted_hash = get_file_hash(decrypted_data)
        
        log_event(f"Web decryption - File: {os.path.basename(encrypted_file_path)}")
        log_event(f"Post-decryption SHA256: {decrypted_hash}")

        # Verify integrity if meta file exists
        meta_path = encrypted_file_path + ".meta"
        integrity_verified = False
        if os.path.exists(meta_path):
            with open(meta_path, "r") as meta_file:
                original_hash = meta_file.read().strip()
                if original_hash != decrypted_hash:
                    log_event("WARNING: Decrypted image hash mismatch!")
                    return {'success': False, 'error': 'Hash mismatch detected! File may be tampered with or wrong PIN used.'}
                else:
                    log_event("Image integrity verified successfully.")
                    integrity_verified = True
        else:
            log_event("No .meta file found. Skipping integrity check.")

        # Load and process decrypted image
        img = Image.open(io.BytesIO(decrypted_data)).convert('RGB')
        entropy_after = calculate_entropy(img)

        # Reverse pixel shift
        unshifted_img = reverse_unshift_pixels(img)

        # Convert back to base64 for web display
        output_buffer = io.BytesIO()
        Image.fromarray(unshifted_img).save(output_buffer, format='PNG')
        img_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        # Generate output filename for decrypted image
        base_name = os.path.splitext(os.path.basename(encrypted_file_path))[0]
        if base_name.endswith('_encrypted'):
            base_name = base_name[:-10]  # Remove '_encrypted' suffix
        
        decrypted_filename = f"{base_name}_decrypted.png"
        decrypted_path = os.path.join("backend/uploads", decrypted_filename)
        
        # Save decrypted image file
        Image.fromarray(unshifted_img).save(decrypted_path)
        size_after = get_file_size_kb(decrypted_path)

        # Note: File cleanup will be handled by Flask app after response is sent

        log_event(f"Web decryption completed: {decrypted_filename}")
        log_event("Encrypted and meta files deleted after successful decryption.")

        return {
            'success': True,
            'decrypted_image': img_base64,
            'decrypted_filename': decrypted_filename,
            'stats': {
                'entropy_before': 8.0,  # Approximate for encrypted data
                'entropy_after': entropy_after,
                'size_before': size_before,
                'size_after': size_after,
                'integrity_verified': integrity_verified
            }
        }

    except UnidentifiedImageError as e:
        error_msg = f"Invalid image or wrong PIN: {str(e)}"
        log_event(f"Web decryption failed: {error_msg}")
        return {'success': False, 'error': error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        log_event(f"Web decryption failed: {error_msg}")
        return {'success': False, 'error': error_msg}
