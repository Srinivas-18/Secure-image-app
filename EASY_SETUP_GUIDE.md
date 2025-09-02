# 🚀 Easy Setup Guide for Beginners

Since you're new to Firebase and deployment, here's a **step-by-step beginner guide**:

## **Part 1: Firebase Setup (15 minutes)**

### **Step 1: Create Firebase Account**
1. Go to https://console.firebase.google.com/
2. Sign in with Google account
3. Click **"Create a project"**
4. Project name: `secure-image-encryption`
5. Disable Google Analytics (simpler for now)
6. Click **"Create project"**

### **Step 2: Enable Services**
**Authentication:**
1. Left sidebar → **Authentication**
2. Click **"Get started"**
3. **Sign-in method** tab → **Email/Password** → **Enable** → **Save**

**Firestore Database:**
1. Left sidebar → **Firestore Database**
2. Click **"Create database"**
3. **Start in test mode** → **Next**
4. Choose location (default is fine) → **Done**

**Storage:**
1. Left sidebar → **Storage**
2. Click **"Get started"**
3. **Start in test mode** → **Next**
4. Choose location → **Done**

### **Step 3: Get Your Config**
1. Left sidebar → **Project Overview** (house icon)
2. Click **"Project settings"** (gear icon)
3. Scroll down to **"Your apps"**
4. Click **web icon** `</>`
5. App nickname: `secure-image-encryption-web`
6. Click **"Register app"**
7. **COPY** the `firebaseConfig` object (looks like this):

```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-12345",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

8. **PASTE** these values into `frontend/.env`:

```env
VITE_FIREBASE_API_KEY=AIza...
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-12345
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abc123
```

## **Part 2: GitHub Setup (5 minutes)**

### **Step 1: Create GitHub Account**
1. Go to https://github.com/
2. Sign up if you don't have an account

### **Step 2: Create Repository**
1. Click **"New repository"**
2. Repository name: `secure-image-encryption`
3. Make it **Public**
4. Click **"Create repository"**

### **Step 3: Upload Your Code**
1. Download **GitHub Desktop** or use web interface
2. **Web method**: Click **"uploading an existing file"**
3. Drag your entire project folder
4. Commit message: `Initial commit`
5. Click **"Commit changes"**

## **Part 3: Render Deployment (Backend) (10 minutes)**

### **Step 1: Create Render Account**
1. Go to https://render.com/
2. Sign up with GitHub account

### **Step 2: Deploy Backend**
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. **Settings:**
   - Name: `secure-image-encryption-api`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`

### **Step 3: Add Environment Variables**
In Render dashboard → Environment:
```
FLASK_SECRET_KEY = qwertyuiopasdfghjklzxcvbnm1234567890
DEBUG = False
FIREBASE_PROJECT_ID = your-project-12345
```

4. Click **"Create Web Service"**
5. **COPY** your backend URL (e.g., `https://your-app.onrender.com`)

## **Part 4: Vercel Deployment (Frontend) (10 minutes)**

### **Step 1: Create Vercel Account**
1. Go to https://vercel.com/
2. Sign up with GitHub account

### **Step 2: Deploy Frontend**
1. Click **"New Project"**
2. Import your GitHub repository
3. **Settings:**
   - Framework Preset: `Other`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

### **Step 3: Add Environment Variables**
In Vercel dashboard → Settings → Environment Variables:
```
VITE_FIREBASE_API_KEY = AIza...
VITE_FIREBASE_AUTH_DOMAIN = your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID = your-project-12345
VITE_FIREBASE_STORAGE_BUCKET = your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID = 123456789
VITE_FIREBASE_APP_ID = 1:123456789:web:abc123
VITE_API_URL = https://your-render-app.onrender.com
```

4. Click **"Deploy"**

## **Part 5: Final Configuration (5 minutes)**

### **Update Firebase Security Rules**

**Firestore Rules** (Database → Rules):
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /activity_logs/{document} {
      allow read, write: if request.auth != null;
    }
  }
}
```

**Storage Rules** (Storage → Rules):
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

## **🎉 You're Done!**

Your app is now live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.onrender.com`

**Test it:**
1. Register a new account
2. Upload and encrypt an image
3. Download and decrypt it
4. Check Firebase console to see stored files and logs

**Need help?** Each service has excellent documentation and support!
