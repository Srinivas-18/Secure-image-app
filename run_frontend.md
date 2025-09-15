# 🚀 How to Run Your Frontend

## 🔧 **Backend Connection Fixed**
Your frontend is now configured to connect to: `https://secure-image-encryption-api.onrender.com`

## 📱 **Running Frontend Locally**

### **Option 1: Live Server (Recommended)**
1. **Install Live Server Extension** in VS Code
2. **Right-click on `index.html`** → "Open with Live Server"
3. **Add Firebase Domain**: Go to Firebase Console → Authentication → Settings → Authorized domains
4. **Add**: `127.0.0.1` and `localhost`

### **Option 2: Python HTTP Server**
```bash
# Navigate to your project directory
cd "c:\Users\Acer\Downloads\image encryption\image_encryption_project - Copy"

# Run Python server
python -m http.server 8000

# Open browser to: http://localhost:8000
```

### **Option 3: Node.js HTTP Server**
```bash
# Install http-server globally
npm install -g http-server

# Run server
http-server -p 8000

# Open browser to: http://localhost:8000
```

## 🔥 **Fix Firebase Auth Error**

The error `auth/unauthorized-domain` means you need to add your local domain to Firebase:

1. **Go to Firebase Console**: https://console.firebase.google.com
2. **Select your project**
3. **Authentication** → **Settings** → **Authorized domains**
4. **Add these domains**:
   - `127.0.0.1`
   - `localhost`
   - `localhost:8000` (if using port 8000)
   - `127.0.0.1:5500` (if using Live Server)

## ✅ **What's Fixed**

- ✅ Backend URL now points to your deployed Render API
- ✅ Removed Flask template syntax from frontend
- ✅ Frontend will work with your deployed backend
- ✅ Better error handling for connection issues

## 🧪 **Testing**

Once you run the frontend:
1. **Authentication**: Should work after adding domains to Firebase
2. **Encryption**: Will connect to your Render backend
3. **Log Activity**: Will authenticate with your backend

## 🌐 **For Production**
Your GitHub Pages deployment at `https://srinivas-18.github.io/Secure-image-app/` should work automatically once you push these changes.
