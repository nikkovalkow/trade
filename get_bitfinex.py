import datetime
from urllib.request import Request, urlopen
import urllib.error
import pymongo
from urllib.parse   import quote
import time
import demjson
import time
import lxml.html as html
import json


def GetPageText(url):
    # Gets URL as text, return URL contenet as text,
    # in case of HTML error returns Error code
    # in case of non-HTML error retuens None
    ErrorCount = 0
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    for i in range(0, 3):

        try:
            response = urlopen(req)
        except urllib.error.HTTPError as e:
            ExceptionMessage("HTTP ERROR: " + str(e.code) + " " + url)
            time.sleep(5)
            ErrorCount = ErrorCount + 1
            pass
        except:
            ExceptionMessage("HTTP ERROR: NO TYPE")
            time.sleep(5)
            ErrorCount = ErrorCount + 1
            pass
    if ErrorCount == 3:
        return None
    else:
        response.encoding = 'UTF-8'
        data = response.read()
        encoding = response.headers.get_content_charset('utf-8')

        return data.decode(encoding, errors='ignore')



def GetBittrexHistory():

    d = json.loads(GetPageText('https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=USDT-BTC'))

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["bitfinex"]
    mycol = mydb["mhistory"]

    for i in d['result']:
        if mycol.count_documents({'Id': i['Id']}) == 0:
            mycol.insert_one(i)
        else:
            print("Exists",i['Id'])


def GetBittrexHistory():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["bitfinex"]
    mycol = mydb["orderbook"]


    t=datetime.datetime.utcnow()
    d = json.loads(GetPageText('https://api.bittrex.com/api/v1.1/public/getorderbook?market=USDT-BTC&type=both'))
    d=d['result']
    d['time']=t
    mycol.insert_one(d)


GetBittrexHistory()
GetBittrexHistory()
print('ok -',datetime.datetime.utcnow())








