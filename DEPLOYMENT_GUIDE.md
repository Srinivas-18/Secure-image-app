# 🚀 Complete Deployment Guide

## **Step 1: Firebase Setup**

### **1.1 Create Firebase Project**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Name: `secure-image-encryption`
4. Enable Google Analytics (optional)

### **1.2 Enable Services**
1. **Authentication**:
   - Go to Authentication → Sign-in method
   - Enable "Email/Password"
   
2. **Firestore Database**:
   - Go to Firestore Database → Create database
   - Start in "test mode" for now
   
3. **Storage**:
   - Go to Storage → Get started
   - Start in "test mode"

### **1.3 Get Configuration**
1. Go to Project Settings (gear icon) → General tab
2. Scroll to "Your apps" → Click web icon `</>`
3. Register app name: `secure-image-encryption-web`
4. Copy the `firebaseConfig` object
5. Update `frontend/.env` with your actual values:

```env
VITE_FIREBASE_API_KEY=your-actual-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=your-app-id
```

## **Step 2: Backend Deployment (Render)**

### **2.1 Prepare for Render**
1. Create GitHub repository for your project
2. Push code to GitHub
3. Go to [Render.com](https://render.com/) → Sign up/Login

### **2.2 Deploy Backend**
1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Settings:
   - **Name**: `secure-image-encryption-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### **2.3 Environment Variables on Render**
Add these in Render dashboard:
```
FLASK_SECRET_KEY=qwertyuiopasdfghjklzxcvbnm1234567890
DEBUG=False
HOST=0.0.0.0
PORT=10000
FIREBASE_PROJECT_ID=your-project-id
```

## **Step 3: Frontend Deployment (Vercel)**

### **3.1 Prepare for Vercel**
1. Go to [Vercel.com](https://vercel.com/) → Sign up/Login
2. Install Vercel CLI: `npm i -g vercel`

### **3.2 Deploy Frontend**
1. Click "New Project"
2. Import from GitHub
3. Settings:
   - **Framework Preset**: `Other`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### **3.3 Environment Variables on Vercel**
Add these in Vercel dashboard:
```
VITE_FIREBASE_API_KEY=your-actual-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=your-app-id
VITE_API_URL=https://your-render-app.onrender.com
```

## **Step 4: Final Configuration**

### **4.1 Update Firebase Security Rules**
In Firebase Console:

**Firestore Rules**:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /activity_logs/{document} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
    }
  }
}
```

**Storage Rules**:
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## **Step 5: Test Deployment**

1. **Test Firebase Auth**: Register/Login on deployed frontend
2. **Test API Connection**: Encrypt an image
3. **Test File Storage**: Check Firebase Storage console
4. **Test Logs**: Check Firestore console

## **Architecture Overview**

```
User → Vercel (Frontend) → Render (Backend API) → Firebase (Auth/Storage/DB)
```

- **Frontend**: Static files on Vercel CDN
- **Backend**: Python Flask API on Render
- **Files**: Encrypted files in Firebase Storage
- **Data**: User profiles & logs in Firestore
- **Auth**: Firebase Authentication

## **URLs After Deployment**
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.onrender.com`
- **Firebase**: Managed by Google

Ready to deploy! 🚀
