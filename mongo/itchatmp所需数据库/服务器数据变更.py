# -*- coding: cp936 -*-
import datetime
import json,csv
import pandas as pd
from pymongo import MongoClient

client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')
client2=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')


print('shan')
db = client.shan           #�õ����ݿ�
collection = db.shan      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.shan     
collection2 = db.shan      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('nickname')
db = client.nickname           #�õ����ݿ�
collection = db.nickname      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.nickname     
collection2 = db.nickname      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('cun')
db = client.cun           #�õ����ݿ�
collection = db.cun      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.cun     
collection2 = db.cun      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('fu')
db = client.fu           #�õ����ݿ�
collection = db.fu      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.fu     
collection2 = db.fu      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)

print('li')
db = client.li           #�õ����ݿ�
collection = db.li      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.li     
collection2 = db.li      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('piaofen')
db = client.piaofen           #�õ����ݿ�
collection = db.piaofen      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.piaofen     
collection2 = db.piaofen      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)



print('jishi')
db = client.jishi           #�õ����ݿ�
collection = db.jishi      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.jishi     
collection2 = db.jishi      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)

print('huiguang')
db = client.huiguang           #�õ����ݿ�
collection = db.huiguang      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.huiguang     
collection2 = db.huiguang      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('huiguangzhu')
db = client.huiguangzhu           #�õ����ݿ�
collection = db.huiguangzhu      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.huiguangzhu     
collection2 = db.huiguangzhu      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('tongxun')
db = client.tongxun           #�õ����ݿ�
collection = db.tongxun      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.tongxun     
collection2 = db.tongxun      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('piaofenxi')
db = client.piaofenxi           #�õ����ݿ�
collection = db.piaofenxi      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.piaofenxi     
collection2 = db.piaofenxi      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('zixun')
db = client.zixun           #�õ����ݿ�
collection = db.zixun      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.zixun     
collection2 = db.zixun      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('tongxun')
db = client.tongxun           #�õ����ݿ�
collection = db.tongxun      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.tongxun     
collection2 = db.tongxun      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)



print('cundan')
db = client.cundan           #�õ����ݿ�
collection = db.cundan      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.cundan     
collection2 = db.cundan      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)



print('xianxia')
db = client.xianxia           #�õ����ݿ�
collection = db.xianxia      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.xianxia     
collection2 = db.xianxia      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('number')
db = client.number           #�õ����ݿ�
collection = db.number      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.number     
collection2 = db.number      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('piaojiaosuo2')
db = client.piaojiaosuo2           #�õ����ݿ�
collection = db.piaojiaosuo2      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.piaojiaosuo2     
collection2 = db.piaojiaosuo2      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('cundanbank')
db = client.cundanbank           #�õ����ݿ�
collection = db.cundanbank      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.cundanbank     
collection2 = db.cundanbank      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)



print('guogu')
db = client.guogu           #�õ����ݿ�
collection = db.guogu      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.guogu     
collection2 = db.guogu      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('yucebiao')
db = client.yucebiao           #�õ����ݿ�
collection = db.yucebiao      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.yucebiao     
collection2 = db.yucebiao      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('lilvquxian')
db = client.lilvquxian           #�õ����ݿ�
collection = db.lilvquxian      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.lilvquxian     
collection2 = db.lilvquxian      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)


print('lilvquxian')
db = client.lilvquxian           #�õ����ݿ�
collection = db.lilvquxian      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.lilvquxian     
collection2 = db.lilvquxian      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)



print('huiyuan')
db = client.huiyuan           #�õ����ݿ�
collection = db.huiyuan      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.huiyuan     
collection2 = db.huiyuan      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)



print('quxian')
db = client.quxian           #�õ����ݿ�
collection = db.quxian      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.quxian     
collection2 = db.quxian      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)

print('toupiao')
db = client.toupiao           #�õ����ݿ�
collection = db.toupiao      #�õ����ݼ���
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.toupiao     
collection2 = db.toupiao      #�õ����ݼ���
#collection2.remove()
collection2.insert(records)
