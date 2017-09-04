# -*- coding: utf-8 -*-
import itchatmp,json,os,re,time,datetime
from itchatmp.content import *
import pandas as pd
import numpy as np
from pandas import DataFrame
from pymongo import MongoClient
client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')

global content,collection3,piaofen_df,shijian11,shijian0,shijian01,shijian02
shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
shijian0=shijian11-datetime.timedelta(days=1)
shijian01=shijian11-datetime.timedelta(days=2)
shijian02=shijian11-datetime.timedelta(days=3)
shijian11=shijian11.strftime("%Y-%m-%d")  
shijian0=shijian0.strftime("%Y-%m-%d")
shijian01=shijian01.strftime("%Y-%m-%d")  
shijian02=shijian02.strftime("%Y-%m-%d")  



print(shijian11)
print(shijian0)
print(shijian01)
print(shijian02)


#从数据导入piao
db = client.piao
collection = db.piao  #http://www.jb51.net/article/77537.htm
cursor = collection.find()
piao_df= pd.DataFrame(list(cursor))
piao_df=piao_df[['xuhao','ci','shou','chu','shoudai','chudai','shouhui','chuhui']]
piao_df=piao_df.set_index('xuhao')
piao_df=piao_df.sort_index(ascending=True)

#从数据导入cun
db = client.cun
collection = db.cun  #http://www.jb51.net/article/77537.htm
cursor = collection.find()
cun_df= pd.DataFrame(list(cursor))
cun_df=cun_df[['xuhao','ci','shoucun','chucun']]
cun_df=cun_df.set_index('xuhao')
cun_df=cun_df.sort_index(ascending=True)

#从数据导入fu
db = client.fu
collection = db.fu  #http://www.jb51.net/article/77537.htm
cursor = collection.find()
fu_df= pd.DataFrame(list(cursor))
fu_df=fu_df[['xuhao','ci','shoufu','chufu']]
fu_df=fu_df.set_index('xuhao')
fu_df=fu_df.sort_index(ascending=True)

#从数据导入li
db = client.li
collection = db.li  #http://www.jb51.net/article/77537.htm
cursor = collection.find()
li_df= pd.DataFrame(list(cursor))
li_df=li_df[['xuhao','ci','shouli','chuli']]
li_df=li_df.set_index('xuhao')
li_df=li_df.sort_index(ascending=True)


#从数据导入bank
db2 = client.bank
collection2 = db2.bank   
cursor2 = collection2.find()
bank_df = pd.DataFrame(list(cursor2))
bank_df=bank_df[['xuhao','yinhang','fenlei1','fenlei2','fenlei3']]
bank_df=bank_df.set_index('xuhao')
bank_df=bank_df.sort_index(ascending=True)

    #从数据导入piaofen
db3 = client.piaofen
collection3 = db3.piaofen   
#cursor3 = collection3.find({"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]})
#cursor3 = collection3.find({"$or":[{'time':'2017-08-28'},{'time':'2017-08-29'}]})
#piaofen_df = pd.DataFrame(list(cursor3))
content=[]

#连接订阅号
itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wxdca1daea0b4961c4',
    appSecret = '4ff455b4b94a7f32e0f3eb04cd29c304'))


#分析订阅号文本信息
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
                   

     return('1111111')
                
        
        
itchatmp.run()

