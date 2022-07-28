"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FaucetHut import app
from app import faucetinfo

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
        acclist=faucetinfo.returndata(),

    )
