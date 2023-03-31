"""
The flask application package.
"""

from flask import Flask
from .config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

import FaucetHut.views