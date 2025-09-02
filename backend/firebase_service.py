import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
from datetime import datetime
import tempfile

class FirebaseService:
    def __init__(self):
        # Initialize Firebase Admin SDK
        if not firebase_admin._apps:
            # For local development, use service account key
            # For production, use environment variables
            try:
                cred = credentials.Certificate("firebase-service-account.json")
                firebase_admin.initialize_app(cred, {
                    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
                })
            except:
                # Fallback for production deployment or local testing
                try:
                    firebase_admin.initialize_app()
                except:
                    # Skip Firebase for local development if not configured
                    pass
        
        try:
            self.db = firestore.client()
            self.bucket = storage.bucket()
        except:
            # Fallback for local development
            self.db = None
            self.bucket = None
    
    def upload_file(self, file_data, file_path, user_id):
        """Upload file to Firebase Storage"""
        try:
            blob = self.bucket.blob(f"users/{user_id}/{file_path}")
            blob.upload_from_string(file_data)
            blob.make_public()
            return {"success": True, "url": blob.public_url, "path": blob.name}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def download_file(self, file_path):
        """Download file from Firebase Storage"""
        try:
            blob = self.bucket.blob(file_path)
            return {"success": True, "data": blob.download_as_bytes()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_file(self, file_path):
        """Delete file from Firebase Storage"""
        try:
            blob = self.bucket.blob(file_path)
            blob.delete()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def log_activity(self, user_id, activity_type, details):
        """Log user activity to Firestore"""
        try:
            doc_ref = self.db.collection('activity_logs').document()
            doc_ref.set({
                'userId': user_id,
                'activityType': activity_type,
                'details': details,
                'timestamp': datetime.now(),
                'ip': None  # Can be added from request context
            })
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_logs(self, user_id):
        """Get user activity logs from Firestore"""
        try:
            docs = self.db.collection('activity_logs')\
                          .where('userId', '==', user_id)\
                          .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                          .limit(100)\
                          .stream()
            
            logs = []
            for doc in docs:
                log_data = doc.to_dict()
                logs.append({
                    'id': doc.id,
                    'timestamp': log_data.get('timestamp'),
                    'activityType': log_data.get('activityType'),
                    'details': log_data.get('details')
                })
            return {"success": True, "logs": logs}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_user_profile(self, user_id, email):
        """Create user profile in Firestore"""
        try:
            doc_ref = self.db.collection('users').document(user_id)
            doc_ref.set({
                'email': email,
                'createdAt': datetime.now(),
                'encryptionCount': 0,
                'lastActivity': datetime.now()
            })
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_encryption_count(self, user_id):
        """Increment user's encryption count"""
        try:
            doc_ref = self.db.collection('users').document(user_id)
            doc_ref.update({
                'encryptionCount': firestore.Increment(1),
                'lastActivity': datetime.now()
            })
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Global instance
firebase_service = FirebaseService()
