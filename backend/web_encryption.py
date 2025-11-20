from cryptography.fernet import Fernet
import io
import os
import base64
from PIL import Image
from pixel_shift import reverse_shift_pixels
from key_utils import generate_key_from_pin, get_file_hash, log_event, calculate_entropy, get_file_size_kb

# Resolve absolute uploads path from project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOADS_DIR = os.path.join(ROOT_DIR, 'uploads')

def encrypt_image_web(image_path, pin):
    """
    Web-based image encryption function
    Returns a dictionary with success status and relevant data
    """
    import sys
    try:
        print(f"🔍 [ENCRYPT] Starting with image_path: {image_path}", file=sys.stderr, flush=True)
        
        if not os.path.exists(image_path):
            error_msg = f'Image file not found: {image_path}'
            print(f"❌ [ENCRYPT] {error_msg}", file=sys.stderr, flush=True)
            return {'success': False, 'error': error_msg}
        
        if not pin:
            print(f"❌ [ENCRYPT] PIN is required", file=sys.stderr, flush=True)
            return {'success': False, 'error': 'PIN is required'}

        print(f"✅ [ENCRYPT] File exists, loading image...", file=sys.stderr, flush=True)
        # Load and process image
        image = Image.open(image_path).convert('RGB')
        print(f"✅ [ENCRYPT] Image loaded: {image.size}", file=sys.stderr, flush=True)
        
        entropy_before = calculate_entropy(image)
        print(f"✅ [ENCRYPT] Entropy calculated: {entropy_before}", file=sys.stderr, flush=True)
        
        size_before = get_file_size_kb(image_path)
        print(f"✅ [ENCRYPT] Size before: {size_before}KB", file=sys.stderr, flush=True)

        # Apply pixel shift
        print(f"🔄 [ENCRYPT] Applying pixel shift...", file=sys.stderr, flush=True)
        shifted_img = reverse_shift_pixels(image)
        entropy_after = calculate_entropy(Image.fromarray(shifted_img))
        print(f"✅ [ENCRYPT] Pixel shift complete, entropy: {entropy_after}", file=sys.stderr, flush=True)

        # Convert to bytes
        print(f"📦 [ENCRYPT] Converting to bytes...", file=sys.stderr, flush=True)
        buffer = io.BytesIO()
        Image.fromarray(shifted_img).save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        print(f"✅ [ENCRYPT] Image converted to bytes: {len(img_bytes)} bytes", file=sys.stderr, flush=True)

        # Generate hash for integrity
        print(f"🔐 [ENCRYPT] Generating hash...", file=sys.stderr, flush=True)
        original_hash = get_file_hash(img_bytes)
        print(f"✅ [ENCRYPT] Hash: {original_hash[:16]}...", file=sys.stderr, flush=True)
        
        log_event(f"Web encryption - Image: {os.path.basename(image_path)}")
        log_event(f"Pre-encryption SHA256: {original_hash}")
        print(f"✅ [ENCRYPT] Logged events", file=sys.stderr, flush=True)

        # Encrypt data
        print(f"🔑 [ENCRYPT] Generating encryption key from PIN...", file=sys.stderr, flush=True)
        key = generate_key_from_pin(pin)
        print(f"✅ [ENCRYPT] Key generated", file=sys.stderr, flush=True)
        
        print(f"🔐 [ENCRYPT] Encrypting data...", file=sys.stderr, flush=True)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(img_bytes)
        print(f"✅ [ENCRYPT] Data encrypted: {len(encrypted_data)} bytes", file=sys.stderr, flush=True)

        # Generate filename for encrypted file
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        encrypted_filename = f"{base_name}_encrypted.enc"
        encrypted_path = os.path.join(UPLOADS_DIR, encrypted_filename)
        
        # Save encrypted file
        os.makedirs(UPLOADS_DIR, exist_ok=True)
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
        import sys
        error_msg = f"Web encryption failed: {str(e)}"
        print(f"\n{'='*60}", file=sys.stderr, flush=True)
        print(f"❌ [ENCRYPT EXCEPTION] {error_msg}", file=sys.stderr, flush=True)
        import traceback
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        print(f"{'='*60}\n", file=sys.stderr, flush=True)
        log_event(error_msg)
        return {'success': False, 'error': str(e)}
