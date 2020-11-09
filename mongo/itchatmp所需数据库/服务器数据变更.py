# -*- coding: cp936 -*-
import datetime
import json,csv
import pandas as pd
from pymongo import MongoClient

client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')
client2=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')


print('shan')
db = client.shan           #得到数据库
collection = db.shan      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.shan     
collection2 = db.shan      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('nickname')
db = client.nickname           #得到数据库
collection = db.nickname      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.nickname     
collection2 = db.nickname      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('cun')
db = client.cun           #得到数据库
collection = db.cun      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.cun     
collection2 = db.cun      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('fu')
db = client.fu           #得到数据库
collection = db.fu      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.fu     
collection2 = db.fu      #得到数据集合
#collection2.remove()
collection2.insert(records)

print('li')
db = client.li           #得到数据库
collection = db.li      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.li     
collection2 = db.li      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('piaofen')
db = client.piaofen           #得到数据库
collection = db.piaofen      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.piaofen     
collection2 = db.piaofen      #得到数据集合
#collection2.remove()
collection2.insert(records)



print('jishi')
db = client.jishi           #得到数据库
collection = db.jishi      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.jishi     
collection2 = db.jishi      #得到数据集合
#collection2.remove()
collection2.insert(records)

print('huiguang')
db = client.huiguang           #得到数据库
collection = db.huiguang      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.huiguang     
collection2 = db.huiguang      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('huiguangzhu')
db = client.huiguangzhu           #得到数据库
collection = db.huiguangzhu      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.huiguangzhu     
collection2 = db.huiguangzhu      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('tongxun')
db = client.tongxun           #得到数据库
collection = db.tongxun      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.tongxun     
collection2 = db.tongxun      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('piaofenxi')
db = client.piaofenxi           #得到数据库
collection = db.piaofenxi      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.piaofenxi     
collection2 = db.piaofenxi      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('zixun')
db = client.zixun           #得到数据库
collection = db.zixun      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.zixun     
collection2 = db.zixun      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('tongxun')
db = client.tongxun           #得到数据库
collection = db.tongxun      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.tongxun     
collection2 = db.tongxun      #得到数据集合
#collection2.remove()
collection2.insert(records)



print('cundan')
db = client.cundan           #得到数据库
collection = db.cundan      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.cundan     
collection2 = db.cundan      #得到数据集合
#collection2.remove()
collection2.insert(records)



print('xianxia')
db = client.xianxia           #得到数据库
collection = db.xianxia      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.xianxia     
collection2 = db.xianxia      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('number')
db = client.number           #得到数据库
collection = db.number      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.number     
collection2 = db.number      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('piaojiaosuo2')
db = client.piaojiaosuo2           #得到数据库
collection = db.piaojiaosuo2      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.piaojiaosuo2     
collection2 = db.piaojiaosuo2      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('cundanbank')
db = client.cundanbank           #得到数据库
collection = db.cundanbank      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.cundanbank     
collection2 = db.cundanbank      #得到数据集合
#collection2.remove()
collection2.insert(records)



print('guogu')
db = client.guogu           #得到数据库
collection = db.guogu      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.guogu     
collection2 = db.guogu      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('yucebiao')
db = client.yucebiao           #得到数据库
collection = db.yucebiao      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.yucebiao     
collection2 = db.yucebiao      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('lilvquxian')
db = client.lilvquxian           #得到数据库
collection = db.lilvquxian      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.lilvquxian     
collection2 = db.lilvquxian      #得到数据集合
#collection2.remove()
collection2.insert(records)


print('lilvquxian')
db = client.lilvquxian           #得到数据库
collection = db.lilvquxian      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.lilvquxian     
collection2 = db.lilvquxian      #得到数据集合
#collection2.remove()
collection2.insert(records)



print('huiyuan')
db = client.huiyuan           #得到数据库
collection = db.huiyuan      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.huiyuan     
collection2 = db.huiyuan      #得到数据集合
#collection2.remove()
collection2.insert(records)



print('quxian')
db = client.quxian           #得到数据库
collection = db.quxian      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.quxian     
collection2 = db.quxian      #得到数据集合
#collection2.remove()
collection2.insert(records)

print('toupiao')
db = client.toupiao           #得到数据库
collection = db.toupiao      #得到数据集合
cursor = collection.find()
df = pd.DataFrame(list(cursor))
del df['_id']
records = json.loads(df.T.to_json()).values()

db = client2.toupiao     
collection2 = db.toupiao      #得到数据集合
#collection2.remove()
collection2.insert(records)
