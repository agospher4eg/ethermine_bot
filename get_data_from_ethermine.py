import http.client, datetime, json
def humanliketime(a):
    b=datetime.datetime.fromtimestamp(int(a)).strftime('%Y-%m-%d %H:%M:%S')
    return b

def get_new_info(mine):

    conn = http.client.HTTPSConnection("api.ethermine.org")

    _el_url='/miner/{miner}/currentStats'.format(miner=mine)
    conn.request("GET", _el_url)
    r1 = conn.getresponse()
    responce = r1.read()
    conn.close()

    data = json.loads(responce)
    status=data['status']
    data_d=data['data']
    reported_hashrate=round(float(data_d['reportedHashrate'])/1000000,2)
    current_hashrate=round(float(data_d['currentHashrate'])/1000000,2)
    average_hashrate = round(float(data_d['averageHashrate'])/1000000,2)
    time = humanliketime(data_d['time'])
    last_seen = humanliketime(data_d['lastSeen'])
    unpaid = round(float(data_d['unpaid'])/1000000000000000000,4)
    active_workers = data_d['activeWorkers']

    itog='''Status: <b>{}</b>
Time: {}
Last Seen: {}
Reported Hashrate: {}
Current Hashrate: {}
Average Hashrate: {}
Active Workers: {}
Unpaid: <b>{}</b>
'''.format(status,time,last_seen,reported_hashrate,current_hashrate,average_hashrate,active_workers,unpaid,)
    return(itog)

def get_pool_stats():
    conn = http.client.HTTPSConnection("api.ethermine.org")
    _el_url = '/poolStats'
    conn.request("GET", _el_url)
    r1 = conn.getresponse()
    responce = r1.read()
    conn.close()
    data = json.loads(responce)
    usd = data['data']['price']['usd']
    btc = data['data']['price']['btc']
    itog = 'USD: <b>{}</b> \nBTC: <b> {}</b> '.format(usd,btc)
    return(itog)