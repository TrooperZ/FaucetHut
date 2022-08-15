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
from replit import db

load_dotenv()
mpass = os.getenv('MONGO_PASS')
#client = pymongo.MongoClient(f"mongodb+srv://banfaucet:{mpass}@cluster0.qte9l.mongodb.net/?retryWrites=true&w=majority")
#db = client['urls']
#entries = db['entries']
data = []
scraper = cloudscraper.create_scraper()

urls = [
            "https://nanswap.com/get-free-banano?ref=tbanhut",
            "https://bananofaucet.cc/",
            "https://faucet.prussia.dev/",
            "https://banano-faucet.herokuapp.com/",
            "https://banfaucet.com/?r=23786",
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
            'https://www.cryptojungles.com/',
            'https://yet-another-ban-faucet.herokuapp.com/']

addrs = [
        "ban_36seefx46pwcpyp6a8kukybamqioam6a7jef88s8esjpubyc8urccebjqgyj",
        "ban_1faucetjuiyuwnz94j4c7s393r95sk5ac7p5usthmxct816osgqh3qd1caet",
        "ban_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps",
        "ban_3uf1gx114fqm9ppiwp3sw1mywzzr9d8uwhrw9e85zpgdt48eopruqnqpdb68",
        "ban_36aw66z9cnoraud94i7f77sfxahym6ks5ehf85pw495rrysm3cmy51xt54xs",
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
        "ban_3ze6byhismfpj8jhuda6fq1a7nkniq7t5soet9k58y3egt3rco66j69fdksg", 
        "ban_1monkeyt1x77a1rp9bwtthajb8odapbmnzpyt8357ac8a1bcron34i3r9y66",
        "ban_1monkecrqoqr6j6qzhtd9i8x49ujdnoqt7ramt9jmhd543icsrx5accoqtd5",
        "ban_33umod1td1x1szyjxj1a4c66j8s5escrii6ptnykz9axcsce93dqguwgwf78",
        "ban_1barre1777qqdcg86788tk6ojy9jmkyb8ridreezbgkhr7btnoqcntejrxhf",
        "ban_1zgdj86ohh7zbcoqkc8t7n15x9cnyfrefm6wsignd88xdozo9tsn8cg8jtsn",
        "ban_3sinkoff1yj9z5fougwao1gbjtsmb98u1j5p9kcrndqcc4irdxgzsjbem96e",
        "ban_3bdrip3ir5d9y3i1qi5z47pwcmd6jm39xzzzxnebrwfyoje63qa5dmnhm8f9",
        "ban_3tn9xt9sxbyw9injikki3yis5fbn6m47x37gco5cw6e6x6z7z4639cdgzke6",
        "ban_3eeq61ea33jdds5x37otx51esi8wsnxxjc8spjajyq7pj8h3nodkd19pride",
        "ban_3mkng3drofj13oo9dfpdgctayaskydr8t58j7pp6xo8564ko4y4ngboyyqxm",
        "ban_3f1o95qeeg1zignw11ew5sfaxhzogsj3hzm377xjtmab8hwz535p6f96i5uu"]
        
data =  [{'name': 'NanSwap Faucet', 'dur': '1 Day'},
            {'name': 'BananoFaucet.cc', 'dur': '1 Week'},
            {'name': 'Prussia Faucet', 'dur': '1 Day'},
            {'name': 'TNV Banano Faucet', 'dur': '1 Day'},
            {'name': 'Ban Faucet', 'dur': '5 mins'},
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
            {'name': 'Crypto Jungles', 'dur': '1 Day'},
            {'name': 'Yet Another Faucet', 'dur': '1 Day'}
    ]

g_urls = [
            "https://jungletv.live",
            "https://0xshay.itch.io/banano-swiper",
            "https://bananominer.com/",
            "https://bpow.banano.cc/",
            "https://volcano.coranos.cc/",
            "https://www.bananocrop.cc/"]

g_addrs = [
        "ban_1jung1eb3uomk1gsx7w6w7toqrikxm5pgn5wbsg5fpy96ckpdf6wmiuuzpca",
        "ban_3swiperfi43zpunak44hw6rfbrruwfj1aobm6gwjcbd65sy6b3kjfeunkjxc",
        "ban_3fo1d1ng6mfqumfoojqby13nahaugqbe5n6n3trof4q8kg5amo9mribg4muo",
        "ban_1boompow14irck1yauquqypt7afqrh8b6bbu5r93pc6hgbqs7z6o99frcuym",
        "ban_3j67xu1yuhfbezm7myw7bhzekj1mdzjkhhtctrqz5d9sanar8wt6hkgexzwn",
        "ban_1bananof7bbffdj8ssqkbo4gm81iro9g35d41h1tjrhx6ixshbb9r41sggza"]
        
