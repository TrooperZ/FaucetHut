from dotenv import load_dotenv
import time
import datetime
import concurrent
import cloudscraper
import pymongo
import os
from concurrent.futures import ThreadPoolExecutor
import asyncio
import libs.bananopy as ban
import requests

load_dotenv()
mpass = os.getenv('MONGO_PASS')
client = pymongo.MongoClient(f"mongodb+srv://banfaucet:{mpass}@cluster0.qte9l.mongodb.net/?retryWrites=true&w=majority")
db = client['urls']
entries = db['entries']

scraper = cloudscraper.create_scraper()




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


def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num

def last_tx(acc):
    history = ban.get_account_history(acc, 100).history
    payoutamts_list = []
    for i in history:
        if i['type'] == "receive":
            continue
        payoutamts_list.append(float(i['amount_decimal']))
    class tx:
        timesincetx = display_time(int(time.time() - int(history[0]['local_timestamp'])))
        hashlink = "https://creeper.banano.cc/hash/" + history[0]['hash']
        payoutamts = str(formatNumber(round(min(payoutamts_list), 3))) + "-" + str(formatNumber(round(max(payoutamts_list), 3)))
    return tx

def check_bal(accs):
    bals = ban.get_accounts_balances(accs)
    return bals


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
    entryresult = entries.find_one({'url':url})
    if entryresult == None:
        status = checksite_cmd(url)
        entries.insert_one({'url':url, 'status':status, 'time':time.time()})
        return status
    if time.time() - entryresult['time'] > 8000:
        status = checksite_cmd(url)
        entries.update_one({'_id':entryresult['_id']},{ "$set":{'_id':entryresult['_id'],'url':url, 'status':status, 'time':time.time()}})
        return status
    return entryresult['status']        

   


