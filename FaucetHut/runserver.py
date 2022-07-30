"""
This script runs the FaucetHut application using a development server.
"""

from os import environ
from FaucetHut import app

if __name__ == '__main__':
    app.run('0.0.0.0', '5000')
