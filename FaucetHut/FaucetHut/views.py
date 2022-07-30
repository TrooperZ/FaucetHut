"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify
from FaucetHut import app
from app import faucetinfo
from .forms import addressChecker



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    data = faucetinfo.returndata()
    minamt = 0
    maxamt = 0
    for i in data:
        minamt += i['paymin']
        maxamt += i['paymax']
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
        acclist=data,
        minearn=minamt,
        maxearn=maxamt,
    )

@app.route('/api')
def testpost():
    return jsonify(faucetinfo.returndata())