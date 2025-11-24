from flask import Flask, request, jsonify, send_file, session
from flask_cors import CORS
import os
import sys
import traceback
from dotenv import load_dotenv
from web_encryption import encrypt_image_web
from web_decryption import decrypt_image_web
from key_utils import log_event, check_pin_strength
from firebase_service import firebase_service
from PIL import Image
import tempfile
from datetime import datetime
import io
import base64
from werkzeug.utils import secure_filename

# Force unbuffered output for debugging
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Load environment variables
load_dotenv('../.env')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Configure max content length (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# WSGI middleware to catch errors before Flask routing
class ErrorLoggingMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        try:
            print(f"🔍 MIDDLEWARE: {environ['REQUEST_METHOD']} {environ['PATH_INFO']}", file=sys.stderr, flush=True)
            return self.app(environ, start_response)
        except Exception as e:
            print(f"\n{'='*60}", file=sys.stderr, flush=True)
            print(f"❌ MIDDLEWARE EXCEPTION: {str(e)}", file=sys.stderr, flush=True)
            print(traceback.format_exc(), file=sys.stderr, flush=True)
            print(f"{'='*60}\n", file=sys.stderr, flush=True)
            raise

app.wsgi_app = ErrorLoggingMiddleware(app.wsgi_app)

# Global error handler to catch all exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    error_details = traceback.format_exc()
    print(f"\n{'='*60}", file=sys.stderr, flush=True)
    print(f"❌ FLASK ERROR HANDLER: {str(e)}", file=sys.stderr, flush=True)
    print(f"{'='*60}", file=sys.stderr, flush=True)
    print(error_details, file=sys.stderr, flush=True)
    print(f"{'='*60}\n", file=sys.stderr, flush=True)
    return jsonify({'error': f'Server error: {str(e)}', 'details': error_details}), 500

# Enable CORS for cross-origin requests (Frontend → Backend)
CORS(app, origins=[
    "http://localhost:3000", 
    "http://localhost:5000",
    "http://localhost:8000",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:8000",
    "http://10.2.18.108:8000",  # Your LAN IP
    "https://srinivas-18.github.io",
    "https://srinivas-18.github.io/Secure-image-app/",
    "https://srinivas-18.github.io/Secure-image-app",
    "https://secure-image-app-33hz.vercel.app",  # Your Vercel deployment
    "https://*.vercel.app",
    "https://*.netlify.app",
    "*"  # Allow all origins for development - remove in production
], supports_credentials=True)

# Configuration - Use absolute path relative to project root (not backend folder)
# This matches the path used in web_encryption.py
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Ensure uploads directory exists (use absolute path for Render/cloud hosting)
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"✅ Upload folder created/verified at: {UPLOAD_FOLDER}")
    print(f"📂 Current working directory: {os.getcwd()}")
    print(f"📂 Backend directory: {os.path.dirname(__file__)}")
    print(f"📂 Root directory: {ROOT_DIR}")
except Exception as e:
    print(f"⚠️ Warning: Could not create upload folder: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify({
        'message': 'Secure Image Encryption API',
        'status': 'running',
        'endpoints': [
            '/check_pin_strength',
            '/encrypt',
            '/decrypt',
            '/download/<filename>',
            '/authenticate_logs',
            '/get_logs'
        ]
    })

