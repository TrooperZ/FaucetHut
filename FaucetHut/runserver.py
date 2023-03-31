
"""
This script runs the FaucetHut application using a development server.
"""

from os import environ
from FaucetHut import app

if __name__ == '__main__':
    from waitress import serve
    print("Running server on 8080")
    serve(app, host="0.0.0.0", port=8080)