# Secure Image Encryption Web Application

A modern web-based image encryption tool with advanced cryptographic security and pixel manipulation techniques.

## Features

- 🔐 **Advanced Encryption**: Fernet (AES-128) + custom pixel shifting
- 🌐 **Web Interface**: Modern, responsive Flask-based UI
- 🖥️ **Desktop GUI**: Optional Tkinter interface
- 🔍 **Integrity Verification**: SHA256 hash validation
- 📊 **Analytics**: Entropy and file size analysis
- 📋 **Activity Logging**: Secure audit trail
- 💪 **PIN Strength**: Real-time validation

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment**:
   ```bash
   copy .env.example .env
   # Edit .env with your credentials
   ```

3. **Run Web Application**:
   ```bash
   python run.py
   ```

4. **Access**: Open http://localhost:5000

## Security Features

- Multi-layer encryption (cryptographic + pixel manipulation)
- PIN-based key derivation using SHA256
- File integrity verification with hash comparison
- Secure session management
- Activity logging with authentication

## Project Structure

```
├── backend/                 # Backend Python modules
│   ├── app.py              # Flask web server
│   ├── web_encryption.py   # Web encryption logic
│   ├── web_decryption.py   # Web decryption logic
│   ├── key_utils.py        # Cryptographic utilities
│   ├── pixel_shift.py      # Pixel manipulation
│   ├── encryption.py       # GUI encryption (legacy)
│   ├── decryption.py       # GUI decryption (legacy)
│   └── main_gui.py         # Desktop GUI interface
├── frontend/               # Frontend assets
│   ├── templates/          # HTML templates
│   │   ├── index.html      # Main web interface
│   │   └── logs.html       # Activity logs page
│   └── static/             # CSS/JS assets
│       ├── style.css       # Styling
│       └── script.js       # Frontend logic
├── logs/                   # Activity logs
├── uploads/                # Temporary file storage
├── run.py                  # Application startup script
├── requirements.txt        # Python dependencies
└── .env                    # Environment configuration
```