@app.route('/check_pin_strength', methods=['POST'])
def check_pin_strength_route():
    data = request.get_json()
    pin = data.get('pin', '')
    strength = check_pin_strength(pin)
    return jsonify({'strength': strength})

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    try:
        print(f"\n{'='*60}", file=sys.stderr, flush=True)
        print(f"📥 ENCRYPT ROUTE CALLED", file=sys.stderr, flush=True)
        print(f"Request method: {request.method}", file=sys.stderr, flush=True)
        print(f"Content-Type: {request.content_type}", file=sys.stderr, flush=True)
        print(f"Content-Length: {request.content_length}", file=sys.stderr, flush=True)
        print(f"{'='*60}\n", file=sys.stderr, flush=True)
        
        if 'image' not in request.files:
            print(f"❌ No 'image' in request.files. Available: {list(request.files.keys())}", file=sys.stderr, flush=True)
            return jsonify({'error': 'No image file provided'}), 400
        
        print(f"✅ Found 'image' in request.files", file=sys.stderr, flush=True)
        
        file = request.files['image']
        pin = request.form.get('pin')
        
        print(f"📝 File details - filename: {file.filename}, content_type: {file.content_type}", file=sys.stderr, flush=True)
        print(f"📝 PIN received: {'Yes' if pin else 'No'} (length: {len(pin) if pin else 0})", file=sys.stderr, flush=True)
        
        if file.filename == '':
            print(f"❌ Empty filename", file=sys.stderr, flush=True)
            return jsonify({'error': 'No file selected'}), 400
        
        if not pin:
            print(f"❌ No PIN provided", file=sys.stderr, flush=True)
            return jsonify({'error': 'PIN is required'}), 400
        
        if not allowed_file(file.filename):
            print(f"❌ File type not allowed: {file.filename}", file=sys.stderr, flush=True)
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        print(f"💾 Saving to: {temp_path}", file=sys.stderr, flush=True)
        file.save(temp_path)
        print(f"✅ File saved successfully", file=sys.stderr, flush=True)
        
        # Encrypt the image
        print(f"🔐 Starting encryption...", file=sys.stderr, flush=True)
        result = encrypt_image_web(temp_path, pin)
        print(f"✅ Encryption completed. Success: {result.get('success')}", file=sys.stderr, flush=True)
        
        if not result.get('success'):
            error_msg = result.get('error', 'Unknown encryption error')
            print(f"❌ Encryption failed with error: {error_msg}", file=sys.stderr, flush=True)
        
        # Clean up original file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if result['success']:
            # Read encrypted file and meta file for direct download (APK compatibility)
            encrypted_path = os.path.join(UPLOAD_FOLDER, result['encrypted_filename'])
            meta_path = os.path.join(UPLOAD_FOLDER, result['meta_filename'])
            
            encrypted_data = None
            meta_data = None
            
            try:
                # Read files into memory for APK clients
                if os.path.exists(encrypted_path):
                    with open(encrypted_path, 'rb') as f:
                        encrypted_data = base64.b64encode(f.read()).decode('utf-8')
                
                if os.path.exists(meta_path):
                    with open(meta_path, 'r') as f:
                        meta_data = f.read()
            except Exception as e:
                print(f"⚠️ Warning: Could not read files for base64 encoding: {e}", file=sys.stderr, flush=True)
            
            return jsonify({
                'success': True,
                'encrypted_filename': result['encrypted_filename'],
                'meta_filename': result['meta_filename'],
                'encrypted_data': encrypted_data,  # Base64 for APK
                'meta_data': meta_data,  # Hash string for APK
                'stats': result['stats']
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        error_details = traceback.format_exc()
        error_msg = f"Encryption error: {str(e)}"
        print(f"\n{'='*60}", file=sys.stderr, flush=True)
        print(f"❌ {error_msg}", file=sys.stderr, flush=True)
        print(f"{'='*60}", file=sys.stderr, flush=True)
        print(error_details, file=sys.stderr, flush=True)
        print(f"{'='*60}\n", file=sys.stderr, flush=True)
        # Don't call log_event here as it might cause secondary errors
        return jsonify({'error': f'Encryption failed: {str(e)}'}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    try:
        if 'encrypted_file' not in request.files:
            return jsonify({'error': 'No encrypted file provided'}), 400
        
        file = request.files['encrypted_file']
        pin = request.form.get('pin')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not pin:
            return jsonify({'error': 'PIN is required'}), 400
        
        # Save uploaded encrypted file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        # Check if meta file exists alongside the encrypted file
        # The meta file should be uploaded together with the .enc file
        meta_filename = filename + '.meta'
        meta_path = os.path.join(UPLOAD_FOLDER, meta_filename)
        
        # Look for meta file in multiple ways:
        # 1. Separate meta_file upload field
        if 'meta_file' in request.files:
            meta_file = request.files['meta_file']
            if meta_file.filename:
                meta_file.save(meta_path)
        
        # 2. Check if user uploaded both files with same base name
        elif not os.path.exists(meta_path):
            # Look for any .meta file in the request
            for field_name, uploaded_file in request.files.items():
                if uploaded_file.filename and uploaded_file.filename.endswith('.meta'):
                    uploaded_file.save(meta_path)
                    break
        
        # Decrypt the image
        result = decrypt_image_web(temp_path, pin)
        
        # Clean up temporary files after decryption
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(meta_path):
            os.remove(meta_path)
        
        if result['success']:
            return jsonify({
                'success': True,
                'decrypted_image': result['decrypted_image'],
                'decrypted_filename': result['decrypted_filename'],
                'stats': result['stats']
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        error_msg = f"Flask decryption error: {str(e)}"
        log_event(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Use absolute path resolution to avoid path issues
        file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))
        
        print(f"\n{'='*60}", file=sys.stderr, flush=True)
        print(f"📥 DOWNLOAD REQUEST", file=sys.stderr, flush=True)
        print(f"Requested filename: {filename}", file=sys.stderr, flush=True)
        print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}", file=sys.stderr, flush=True)
        print(f"Full path: {file_path}", file=sys.stderr, flush=True)
        print(f"File exists: {os.path.exists(file_path)}", file=sys.stderr, flush=True)
        
        # List files in upload folder for debugging
        if os.path.exists(UPLOAD_FOLDER):
            files_in_folder = os.listdir(UPLOAD_FOLDER)
            print(f"Files in upload folder: {files_in_folder}", file=sys.stderr, flush=True)
        else:
            print(f"❌ Upload folder doesn't exist: {UPLOAD_FOLDER}", file=sys.stderr, flush=True)
        print(f"{'='*60}\n", file=sys.stderr, flush=True)
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': f'File not found: {file_path}'}), 404
    except Exception as e:
        print(f"❌ Download error: {str(e)}", file=sys.stderr, flush=True)
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        return jsonify({'error': str(e)}), 500

@app.route('/logs')
def view_logs():
    return jsonify({'error': 'Use /get_logs endpoint with authentication'}), 401

@app.route('/authenticate_logs', methods=['POST'])
def authenticate_logs():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == os.getenv("LOG_USERNAME") and password == os.getenv("LOG_PASSWORD"):
        session['authenticated'] = True
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/get_logs', methods=['GET'])
def get_logs():
    if not session.get('authenticated'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    log_path = os.path.join("logs", "activity_log.csv")
    if not os.path.exists(log_path):
        return jsonify({'logs': []})
    
    logs = []
    try:
        import csv
        with open(log_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                logs.append(row)
        return jsonify({'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5500)
