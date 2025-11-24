<div align="center">

# 🔐 Secure Image Encryption

### Military-Grade Image Encryption Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Authentication-orange.svg)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Protect your sensitive images with enterprise-grade encryption. Fast, secure, and privacy-first.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Security](#-security)

</div>

---

## 🌟 Features

### 🔒 **Advanced Encryption**
- **AES-256 Encryption** - Industry-standard Fernet cryptography
- **Custom Pixel Shifting** - Additional layer with NumPy-optimized algorithms
- **PIN-Based Key Derivation** - SHA256 hashing for secure key generation
- **Integrity Verification** - SHA256 hash validation for tamper detection

### 🎨 **Modern Web Interface**
- **Premium SaaS Design** - Clean, professional, production-ready UI
- **Real-time PIN Strength** - Visual feedback for password security
- **Firebase Authentication** - Secure login with email/password or Google
- **Responsive Layout** - Works seamlessly on desktop, tablet, and mobile
- **Live Stats Display** - Entropy analysis and file size metrics

### 📊 **Analytics & Monitoring**
- **Entropy Measurement** - Before/after encryption analysis
- **File Size Tracking** - Monitor encryption overhead
- **Activity Logging** - Secure audit trail with authentication
- **CSV Export** - Download activity logs for compliance

### 🛡️ **Security First**
- **Zero Data Storage** - Files deleted immediately after processing
- **Session Management** - Secure user authentication
- **CORS Protection** - Configured for production deployment
- **Input Validation** - Comprehensive security checks

---

## 🚀 Demo

