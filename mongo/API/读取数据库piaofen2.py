# -*- coding: cp936 -*-
import datetime
import json,csv
import pandas as pd

from pymongo import MongoClient
#client = MongoClient()
client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')
db = client.piaofen2           #得到数据库
collection = db.piaofen2      #得到数据集合

cursor = collection.find()
df2 = pd.DataFrame(list(cursor))
print(df2)

df2.to_csv('11.csv',encoding='GB18030',mode='w',header=True)
