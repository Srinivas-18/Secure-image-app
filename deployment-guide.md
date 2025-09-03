# 🚀 Deployment Guide for Secure Image Encryption App

## 📋 Pre-Deployment Checklist

### 1. **Backend Deployment (Render.com)**

1. **Create Render Account** and connect your GitHub repository
2. **Create Web Service** with these settings:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Environment**: Python 3
   - **Instance Type**: Free tier is sufficient for testing

3. **Set Environment Variables** in Render dashboard:
   ```
   FLASK_SECRET_KEY=your-super-secure-secret-key-here
   LOG_USERNAME=admin
   LOG_PASSWORD=your-secure-log-password
   DEBUG=False
   HOST=0.0.0.0
   PORT=10000
   ```

4. **Update Backend URL** in your frontend code:
   - Replace `https://secure-image-encryption-backend.onrender.com` with your actual Render URL
   - Update line 1049 in `index.html`

### 2. **Frontend Deployment (Netlify)**

1. **Create Netlify Account** and connect your GitHub repository
2. **Deploy Settings**:
   - **Build Command**: Leave empty (static site)
   - **Publish Directory**: `/` (root directory)
   - **Build Settings**: Auto-detect

3. **Configure Redirects** - Create `_redirects` file:
   ```
   /*    /index.html   200
   ```

### 3. **CORS Configuration**

Update `backend/app.py` with your actual frontend URL:
```python
CORS(app, origins=[
    "http://localhost:3000", 
    "http://localhost:5000",
    "https://your-netlify-site.netlify.app",  # Replace with actual URL
    "https://your-custom-domain.com"  # If using custom domain
], supports_credentials=True)
```

## 🔧 **Fixed Issues**

### ✅ **Backend Connectivity**
- Added dynamic API URL detection
- Fixed CORS configuration for production
- Added proper error handling for API calls

### ✅ **Log Activity Modal**
- Fixed missing JavaScript functionality
- Added proper modal styling and behavior
- Connected to backend `/authenticate_logs` and `/get_logs` endpoints
- Added loading states and error handling

### ✅ **File Upload & Processing**
- Added file validation and preview
- Fixed encryption/decryption form handlers
- Added progress indicators and result display
- Proper error messaging for failed operations

### ✅ **PIN Strength Validation**
- Real-time PIN strength checking
- Visual feedback with color coding
- Connected to backend validation endpoint

## 📁 **File Structure for Deployment**

```
project/
├── index.html              # Main frontend file (deploy this)
├── backend/                # Deploy to Render
│   ├── app.py
│   ├── requirements.txt
│   └── [other backend files]
├── config.js              # Configuration helper
├── deployment-guide.md     # This guide
└── .env.example           # Environment template
```

## 🌐 **Deployment Steps**

### **Step 1: Deploy Backend to Render**
1. Push your code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set build/start commands as specified above
5. Add environment variables
6. Deploy and note the URL (e.g., `https://your-app-name.onrender.com`)

### **Step 2: Update Frontend Configuration**
1. Update the backend URL in `index.html` line 1049
2. Test locally with the production backend URL

### **Step 3: Deploy Frontend to Netlify**
1. Create new site from Git on Netlify
2. Connect your repository
3. Deploy with default settings
4. Note the frontend URL (e.g., `https://your-site.netlify.app`)

### **Step 4: Update CORS Settings**
1. Update `backend/app.py` with your Netlify URL
2. Redeploy backend on Render

## 🧪 **Testing Your Deployment**

1. **Authentication**: Test Firebase login/register
2. **Encryption**: Upload image, set PIN, encrypt
3. **Decryption**: Upload .enc and .meta files, decrypt
4. **Log Activity**: Click "View Activity Log" button, authenticate, view logs
5. **PIN Strength**: Test real-time PIN validation

## 🔒 **Security Notes**

- Remove `"*"` from CORS origins in production
- Use strong environment variables
- Enable HTTPS only in production
- Regularly rotate secret keys

## 🐛 **Troubleshooting**

### **Backend Not Working**
- Check Render logs for errors
- Verify environment variables are set
- Ensure build/start commands are correct

### **CORS Errors**
- Verify frontend URL is in CORS origins
- Check for typos in URLs
- Ensure both HTTP and HTTPS variants if needed

### **Log Modal Not Opening**
- Check browser console for JavaScript errors
- Verify backend `/authenticate_logs` endpoint is working
- Test with correct credentials (from environment variables)

## 📞 **Support**

If issues persist:
1. Check browser developer console for errors
2. Check Render deployment logs
3. Verify all URLs are correctly configured
4. Test API endpoints directly using tools like Postman