g_data =  [{'name': 'JungleTV', 'des': 'Watch videos and earn Banano!'},
            {'name': 'Banano Swiper', 'des': 'Android game where you run and collect coins for Banano.'},
            {'name': 'BananoMiner', 'des': 'Earn Banano by Folding@Home for medical research.'},
            {'name': 'BoomPow', 'des': 'Perform proof of work calculations for Banano and earn.'},
            {'name': 'Volcano', 'des': 'Draw a picture, top pictures get rewards.'},
            {'name': 'BananoCrop', 'des': 'Play a variety of games and get paid in Banano daily.'}]

intervals = (
    ("w", 604800),  # 60 * 60 * 24 * 7
    ("d", 86400),  # 60 * 60 * 24
    ("h", 3600),  # 60 * 60
    ("m", 60),
    ("s", 1),
)

headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

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
    nameacc = f"lasttx{acc}"
    try:
      history = db[nameacc]
      if time.time() - history['time'] > 300:
        history = ban.get_account_history(acc, 100).history
        time.sleep(0.05)
        db[nameacc] = {'history':history, 'time':time.time()}  
    except KeyError or TypeError:
      history = ban.get_account_history(acc, 100).history
      time.sleep(0.05)
      db[nameacc] = {'history':history, 'time':time.time()}
    history = db[nameacc]['history']
    payoutamts_list = []
    for i in history:
        if i['type'] == "receive":
            continue
        payoutamts_list.append(float(i['amount_decimal']))
    class tx:
        timesincetx = display_time(int(time.time() - int(history[0]['local_timestamp'])))
        hashlink = "https://creeper.banano.cc/hash/" + history[0]['hash']
        payoutmin = formatNumber(round(min(payoutamts_list), 3))
        payoutmax = formatNumber(round(max(payoutamts_list), 3))
        hash = history[0]['hash']
    return tx

def check_bal(accs):
    bals = ban.get_accounts_balances(accs)
    return bals


def checksite_cmd(url):
    try:

        response = scraper.head(url, headers=headers)
         
        # check the status code
        if response.status_code == 200:
            return f"🟢 {response.status_code}"

        else:
            return f"🟡 {response.status_code}"

    except requests.ConnectionError as e:
        print(e)
        return "🔴 off"

def checksite(url, addr):
    #entryresult = entries.find_one({'url':url})
    try:
      entryresult = db[addr]
    except KeyError:
      status = checksite_cmd(url)
      db[addr] = {'status':status, 'time':time.time()}
      return status
    if time.time() - entryresult['time'] > 3600:
        status = checksite_cmd(url)
        db[addr] = {'status':status, 'time':time.time()}
        #entries.update_one({'_id':entryresult['_id']},{ "$set":{'_id':entryresult['_id'],'url':url, 'status':status, 'time':time.time()}})
        return status
    return entryresult['status']        

   


def returndata():
    index1 = 0
    balances = check_bal(addrs)

    with ThreadPoolExecutor(max_workers=10) as pool:
        returned1 = list(pool.map(checksite,urls,addrs))

    for (a, c, d) in zip(addrs, returned1, data):
        z = last_tx(a)
        d['status'] = c
        d['url'] = urls[index1] 
        d['paymin'] = z.payoutmin
        d['paymax'] = z.payoutmax        
        if a == "ban_36aw66z9cnoraud94i7f77sfxahym6ks5ehf85pw495rrysm3cmy51xt54xs":
          d['paymin'] = 0.00001
          d['paymax'] = 0.00006

        d['bal'] = round(float(balances[a]['balance_decimal']), 2) 
        d['lasttx_time'] = z.timesincetx
        d['lasttx_url'] = z.hashlink
        d['lasttx_hash'] = z.hash
        index1 = index1 + 1


    return data



def returndata_nonf():
    index1 = 0    
    balances = check_bal(g_addrs)

    with ThreadPoolExecutor(max_workers=10) as pool:
        returned1 = list(pool.map(checksite,g_urls,g_addrs))

    for (a, c, d) in zip(g_addrs, returned1, g_data):
        z = last_tx(a)
        d['status'] = c
        d['url'] = g_urls[index1] 
        d['paymin'] = z.payoutmin
        d['paymax'] = z.payoutmax        
      
        d['bal'] = round(float(balances[a]['balance_decimal']), 2) 
        d['lasttx_time'] = z.timesincetx
        d['lasttx_url'] = z.hashlink
        d['lasttx_hash'] = z.hash
        index1 = index1 + 1


    return g_data