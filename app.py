"""Top-level Flask entrypoint for hosting (e.g. Render, Vercel, Gunicorn).

This file exposes the Flask `app` object so platform builders that look
for a root-level entrypoint (app.py, main.py, index.py, etc.) can find it.
It sets up the Python path to include the backend directory, then imports
the app instance from `backend/app.py`.
"""
import os
import sys

# Add backend directory to Python path so imports work correctly
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Now import the app
from backend.app import app


if __name__ == '__main__':
    # Run locally for development
    app.run(host='0.0.0.0', port=5500, debug=False)
