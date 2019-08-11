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


myclient = pymongo.MongoClient("mongodb://192.168.1.18:27017/")
mydb = myclient["bitfinex"]
mycol = mydb["mhistory"]

mlist={}
i=0;
for r in mycol.find():
    i=i+1
    if mlist.get(r['Id'])==None:
        mlist[r['Id']]=1
    else:
        print('Exist')
        mlist[r['Id']] = mlist[r['Id']]+1

print(i)
