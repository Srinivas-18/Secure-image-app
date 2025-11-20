"""Top-level Flask entrypoint for hosting (e.g. Vercel, Gunicorn).

This file exposes the Flask `app` object so platform builders that look
for a root-level entrypoint (app.py, main.py, index.py, etc.) can find it.
It simply imports the `app` instance defined in `backend/app.py`.
"""
from backend.app import app


if __name__ == '__main__':
    # Run locally for development
    app.run(host='0.0.0.0', port=5500, debug=False)
