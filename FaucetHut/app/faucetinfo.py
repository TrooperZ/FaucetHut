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
from concurrent.futures import ThreadPoolExecutor

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
            'https://faucet.bananotime.com/',
            'https://banfaucet.perrypal21.repl.co/',
            'https://pronouns.h.prussiafan.club/',
            'https://www.cryptojungles.com/']
        
    data =  [{'name': 'NanSwap Faucet', 'dur': '1 Day', 'pay': '0.1 BAN', 'bal': check_bal("ban_36seefx46pwcpyp6a8kukybamqioam6a7jef88s8esjpubyc8urccebjqgyj"), 'lasttx': last_tx("ban_36seefx46pwcpyp6a8kukybamqioam6a7jef88s8esjpubyc8urccebjqgyj").timesincetx, 'lasttx_hash': last_tx("ban_36seefx46pwcpyp6a8kukybamqioam6a7jef88s8esjpubyc8urccebjqgyj").hashlink, 'url':'https://nanswap.com/?ref=tbanhut'},
            {'name': 'BananoFaucet.cc', 'dur': '1 Week', 'pay': '0-42 BAN', 'bal': check_bal("ban_1faucetjuiyuwnz94j4c7s393r95sk5ac7p5usthmxct816osgqh3qd1caet"), 'lasttx': last_tx("ban_1faucetjuiyuwnz94j4c7s393r95sk5ac7p5usthmxct816osgqh3qd1caet").timesincetx, 'lasttx_hash': last_tx("ban_1faucetjuiyuwnz94j4c7s393r95sk5ac7p5usthmxct816osgqh3qd1caet").hashlink, 'url':'https://bananofaucet.cc/'},
            {'name': 'Prussia Faucet', 'dur': '1 Day', 'pay': '0.01-0.1 BAN', 'bal': check_bal("ban_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps"), 'lasttx': last_tx("ban_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps").timesincetx, 'lasttx_hash': last_tx("ban_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps").hashlink, 'url':'https://faucet.prussia.dev/'},
            {'name': 'TNV Banano Faucet', 'dur': '1 Day', 'pay': '0.04 BAN', 'bal': check_bal("ban_3uf1gx114fqm9ppiwp3sw1mywzzr9d8uwhrw9e85zpgdt48eopruqnqpdb68"), 'lasttx': last_tx("ban_3uf1gx114fqm9ppiwp3sw1mywzzr9d8uwhrw9e85zpgdt48eopruqnqpdb68").timesincetx, 'lasttx_hash': last_tx("ban_3uf1gx114fqm9ppiwp3sw1mywzzr9d8uwhrw9e85zpgdt48eopruqnqpdb68").hashlink, 'url':'https://banano-faucet.herokuapp.com/'},
            {'name': "iMalFect's faucet", 'dur': '1 Week', 'pay': 'Varied', 'bal': check_bal("ban_1rp3ke75c8a3t5mkzekibo8w4mxzydrie8xzwqmkajfk9ww76f7wzbhd5bmt"), 'lasttx': last_tx("ban_1rp3ke75c8a3t5mkzekibo8w4mxzydrie8xzwqmkajfk9ww76f7wzbhd5bmt").timesincetx, 'lasttx_hash': last_tx("ban_1rp3ke75c8a3t5mkzekibo8w4mxzydrie8xzwqmkajfk9ww76f7wzbhd5bmt").hashlink, 'url':'https://getbanano.cc/'},
            {'name': 'BananoPlanet.cc', 'dur': '2 Hours', 'pay': 'Varied', 'bal': check_bal("ban_3p1anetee7arfx9zbmspwf9c8c5r88wy6zkgwcbt7rndtcqsoj6fzuy11na3"), 'lasttx': last_tx("ban_3p1anetee7arfx9zbmspwf9c8c5r88wy6zkgwcbt7rndtcqsoj6fzuy11na3").timesincetx, 'lasttx_hash': last_tx("ban_3p1anetee7arfx9zbmspwf9c8c5r88wy6zkgwcbt7rndtcqsoj6fzuy11na3").hashlink, 'url':'https://bananoplanet.cc/faucet'},
            {'name': 'BanBucket Ninja', 'dur': '15 Hours', 'pay': '0.001-0.05 BAN', 'bal': check_bal("ban_1j3rqseffoin7x5z5y1ehaqe1n7todza41kdf4oyga8phps3ea31u39ruchu"), 'lasttx': last_tx("ban_1j3rqseffoin7x5z5y1ehaqe1n7todza41kdf4oyga8phps3ea31u39ruchu").timesincetx, 'lasttx_hash': last_tx("ban_1j3rqseffoin7x5z5y1ehaqe1n7todza41kdf4oyga8phps3ea31u39ruchu").hashlink, 'url':'https://www.banbucket.ninja/'},
            {'name': 'BananoTime', 'dur': 'N/A', 'pay': '0.01-0.1 BAN', 'bal': check_bal("ban_39665maxw96iifne3izma1icdmomxy3o5z35hqzh9s13xw7si4opp5xxyg8g"), 'lasttx': last_tx("ban_39665maxw96iifne3izma1icdmomxy3o5z35hqzh9s13xw7si4opp5xxyg8g").timesincetx, 'lasttx_hash': last_tx("ban_39665maxw96iifne3izma1icdmomxy3o5z35hqzh9s13xw7si4opp5xxyg8g").hashlink, 'url':'https://faucet.bananotime.com/'},
            {'name': 'GorillaNation', 'dur': '1 Day', 'pay': '0.01 BAN', 'bal': check_bal("ban_1gori11a7fz3tee6aydqxcehttzbuk93pjsctanfkgqmesa3dmo1cyw89xex"), 'lasttx': last_tx("ban_1gori11a7fz3tee6aydqxcehttzbuk93pjsctanfkgqmesa3dmo1cyw89xex").timesincetx, 'lasttx_hash': last_tx("ban_1gori11a7fz3tee6aydqxcehttzbuk93pjsctanfkgqmesa3dmo1cyw89xex").hashlink, 'url':'https://gorillanation.ga/'},
            {'name': 'GoBanano', 'dur': '1 Day', 'pay': 'N/A', 'bal': check_bal("ban_3w91yp9ufjhpzt98xzddfmnoo8bm51ic3fp3mmx4mqbocqqde7dii1w8g4b6"), 'lasttx': last_tx("ban_3w91yp9ufjhpzt98xzddfmnoo8bm51ic3fp3mmx4mqbocqqde7dii1w8g4b6").timesincetx, 'lasttx_hash': last_tx("ban_1gori11a7fz3tee6aydqxcehttzbuk93pjsctanfkgqmesa3dmo1cyw89xex").hashlink, 'url':'https://gobanano.com/home'},
            {'name': 'BananoFaucet.club', 'dur': '1 Day', 'pay': '0.1 BAN', 'bal': check_bal("ban_3rzg5w93ipik4aie3uzafetsfa6dnqdrrsmw9c9dussge7eb5s45xmh4o4pa"), 'lasttx': last_tx("ban_3rzg5w93ipik4aie3uzafetsfa6dnqdrrsmw9c9dussge7eb5s45xmh4o4pa").timesincetx, 'lasttx_hash': last_tx("ban_3rzg5w93ipik4aie3uzafetsfa6dnqdrrsmw9c9dussge7eb5s45xmh4o4pa").hashlink, 'url':'https://www.bananofaucet.club/'},
            {'name': 'CSquared', 'dur': '1 Day', 'pay': '0.05 BAN', 'bal': check_bal("ban_3jyqzypmcn94dmyp7eb3k85sug1568xwehzx738o5jniaxaf1jpxdakjz96r"), 'lasttx': last_tx("ban_3jyqzypmcn94dmyp7eb3k85sug1568xwehzx738o5jniaxaf1jpxdakjz96r").timesincetx, 'lasttx_hash': last_tx("ban_3jyqzypmcn94dmyp7eb3k85sug1568xwehzx738o5jniaxaf1jpxdakjz96r").hashlink, 'url':'https://getban.csquared.nz/'},
            {'name': 'Bonobo', 'dur': '1 Week', 'pay': '0.07 BAN', 'bal': check_bal("ban_3faubo4bfzexkbodi67c74ut1a6it64chofgobbag87yfmy1x457jbsdccd4"), 'lasttx': last_tx("ban_3faubo4bfzexkbodi67c74ut1a6it64chofgobbag87yfmy1x457jbsdccd4").timesincetx, 'lasttx_hash': last_tx("ban_3faubo4bfzexkbodi67c74ut1a6it64chofgobbag87yfmy1x457jbsdccd4").hashlink, 'url':'https://bonobo.cc/faucet'},
            {'name': 'Banboto\'s Future Faucet', 'dur': '1 Day', 'pay': '0.19 BAN', 'bal': check_bal("ban_3jzi3modbcrfq7gds5nmudstw3kghndqb1k48twhqxds3ytyj4k7cf79q5ij"), 'lasttx': last_tx("ban_3jzi3modbcrfq7gds5nmudstw3kghndqb1k48twhqxds3ytyj4k7cf79q5ij").timesincetx, 'lasttx_hash': last_tx("ban_3jzi3modbcrfq7gds5nmudstw3kghndqb1k48twhqxds3ytyj4k7cf79q5ij").hashlink, 'url':'https://faucet.banoboto.repl.co/'},
            {'name': 'Baucarp Faucet', 'dur': '1 Day', 'pay': '0.05 BAN', 'bal': check_bal("ban_3x8hzeb8spb6e36y7yjgo6esmeahgphq1mhp545ofouuu5enrne5nzwkdasb"), 'lasttx': last_tx("ban_3x8hzeb8spb6e36y7yjgo6esmeahgphq1mhp545ofouuu5enrne5nzwkdasb").timesincetx, 'lasttx_hash': last_tx("ban_3x8hzeb8spb6e36y7yjgo6esmeahgphq1mhp545ofouuu5enrne5nzwkdasb").hashlink, 'url':'https://baucarp.herokuapp.com/'},
            {'name': 'OnlyBans Faucet', 'dur': '1 Day', 'pay': 'Varied', 'bal': check_bal("ban_1on1ybanskzzsqize1477wximtkdzrftmxqtajtwh4p4tg1w6awn1hq677cp"), 'lasttx': last_tx("ban_1on1ybanskzzsqize1477wximtkdzrftmxqtajtwh4p4tg1w6awn1hq677cp").timesincetx, 'lasttx_hash': last_tx("ban_1on1ybanskzzsqize1477wximtkdzrftmxqtajtwh4p4tg1w6awn1hq677cp").hashlink, 'url':'https://www.only-bans.cc/'},
            {'name': 'Earns.cc Faucet', 'dur': '1 Day', 'pay': 'N/A', 'bal': "N/A", 'lasttx': "N/A", 'lasttx_hash': "N/A", 'url':'https://ban.earns.cc/'},
            {'name': 'MonkeyTalks Faucet', 'dur': '1 Day', 'pay': 'Varied', 'bal': check_bal("ban_1monkeyt1x77a1rp9bwtthajb8odapbmnzpyt8357ac8a1bcron34i3r9y66"), 'lasttx': last_tx("ban_1monkeyt1x77a1rp9bwtthajb8odapbmnzpyt8357ac8a1bcron34i3r9y66").timesincetx, 'lasttx_hash': last_tx("ban_1monkeyt1x77a1rp9bwtthajb8odapbmnzpyt8357ac8a1bcron34i3r9y66").hashlink, 'url':'https://monkeytalks.cc/'},
            {'name': 'icanhaznano monke42 faucet', 'dur': '1 Day', 'pay': '0.01-0.19 BAN', 'bal': check_bal("ban_1monkecrqoqr6j6qzhtd9i8x49ujdnoqt7ramt9jmhd543icsrx5accoqtd5"), 'lasttx': last_tx("ban_1monkecrqoqr6j6qzhtd9i8x49ujdnoqt7ramt9jmhd543icsrx5accoqtd5").timesincetx, 'lasttx_hash': last_tx("ban_1monkecrqoqr6j6qzhtd9i8x49ujdnoqt7ramt9jmhd543icsrx5accoqtd5").hashlink, 'url':'https://icanhaznano.monke42.tk/'},
            {'name': 'TryBanano', 'dur': '1 Day', 'pay': '0.02 BAN', 'bal': check_bal("ban_3x4ya94gh6b8to54su8xy7nwys9n1mn5ydjn6sq4smq9fx9qi4qw1bguab7o"), 'lasttx': last_tx("ban_3x4ya94gh6b8to54su8xy7nwys9n1mn5ydjn6sq4smq9fx9qi4qw1bguab7o").timesincetx, 'lasttx_hash': last_tx("ban_3x4ya94gh6b8to54su8xy7nwys9n1mn5ydjn6sq4smq9fx9qi4qw1bguab7o").hashlink, 'url':'https://trybanano.com/'},
            {'name': 'Barrel O\' Bananos', 'dur': 'N/A', 'pay': '0.19 BAN', 'bal': check_bal("ban_1barre1777qqdcg86788tk6ojy9jmkyb8ridreezbgkhr7btnoqcntejrxhf"), 'lasttx': last_tx("ban_1barre1777qqdcg86788tk6ojy9jmkyb8ridreezbgkhr7btnoqcntejrxhf").timesincetx, 'lasttx_hash': last_tx("ban_1barre1777qqdcg86788tk6ojy9jmkyb8ridreezbgkhr7btnoqcntejrxhf").hashlink, 'url':'https://www.devinmontes.com/'},
            {'name': 'BanHub', 'dur': '1 Day', 'pay': 'N/A', 'bal': check_bal("ban_1zgdj86ohh7zbcoqkc8t7n15x9cnyfrefm6wsignd88xdozo9tsn8cg8jtsn"), 'lasttx': last_tx("ban_1zgdj86ohh7zbcoqkc8t7n15x9cnyfrefm6wsignd88xdozo9tsn8cg8jtsn").timesincetx, 'lasttx_hash': last_tx("ban_1zgdj86ohh7zbcoqkc8t7n15x9cnyfrefm6wsignd88xdozo9tsn8cg8jtsn").hashlink, 'url':'https://banhub.com/'},
            {'name': 'BananoForest', 'dur': '1 Day', 'pay': '0.42 BAN', 'bal': check_bal("ban_3sinkoff1yj9z5fougwao1gbjtsmb98u1j5p9kcrndqcc4irdxgzsjbem96e"), 'lasttx': last_tx("ban_3sinkoff1yj9z5fougwao1gbjtsmb98u1j5p9kcrndqcc4irdxgzsjbem96e").timesincetx, 'lasttx_hash': last_tx("ban_3sinkoff1yj9z5fougwao1gbjtsmb98u1j5p9kcrndqcc4irdxgzsjbem96e").hashlink, 'url':'https://faucet.bananoforest.com/'},
            {'name': 'BananoDrip', 'dur': '1 Day', 'pay': 'Varied', 'bal': check_bal("ban_3bdrip3ir5d9y3i1qi5z47pwcmd6jm39xzzzxnebrwfyoje63qa5dmnhm8f9"), 'lasttx': last_tx("ban_3bdrip3ir5d9y3i1qi5z47pwcmd6jm39xzzzxnebrwfyoje63qa5dmnhm8f9").timesincetx, 'lasttx_hash': last_tx("ban_3bdrip3ir5d9y3i1qi5z47pwcmd6jm39xzzzxnebrwfyoje63qa5dmnhm8f9").hashlink, 'url':'https://bananodrip.com/'},
            {'name': 'BananoTime', 'dur': '1 Day', 'pay': 'Varied', 'bal': check_bal("ban_39665maxw96iifne3izma1icdmomxy3o5z35hqzh9s13xw7si4opp5xxyg8g"), 'lasttx': last_tx("ban_39665maxw96iifne3izma1icdmomxy3o5z35hqzh9s13xw7si4opp5xxyg8g").timesincetx, 'lasttx_hash': last_tx("ban_39665maxw96iifne3izma1icdmomxy3o5z35hqzh9s13xw7si4opp5xxyg8g").hashlink, 'url':'https://faucet.bananotime.com/'},
            {'name': 'PerryPal', 'dur': '1 Day', 'pay': 'Varied', 'bal': check_bal("ban_3tn9xt9sxbyw9injikki3yis5fbn6m47x37gco5cw6e6x6z7z4639cdgzke6"), 'lasttx': last_tx("ban_3tn9xt9sxbyw9injikki3yis5fbn6m47x37gco5cw6e6x6z7z4639cdgzke6").timesincetx, 'lasttx_hash': last_tx("ban_3tn9xt9sxbyw9injikki3yis5fbn6m47x37gco5cw6e6x6z7z4639cdgzke6").hashlink, 'url':'https://banfaucet.perrypal21.repl.co/'},
            {'name': 'Pronouns Faucet', 'dur': '1 Day', 'pay': '0.75 BAN', 'bal': check_bal("ban_3eeq61ea33jdds5x37otx51esi8wsnxxjc8spjajyq7pj8h3nodkd19pride"), 'lasttx': last_tx("ban_3eeq61ea33jdds5x37otx51esi8wsnxxjc8spjajyq7pj8h3nodkd19pride").timesincetx, 'lasttx_hash': last_tx("ban_3eeq61ea33jdds5x37otx51esi8wsnxxjc8spjajyq7pj8h3nodkd19pride").hashlink, 'url':'https://pronouns.h.prussiafan.club/'},
            {'name': 'Crypto Jungles', 'dur': '1 Day', 'pay': '0.1 BAN', 'bal': check_bal("ban_3mkng3drofj13oo9dfpdgctayaskydr8t58j7pp6xo8564ko4y4ngboyyqxm"), 'lasttx': last_tx("ban_3mkng3drofj13oo9dfpdgctayaskydr8t58j7pp6xo8564ko4y4ngboyyqxm").timesincetx, 'lasttx_hash': last_tx("ban_3mkng3drofj13oo9dfpdgctayaskydr8t58j7pp6xo8564ko4y4ngboyyqxm").hashlink, 'url':'https://www.cryptojungles.com/'}
]
    with ThreadPoolExecutor(max_workers=200) as pool:
        returned = list(pool.map(checksite,urls))
        print(returned)
    for i in data:
        print(f"{index1} - data")
        for a in returned:
            i['status'] = a
        i['url'] = urls[index1]
        index1 = index1 + 1
    return data