### Live Deployment
- **Frontend**: Deployed on [Vercel](https://vercel.com) *(Add your URL)*
- **Backend**: Hosted on [Render](https://render.com) *(Add your URL)*

### Screenshots

**Hero & Authentication**
```
Modern landing page with gradient hero section
Secure Firebase authentication (Email/Google)
```

**Encryption Interface**
```
Drag-and-drop file upload
Real-time PIN strength indicator
Instant encryption with download links
```

**Analytics Dashboard**
```
Entropy comparison (before/after)
File size metrics
Activity logs with timestamps
```

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **pip** package manager
- **Git**
- **Firebase account** (for authentication)

### Step 1: Clone Repository
```bash
git clone https://github.com/Srinivas-18/Secure-image-app.git
cd Secure-image-app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Backend dependencies:**
- Flask 2.0+
- Flask-CORS
- cryptography
- Pillow (PIL)
- numpy
- firebase-admin
- python-dotenv

### Step 3: Configure Firebase
1. Create a Firebase project at [console.firebase.google.com](https://console.firebase.google.com)
2. Enable **Email/Password** and **Google** authentication
3. Update `firebaseConfig` in `index.html` with your credentials:
```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

### Step 4: Run Backend Server
```bash
cd backend
python app.py
```
Backend will run on `http://localhost:5500`

### Step 5: Open Frontend
Open `index.html` in your browser or use a local server:
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server -p 8000
```

---

## 💡 Usage

### Encrypting Images

1. **Login** with your email/password or Google account
2. **Upload** your image (PNG, JPG, JPEG)
3. **Enter** a secure PIN (minimum 6 characters)
4. **Encrypt** - Get two files:
   - `.enc` - Encrypted image
   - `.meta` - Hash file for integrity verification
5. **Download** both files and keep them safe

### Decrypting Images

1. **Login** to your account
2. **Upload** the encrypted `.enc` file
3. **(Optional)** Upload the `.meta` file for integrity check
4. **Enter** the correct PIN
5. **Decrypt** - View and download the original image

### Activity Logs

1. Click **"View Activity Log"**
2. Authenticate with admin credentials
3. View all encryption/decryption activities with timestamps

---

## 🏗️ Architecture

### Technology Stack

**Frontend**
- HTML5 / CSS3 (Modern, Responsive Design)
- JavaScript (ES6+)
- Firebase SDK (Authentication)

**Backend**
- Flask (Python Web Framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- Gunicorn (Production WSGI Server)

**Security**
- Cryptography (Fernet - AES-256)
- NumPy (Optimized Pixel Manipulation)
- SHA256 (Hashing & Key Derivation)

**Deployment**
- Vercel (Frontend Hosting)
- Render (Backend Hosting)
- Firebase (Authentication Service)

### Project Structure

```
Secure-image-app/
├── backend/
│   ├── app.py                  # Flask server & API endpoints
│   ├── web_encryption.py       # Image encryption logic
│   ├── web_decryption.py       # Image decryption logic
│   ├── pixel_shift.py          # NumPy pixel manipulation
│   ├── key_utils.py            # Cryptographic utilities
│   ├── firebase_service.py     # Firebase integration
│   ├── requirements.txt        # Python dependencies
│   └── render.yaml             # Render deployment config
│
├── frontend/
│   ├── index.html              # Main SPA (Single Page App)
│   ├── style.css               # Premium UI styles
│   └── netlify.toml            # Netlify config (alternative)
│
├── logs/
│   └── activity_log.csv        # Audit trail
│
├── uploads/                    # Temporary file storage (auto-cleanup)
│
├── index.html                  # Root entry point
├── requirements.txt            # Root dependencies
├── run.py                      # Local development server
└── README.md                   # This file
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/encrypt` | POST | Encrypt image with PIN |
| `/decrypt` | POST | Decrypt image with PIN |
| `/check_pin_strength` | POST | Validate PIN strength |
| `/authenticate_logs` | POST | Authenticate for log access |
| `/get_logs` | GET | Retrieve activity logs |
| `/download/<filename>` | GET | Download encrypted/decrypted files |

---

## 🔐 Security

### Encryption Process

1. **PIN Hashing**: User PIN → SHA256 → 32-byte key
2. **Fernet Encryption**: Image bytes → AES-256-CBC encryption
3. **Pixel Shifting**: Encrypted data → NumPy pixel manipulation
4. **Hash Generation**: Original image → SHA256 → `.meta` file

### Decryption Process

1. **PIN Verification**: User PIN → SHA256 → Key derivation
2. **Reverse Pixel Shift**: Encrypted data → Original encrypted bytes
3. **Fernet Decryption**: Encrypted bytes → AES-256 decryption → Image
4. **Integrity Check**: Compare hash with `.meta` file (if provided)

### Security Best Practices

✅ **PIN Requirements**
- Minimum 6 characters
- Mix of letters, numbers, symbols recommended
- Real-time strength indicator

✅ **Data Handling**
- Files stored temporarily in `uploads/`
- Automatic cleanup after processing
- No permanent storage of user images

✅ **Authentication**
- Firebase secure authentication
- Email verification supported
- Google OAuth integration

✅ **Production Security**
- CORS configured for specific origins
- HTTPS enforced in production
- Environment variables for sensitive data

---

## 🚀 Deployment

### Backend (Render)

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: secure-image-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --timeout 300
```

2. Deploy to Render
3. Update frontend API URL in `index.html`

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Deploy with one click
4. Update CORS in backend to allow Vercel domain

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Srinivas**
- GitHub: [@Srinivas-18](https://github.com/Srinivas-18)
- Email: iamlakshmisrinivas2005@gmail.com

---

## 🙏 Acknowledgments

- **Firebase** - Authentication infrastructure
- **Vercel & Render** - Deployment platforms
- **Cryptography.io** - Python cryptography library
- **NumPy** - High-performance array operations

---

<div align="center">

**⭐ Star this repo if you find it useful!**

[Report Bug](https://github.com/Srinivas-18/Secure-image-app/issues) • [Request Feature](https://github.com/Srinivas-18/Secure-image-app/issues)

Made with ❤️ for secure image encryption

</div>
