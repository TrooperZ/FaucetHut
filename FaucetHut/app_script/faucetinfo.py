import time
import libs.bananopy as ban
import requests
from replit import db
import threading
import ast
import base64
import cloudscraper

requests.packages.urllib3.disable_warnings()

with open('/home/runner/FaucetHut/FaucetHut/app_script/faucets.txt') as f:
  encodedData = f.read()
  data = ast.literal_eval(base64.b64decode(encodedData).decode('utf-8'))

with open('/home/runner/FaucetHut/FaucetHut/app_script/games.txt') as f:
  encodedData = f.read()
  gdata = ast.literal_eval(base64.b64decode(encodedData).decode('utf-8'))

faucets = data

games = gdata

scraper = requests

intervals = (
  ("w", 604800),  # 60 * 60 * 24 * 7
  ("d", 86400),  # 60 * 60 * 24
  ("h", 3600),  # 60 * 60
  ("m", 60),
  ("s", 1),
)

headers = {
  'User-Agent':
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


def display_time(seconds, granularity=2):
  result = []

  for name, count in intervals:
    value = seconds // count
    if value:
      seconds -= value * count
      result.append("{}{}".format(value, name))
  return ", ".join(result[:granularity])


def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num


def last_tx(acc):
  history = ban.get_account_history(acc, 80).history
  time.sleep(0.01)

  payoutamts_list = []
  for i in history:
    if i['type'] == "recieve":
      continue
    payoutamts_list.append(float(i['amount_decimal']))

  class tx:
    timesincetx = display_time(
      int(time.time() - int(history[0]['local_timestamp'])))
    hashlink = "https://creeper.banano.cc/hash/" + history[0]['hash']
    payoutmin = formatNumber(round(min(payoutamts_list), 3))
    payoutmax = formatNumber(round(max(payoutamts_list), 3))
    hash = history[0]['hash']

  return tx


def check_bal(accs):
  bals = ban.get_accounts_balances(accs)
  return bals


def checksite(url, isSite):
  code = 0
  try:

    response = scraper.head(url, headers=headers, timeout=5, verify=False)

    code = int(response.status_code)

  except requests.ConnectionError as e:
    print(e)
    if "SSLError" in str(e):
      print("SSL Error, ignoring and returning 201")
      code = 201
    else:
      code = 0

  except requests.ReadTimeout:
    code = 404

  if isSite:
    if code == 200:
      return "🟢 200"
    elif code == 404:
      code = "🔴 404"
    elif code == 0:
      code = "🔴 off"
    else:
      code = f"🟡 {code}"

  return code

def fetchdata(isSite):
  addrList = []

  for entry in faucets:
    addrList.append(entry['address'])
    entry['status'] = checksite(entry['url'], isSite)

    lastTxData = last_tx(entry['address'])

    entry['paymin'] = lastTxData.payoutmin
    entry['paymax'] = lastTxData.payoutmax

    if entry[
        'address'] == "ban_36aw66z9cnoraud94i7f77sfxahym6ks5ehf85pw495rrysm3cmy51xt54xs":
      entry['paymin'] = 0.00001
      entry['paymax'] = 0.00006

    entry['lasttx_time'] = lastTxData.timesincetx
    entry['lasttx_url'] = lastTxData.hashlink
    entry['lasttx_hash'] = lastTxData.hash

  balances = check_bal(addrList)

  for entry in faucets:
    entry['bal'] = round(float(balances[entry['address']]['balance_decimal']),
                         2)

  return faucets


def returndata(isSite):

  key = 'savedAPIData'
  if isSite:
    key = 'savedSiteData'

  try:
    data = dict(db.get(key))
    if time.time() - data['time'] > 3600:
      db[key] = {'time': time.time(), 'data': fetchdata(isSite)}
      data = dict(db.get(key))
  except:
    db[key] = {'time': time.time(), 'data': fetchdata(isSite)}
    data = dict(db.get(key))

  return data['data']


def fetchgamedata(isSite):
  addrList = []

  for entry in games:
    addrList.append(entry['address'])
    entry['status'] = checksite(entry['url'], isSite)

  

    lastTxData = last_tx(entry['address'])
    entry['lasttx_time'] = lastTxData.timesincetx
    entry['lasttx_url'] = lastTxData.hashlink
    entry['lasttx_hash'] = lastTxData.hash
    entry['paymin'] = lastTxData.payoutmin
    entry['paymax'] = lastTxData.payoutmax

  balances = check_bal(addrList)
  
  for entry in games:
    entry['bal'] = round(float(balances[entry['address']]['balance_decimal']),
                         2)

  return games


def returngamedata(isSite):
  key = 'savedGAPIData'
  if isSite:
    key = 'savedGSiteData'

  try:
    data = db.get(key)
    if time.time() - data['time'] > 3600:
      db[key] = {'time': time.time(), 'data': fetchgamedata(isSite)}
      data = db.get(key)
  except:
    db[key] = {'time': time.time(), 'data': fetchgamedata(isSite)}
    data = db.get(key)


  return data['data']


class BackgroundTasks(threading.Thread):

  def run(self, *args, **kwargs):
    while True:
      print("Gathering Periodic Refresh Data...")
      returndata(True)
      returngamedata(True)
      returndata(False)
      returngamedata(False)
      time.sleep(3600)

  # updates data that takes a long time to get every hour in background if not a lot of people are active


if __name__ != "__main__":

  t = BackgroundTasks()
  t.start()
