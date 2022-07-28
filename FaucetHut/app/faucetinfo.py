from dotenv import load_dotenv
import time
import datetime
import requests
import json
import concurrent
import cloudscraper
from fake_useragent import UserAgent
import pymongo
import os
load_dotenv()
ua = UserAgent()
mpass = os.getenv('MONGO_PASS')
client = pymongo.MongoClient(f"mongodb+srv://banfaucet:{mpass}@cluster0.qte9l.mongodb.net/?retryWrites=true&w=majority")
db = client['urls']
entries = db['entries']

statusDB = {}

ses = requests.Session()
ses.headers = {
    'referer': 'https://magiceden.io/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'accept': 'application/json'
}

scraper = cloudscraper.create_scraper(sess=ses, interpreter='nodejs')

import libs.bananopy as ban


intervals = (
    ("w", 604800),  # 60 * 60 * 24 * 7
    ("d", 86400),  # 60 * 60 * 24
    ("h", 3600),  # 60 * 60
    ("m", 60),
    ("s", 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append("{}{}".format(value, name))
    return ", ".join(result[:granularity])

def check_bal(acc):
    return str(round(ban.ban_from_raw(int(ban.get_account_balance(acc).balance)), 3)) + " BAN"

def last_tx(acc):
    history = ban.get_account_history(acc, 1).history
    class tx:
        timesincetx = display_time(int(time.time() - int(history[0]['local_timestamp'])))
        hashlink = "https://creeper.banano.cc/hash/" + history[0]['hash']
    return tx

def checksite_cmd(url):
    try:
       
        # pass the url into
        # request.hear
        headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        response = scraper.head(url, headers=headers)
         
        # check the status code
        if response.status_code == 200:
            return f"🟢 {response.status_code}"

        else:
            return f"🟡 {response.status_code}"

    except requests.ConnectionError as e:
        print(e)
        return "🔴 off"

def checksite(url):
    print(1)
    entryresult = entries.find_one({'url':url})
    if entryresult == None:
        status = checksite_cmd(url)
        entries.insert_one({'url':url, 'status':status, 'time':time.time()})
        return status
    if time.time() - entryresult['time'] > 10000:
        status = checksite_cmd(url)
        entries.update_one({'_id':entryresult['_id'],'url':url, 'status':status, 'time':time.time()})
        return status
        statusDB[url] = checksite_cmd(url)
    
    return entryresult['status']



