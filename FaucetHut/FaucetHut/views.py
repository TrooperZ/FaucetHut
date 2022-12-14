"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify
from FaucetHut import app
from app_script import faucetinfo
from .forms import addressChecker
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["69000 per day", "420 per hour"]
)

@app.route('/')
@app.route('/home')
def home():
    print('Loading home')
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
        minearn=round(minamt, 3),
        maxearn=round(maxamt, 3),
      gamelist=faucetinfo.returndata_nonf()
    )

@app.route('/api_faucet')
def faucet_api():
    print('Loading faucet api')  
    return jsonify(faucetinfo.returndata())

@app.route('/api_game')
def game_api():
    print('Loading game api') 
    return jsonify(faucetinfo.returndata_nonf())

@app.route('/api_info')
def apiinfo():
    print('Loading apiinfo')  
    return render_template(
        'api_info.html',
        title='API Info',
        year=datetime.now().year,
    )

@app.route('/banano.json')
def jsonban():
    print('Loading banano.json')  
    return render_template(
        'banano.json',
    )