def returndata():
    index1 = 0
    urls = [
            "https://nanswap.com/get-free-banano?ref=tbanhut",
            "https://bananofaucet.cc/",
            "https://faucet.prussia.dev/",
            "https://banano-faucet.herokuapp.com/",
            "https://getbanano.cc/",
            "https://bananoplanet.cc/faucet",
            "https://www.banbucket.ninja",
            "https://faucet.bananotime.com/",
            "https://gorillanation.ga/",
            "https://gobanano.com/home",
            "https://www.bananofaucet.club/",
            "https://getban.csquared.nz/",
            "https://bonobo.cc/faucet",
            "https://faucet.banoboto.repl.co/",
            'https://baucarp.herokuapp.com/',
            'https://www.only-bans.cc/',
            'https://ban.earns.cc/',
            'https://monkeytalks.cc/t',
            'https://icanhaznano.monke42.tk/',
            'https://trybanano.com/',
            'https://www.devinmontes.com/',
            'https://banhub.com/',
            'https://faucet.bananoforest.com/',
            'https://bananodrip.com/',
            'https://banfaucet.perrypal21.repl.co/',
            'https://pronouns.h.prussiafan.club/',
            'https://www.cryptojungles.com/']

    addrs = [
        "ban_36seefx46pwcpyp6a8kukybamqioam6a7jef88s8esjpubyc8urccebjqgyj",
        "ban_1faucetjuiyuwnz94j4c7s393r95sk5ac7p5usthmxct816osgqh3qd1caet",
        "ban_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps",
        "ban_3uf1gx114fqm9ppiwp3sw1mywzzr9d8uwhrw9e85zpgdt48eopruqnqpdb68",
        "ban_1rp3ke75c8a3t5mkzekibo8w4mxzydrie8xzwqmkajfk9ww76f7wzbhd5bmt",
        "ban_3p1anetee7arfx9zbmspwf9c8c5r88wy6zkgwcbt7rndtcqsoj6fzuy11na3",
        "ban_1j3rqseffoin7x5z5y1ehaqe1n7todza41kdf4oyga8phps3ea31u39ruchu",
        "ban_39665maxw96iifne3izma1icdmomxy3o5z35hqzh9s13xw7si4opp5xxyg8g",
        "ban_1gori11a7fz3tee6aydqxcehttzbuk93pjsctanfkgqmesa3dmo1cyw89xex",
        "ban_3w91yp9ufjhpzt98xzddfmnoo8bm51ic3fp3mmx4mqbocqqde7dii1w8g4b6",
        "ban_3rzg5w93ipik4aie3uzafetsfa6dnqdrrsmw9c9dussge7eb5s45xmh4o4pa",
        "ban_3jyqzypmcn94dmyp7eb3k85sug1568xwehzx738o5jniaxaf1jpxdakjz96r",
        "ban_3faubo4bfzexkbodi67c74ut1a6it64chofgobbag87yfmy1x457jbsdccd4",
        "ban_3jzi3modbcrfq7gds5nmudstw3kghndqb1k48twhqxds3ytyj4k7cf79q5ij",
        "ban_3x8hzeb8spb6e36y7yjgo6esmeahgphq1mhp545ofouuu5enrne5nzwkdasb",
        "ban_1on1ybanskzzsqize1477wximtkdzrftmxqtajtwh4p4tg1w6awn1hq677cp",
        "ban_396zzoypz8pabdtagh5enoa55pu7izwmzzf3a1qp5shmtqfbc8cxsfrfsgzj", #NOT EARNS.CC ACCOUNT
        "ban_1monkeyt1x77a1rp9bwtthajb8odapbmnzpyt8357ac8a1bcron34i3r9y66",
        "ban_1monkecrqoqr6j6qzhtd9i8x49ujdnoqt7ramt9jmhd543icsrx5accoqtd5",
        "ban_33umod1td1x1szyjxj1a4c66j8s5escrii6ptnykz9axcsce93dqguwgwf78",
        "ban_1barre1777qqdcg86788tk6ojy9jmkyb8ridreezbgkhr7btnoqcntejrxhf",
        "ban_1zgdj86ohh7zbcoqkc8t7n15x9cnyfrefm6wsignd88xdozo9tsn8cg8jtsn",
        "ban_3sinkoff1yj9z5fougwao1gbjtsmb98u1j5p9kcrndqcc4irdxgzsjbem96e",
        "ban_3bdrip3ir5d9y3i1qi5z47pwcmd6jm39xzzzxnebrwfyoje63qa5dmnhm8f9",
        "ban_3tn9xt9sxbyw9injikki3yis5fbn6m47x37gco5cw6e6x6z7z4639cdgzke6",
        "ban_3eeq61ea33jdds5x37otx51esi8wsnxxjc8spjajyq7pj8h3nodkd19pride",
        "ban_3mkng3drofj13oo9dfpdgctayaskydr8t58j7pp6xo8564ko4y4ngboyyqxm"]
        
    data =  [{'name': 'NanSwap Faucet', 'dur': '1 Day'},
            {'name': 'BananoFaucet.cc', 'dur': '1 Week'},
            {'name': 'Prussia Faucet', 'dur': '1 Day'},
            {'name': 'TNV Banano Faucet', 'dur': '1 Day'},
            {'name': "iMalFect's faucet", 'dur': '1 Week'},
            {'name': 'BananoPlanet.cc', 'dur': '2 Hours'},
            {'name': 'BanBucket Ninja', 'dur': '15 Hours'},
            {'name': 'BananoTime', 'dur': 'N/A'},
            {'name': 'GorillaNation', 'dur': '1 Day'},
            {'name': 'GoBanano', 'dur': '1 Day', 'pay': 'N/A'},
            {'name': 'BananoFaucet.club', 'dur': '1 Day'},
            {'name': 'CSquared', 'dur': '1 Day'},
            {'name': 'Bonobo', 'dur': '1 Week'},
            {'name': 'Banboto\'s Future Faucet', 'dur': '1 Day'},
            {'name': 'Baucarp Faucet', 'dur': '1 Day'},
            {'name': 'OnlyBans Faucet', 'dur': '1 Day'},
            {'name': 'Earns.cc Faucet', 'dur': '1 Day'},
            {'name': 'MonkeyTalks Faucet', 'dur': '1 Day'},
            {'name': 'icanhaznano monke42 faucet', 'dur': '1 Day'},
            {'name': 'TryBanano', 'dur': '1 Day'},
            {'name': 'Barrel O\' Bananos', 'dur': 'N/A'},
            {'name': 'BanHub', 'dur': '1 Day'},
            {'name': 'BananoForest', 'dur': '1 Day'},
            {'name': 'BananoDrip', 'dur': '1 Day'},
            {'name': 'PerryPal', 'dur': '1 Day'},
            {'name': 'Pronouns Faucet', 'dur': '1 Day'},
            {'name': 'Crypto Jungles', 'dur': '1 Day'}
    ]
    balances = check_bal(addrs)

    with ThreadPoolExecutor(max_workers=10) as pool:
        returned = list(pool.map(checksite,urls))

    for (a, c, d) in zip(addrs, returned, data):
        d['status'] = c
        d['url'] = urls[index1] 
        if a == "N/A":
            d['bal'] = "N/A"
            d['lasttx'] = "N/A"
            d['lasttx_hash'] = "N/A"
            d['pay'] = "N/A"
        else:
            lasttx = last_tx(a)
            d['pay'] = lasttx.payoutamts
            d['bal'] = round(float(balances[a]['balance_decimal']), 2) 
            d['lasttx'] = lasttx.timesincetx
            d['lasttx_hash'] = lasttx.hashlink
        index1 = index1 + 1


    return data


