import http.client, xml.etree.ElementTree as ET, json, datetime
from additional_data import weather_token
#cbr.ru
def get_curs(el_date):
    content_type={'Content-Type': 'text/xml', 'charset': 'UTF-8'}
    url='/DailyInfoWebServ/DailyInfo.asmx'		   # 5.1. Введите url SOAP сервиса
    soap_server='cbr.ru'		                       # 5.2. Введите IP Адрес SOAP сервиса
    soap_port='80'		                               # 5.3. Введите Порт SOAP сервиса
    method='POST'
    soap='{soap_server}:{soap_port}'.format(soap_server=soap_server,soap_port=soap_port)
    connection=http.client.HTTPConnection(soap)
    soap_envelope='<?xml version="1.0" encoding="utf-8"?>\n<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">\n  <soap12:Body>\n    <GetCursOnDate xmlns="http://web.cbr.ru/">     \n <On_date>{}</On_date>  \n  </GetCursOnDate> \n </soap12:Body></soap12:Envelope>'.format(el_date)

    connection.request(method, url, soap_envelope, content_type)
    soapResponse = connection.getresponse()
    resp = soapResponse.read()
    connection.close()
    #resp=resp[2:len(resp)-1]
    root = ET.fromstring(resp)

    body=root.find('{http://www.w3.org/2003/05/soap-envelope}Body')
    response=body.find('{http://web.cbr.ru/}GetCursOnDateResponse')
    result=response.find('{http://web.cbr.ru/}GetCursOnDateResult')
    diffragm=result.find('{urn:schemas-microsoft-com:xml-diffgram-v1}diffgram')
    value_data=diffragm.find('ValuteData')
    valc=value_data.findall('ValuteCursOnDate')
    for n in valc:
            roworder = n.get('{urn:schemas-microsoft-com:xml-msdata}rowOrder')
            vname   = n.find('Vname').text.strip()
            #vnom    = n.find('Vnom').text
            vcurs    = n.find('Vcurs').text
            vcode    = n.find('Vcode').text
            vchcode  = n.find('VchCode').text
            if vchcode=='USD':
                usd_price = vcurs
            if vchcode=='EUR':
                eur_price = vcurs
            #print(el_date,vcode,vchcode,vcurs,roworder,vname)
    itog='Date: {}\nUSD <b>{}</b>\nEUR <b>{}</b>'.format(el_date,usd_price,eur_price)
    return(itog)

el_city=524901

#openweathermap.org

def humanliketime(a):
    b=datetime.datetime.fromtimestamp(int(a)).strftime('%Y-%m-%d %H:%M:%S')
    return b

def humanliketemp(a):
    if int(a)>0:
        b='+'+str(a)
    return b

def humanlike_wind(el_deg):
    if el_deg==360:
        el_deg=359
    el_deg=el_deg*10
    a=list(range(0,3601,225))
    compas='N;NE;NE;E;E;SE;SE;S;S;SW;SW;W;W;NW;NW;N'.split(';')
    for n in range(len(a)-1):
        if n+2 > len(a):
            b=n
        else:
            b=n+1
        if el_deg>= a[n] and el_deg<a[b]:
            return(compas[n])

def get_weather_by_city_id(city_id):
    conn = http.client.HTTPSConnection('api.openweathermap.org')
    _el_url = '/data/2.5/weather?id={city}&APPID={weather}&units=metric'.format(city=city_id,weather=weather_token)
    conn.request("GET", _el_url)
    r1 = conn.getresponse()
    data1 = r1.read()
    conn.close()

    data=json.loads(data1)

    coord=data['coord']
    weather=data['weather'][0]
    clou1=weather.get('main')
    clou2=weather.get('description')
    base=data['base']
    main=data['main']
    temp=humanliketemp(main.get('temp'))
    temp_min=humanliketemp(main.get('temp_min'))
    temp_max=humanliketemp(main.get('temp_max'))
    pressure=main.get('pressure')
    humidity=main.get('humidity')
    visib=data['visibility']
    wind=data['wind']
    wind_speed=wind.get('speed')
    wind_deg=humanlike_wind(wind.get('deg'))
    clouds=data['clouds'].get('all')
    sys=data['sys']
    sunrise=humanliketime(sys.get('sunrise'))[11:20]
    sunset=humanliketime(sys.get('sunset'))[11:20]
    city_name=data['name']
    dt=humanliketime(data['dt'])

    itog=('''
City: {}
Min Temp: {} 
Max Temp: {} 
Current Temp: <b>{}</b>
Pressure: {}
Humidity: {} %
Cloudiness: {} %
Visibility: {}
Wind Speed: {} meter/sec
Wind Deg: {}
Sunrise: {}
Sunset: {}
Weather Condition: {} - {}
Time: {}
    '''.format(city_name,temp_min, temp_max, temp,pressure,humidity,clouds, visib,wind_speed,wind_deg,sunrise,sunset,clou1,clou2,dt))

    return(itog)


#print(get_weather_by_city_id(524901))