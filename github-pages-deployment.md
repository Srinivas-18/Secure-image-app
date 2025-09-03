# 🚀 GitHub Pages Deployment Guide

## 📋 Your Current Setup
- **Frontend URL**: https://srinivas-18.github.io/Secure-image-app/
- **Repository**: Srinivas-18/Secure-image-app
- **Deployment Method**: GitHub Pages

## 🔧 Configuration Updates Made

### ✅ **CORS Configuration Updated**
Your backend `app.py` now includes your GitHub Pages domain:
```python
CORS(app, origins=[
    "https://srinivas-18.github.io",
    "https://srinivas-18.github.io/Secure-image-app/",
    # ... other origins
])
```

### ✅ **API URL Configuration**
Your frontend automatically detects the environment and uses the correct backend URL.

## 🚀 **Deployment Steps**

### **Step 1: Deploy Backend to Render**
1. Create a Render account at https://render.com
2. Connect your GitHub repository
3. Create a **Web Service** with these settings:
   - **Name**: `secure-image-encryption-backend`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Environment**: Python 3

4. **Set Environment Variables** in Render:
   ```
   FLASK_SECRET_KEY=your-super-secure-secret-key-here
   LOG_USERNAME=admin
   LOG_PASSWORD=your-secure-password-123
   DEBUG=False
   HOST=0.0.0.0
   PORT=10000
   ```

5. **Note your Render URL** (e.g., `https://your-app-name.onrender.com`)

### **Step 2: Update Frontend Configuration**
1. In your `index.html` file, update line 1049:
   ```javascript
   return 'https://your-actual-render-url.onrender.com';
   ```
   Replace with your actual Render deployment URL

### **Step 3: Deploy to GitHub Pages**
1. **Push to GitHub**: Commit and push all your changes to the `main` branch
2. **Enable GitHub Pages**:
   - Go to your repository settings
   - Scroll to "Pages" section
   - Select "Deploy from a branch"
   - Choose `main` branch and `/ (root)` folder
   - Save

3. **Your site will be available at**: https://srinivas-18.github.io/Secure-image-app/

## 📁 **File Structure for GitHub Pages**

Make sure these files are in your repository root:
```
/
├── index.html              # Main frontend file (required)
├── backend/                # Backend files (for Render deployment)
│   ├── app.py
│   ├── requirements.txt
│   └── [other backend files]
├── config.js              # Configuration helper
└── deployment-guide.md     # Documentation
```

## 🧪 **Testing Your Deployment**

1. **Visit**: https://srinivas-18.github.io/Secure-image-app/
2. **Test Authentication**: Register/login with Firebase
3. **Test Encryption**: Upload image → Set PIN → Encrypt
4. **Test Decryption**: Upload .enc/.meta files → Decrypt
5. **Test Log Activity**: Click "View Activity Log" → Authenticate → View logs

## 🔒 **Important Security Notes**

### **Before Going Live:**
1. **Remove wildcard CORS**: In `backend/app.py`, remove the `"*"` from origins list
2. **Use strong credentials**: Update LOG_USERNAME and LOG_PASSWORD
3. **Secure Firebase**: Ensure Firebase security rules are properly configured

### **Production CORS Configuration:**
```python
CORS(app, origins=[
    "https://srinivas-18.github.io",
    "https://srinivas-18.github.io/Secure-image-app/"
], supports_credentials=True)
```

## 🐛 **Troubleshooting**

### **Backend Not Connecting**
- Check if Render service is running
- Verify the backend URL in `index.html` matches your Render URL
- Check Render logs for errors

### **CORS Errors**
- Ensure your GitHub Pages URL is in the CORS origins list
- Redeploy backend after updating CORS settings
- Check browser console for specific CORS error messages

### **Log Modal Not Working**
- Verify backend `/authenticate_logs` endpoint is accessible
- Check that LOG_USERNAME and LOG_PASSWORD are set in Render environment
- Test with correct credentials

### **Firebase Authentication Issues**
- Ensure Firebase project is properly configured
- Check Firebase console for authentication settings
- Verify domain is added to Firebase authorized domains

## 📞 **Next Steps**

1. **Deploy Backend**: Set up Render with your backend code
2. **Update API URL**: Replace the placeholder URL with your actual Render URL
3. **Test Locally**: Test with production backend URL
4. **Deploy Frontend**: Push to GitHub and enable Pages
5. **Final Testing**: Test all functionality on the live site

Your app is now configured for GitHub Pages deployment! The log activity modal and all other features should work correctly once you complete the backend deployment.
