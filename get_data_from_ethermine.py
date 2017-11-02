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
    print(data)
    status=data['status']
    data = data['data']
    if status=='OK' and data!='NO DATA':

        reported_hashrate=round(float(data['reportedHashrate'])/1000000,2)
        current_hashrate=round(float(data['currentHashrate'])/1000000,2)
        average_hashrate = round(float(data['averageHashrate'])/1000000,2)
        time = humanliketime(data['time'])
        last_seen = humanliketime(data['lastSeen'])
        unpaid = round(float(data['unpaid'])/1000000000000000000,4)
        active_workers = data['activeWorkers']

        itog='''Status: <b>{}</b>
Time: {}
Last Seen: {}
Reported Hashrate: {}
Current Hashrate: {}
Average Hashrate: {}
Active Workers: {}
Unpaid: <b>{}</b>
'''.format(status,time,last_seen,reported_hashrate,current_hashrate,average_hashrate,active_workers,unpaid,)
    else:
        itog='NO DATA'
        unpaid='NO DATA'
    return(itog,str(unpaid),status)

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
    itog = 'USD: <b>{}</b> \nBTC: <b> {}</b> \n'.format(usd,btc)
    return(itog,str(usd))

def ethermine_paid(mine):
    conn = http.client.HTTPSConnection("api.ethermine.org")
    _el_url='/miner/{miner}/payouts'.format(miner=mine)
    conn.request("GET", _el_url)
    r1 = conn.getresponse()
    responce = r1.read()
    conn.close()
    data = json.loads(responce)
    data_d = data['data']
    paid=0
    for n in range (0,len(data_d)):
        paid+=data_d[n]['amount']
    paid=round(float(paid) / 1000000000000000000, 4)
    return(paid)


#print(get_new_info('B5304d577494e21Be4fdb13e603248a4A4c61c28'))