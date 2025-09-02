from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
import os
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

# Load environment variables
load_dotenv('../.env')

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Enable CORS for cross-origin requests (Vercel → Render)
CORS(app, origins=["http://localhost:3000", "https://*.vercel.app"])

# Configuration
UPLOAD_FOLDER = 'backend/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_pin_strength', methods=['POST'])
def check_pin_strength_route():
    data = request.get_json()
    pin = data.get('pin', '')
    strength = check_pin_strength(pin)
    return jsonify({'strength': strength})

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        pin = request.form.get('pin')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not pin:
            return jsonify({'error': 'PIN is required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        # Encrypt the image
        result = encrypt_image_web(temp_path, pin)
        
        # Clean up original file
        os.remove(temp_path)
        
        if result['success']:
            return jsonify({
                'success': True,
                'encrypted_filename': result['encrypted_filename'],
                'meta_filename': result['meta_filename'],
                'stats': result['stats']
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        log_event(f"Encryption error: {str(e)}")
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
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': f'File not found: {file_path}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs')
def view_logs():
    return render_template('logs.html')

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
    
    log_path = os.path.join("../logs", "activity_log.csv")
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
    app.run(debug=True, host='0.0.0.0', port=5000)
