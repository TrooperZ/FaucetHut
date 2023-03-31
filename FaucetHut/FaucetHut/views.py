"""
Routes and views for the flask application.
"""

from datetime import datetime
from FaucetHut import app
from app_script import faucetinfo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, render_template
from flask import jsonify
import ast

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
    data = faucetinfo.returndata(True)
    minamt = 0
    maxamt = 0
    for i in data:
        minamt += i['paymin']
        maxamt += i['paymax']

    return render_template(
        'index_min.html',
        title='Home',
        year=datetime.now().year,
        acclist=data,
        minearn=round(minamt, 3),
        maxearn=round(maxamt, 3),
      gamelist=faucetinfo.returngamedata(True)
    )

@app.route('/api_faucet')
def faucet_api():
    print('Loading faucet api')  
    data = str(faucetinfo.returndata(False))
    data = data.replace("ObservedDict(value=", "")
    data = data.replace("ObservedList(value=", "")
    data = data.replace(")", "")
    return jsonify(ast.literal_eval(data))

@app.route('/api_game')
def game_api():
    print('Loading game api') 
    data = str(faucetinfo.returngamedata(False))
    data = data.replace("ObservedDict(value=", "")
    data = data.replace("ObservedList(value=", "")
    data = data.replace(")", "")
    return jsonify(ast.literal_eval(data))

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