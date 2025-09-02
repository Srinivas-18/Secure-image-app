#!/usr/bin/env python3
"""
Startup script for the Image Encryption Web Application
"""
import os
import sys

# Get the root directory
root_dir = os.path.dirname(os.path.abspath(__file__))

# Add backend directory to Python path
backend_dir = os.path.join(root_dir, 'backend')
sys.path.insert(0, backend_dir)

# Set working directory to root for proper relative paths
os.chdir(root_dir)

# Import and run the Flask app
from backend.app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
