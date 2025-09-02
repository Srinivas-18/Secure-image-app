# Deployment Guide - Secure Image Encryption App

## Prerequisites
- Vercel account (for frontend)
- Render account (for backend)
- Firebase project with Authentication, Firestore, and Storage enabled

## 1. Frontend Deployment (Vercel)

### Step 1: Prepare Frontend
```bash
cd frontend
npm install
npm run build
```

### Step 2: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository or upload the `frontend` folder
4. Set Framework Preset to "Vite"
5. Set Root Directory to `frontend`
6. Add Environment Variables:
   - `VITE_FIREBASE_API_KEY`: Your Firebase API key
   - `VITE_FIREBASE_AUTH_DOMAIN`: your-project.firebaseapp.com
   - `VITE_FIREBASE_PROJECT_ID`: your-project-id
   - `VITE_FIREBASE_STORAGE_BUCKET`: your-project.appspot.com
   - `VITE_FIREBASE_MESSAGING_SENDER_ID`: Your sender ID
   - `VITE_FIREBASE_APP_ID`: Your app ID
   - `VITE_API_URL`: https://your-render-app.onrender.com
7. Deploy

## 2. Backend Deployment (Render)

### Step 1: Prepare Backend
1. Ensure `requirements.txt` is complete
2. Update `render.yaml` with your environment variables

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Set Root Directory to `backend`
5. Set Build Command: `pip install -r requirements.txt`
6. Set Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`
7. Add Environment Variables:
   - `FLASK_SECRET_KEY`: Generate a secure random string
   - `FIREBASE_PROJECT_ID`: Your Firebase project ID
   - `DEBUG`: False
   - `GOOGLE_APPLICATION_CREDENTIALS`: (Optional - for Firebase Admin)

## 3. Firebase Configuration

### Update Firebase Settings
1. Go to Firebase Console → Authentication → Settings
2. Add authorized domains:
   - `your-vercel-app.vercel.app`
   - `localhost` (for local development)

### Firestore Security Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /activity_logs/{logId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### Storage Security Rules
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /uploads/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## 4. Post-Deployment Steps

1. Update `VITE_API_URL` in Vercel with your Render backend URL
2. Update CORS origins in `backend/app.py` to include your Vercel domain
3. Test authentication and file upload/download functionality
4. Monitor logs for any errors

## 5. Environment Variables Summary

### Frontend (.env)
```
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
VITE_API_URL=https://your-backend.onrender.com
```

### Backend (.env)
```
FLASK_SECRET_KEY=your_secure_secret_key
FIREBASE_PROJECT_ID=your_project_id
DEBUG=False
```

## Troubleshooting

### Common Issues:
1. **CORS errors**: Update CORS origins in `app.py`
2. **Firebase auth errors**: Check authorized domains
3. **File upload errors**: Verify Firebase Storage rules
4. **Build errors**: Check Node.js version compatibility

### Logs:
- Vercel: Check Function Logs in dashboard
- Render: Check Logs tab in service dashboard
- Firebase: Check Usage and Logs in console
