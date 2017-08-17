# -*- coding: utf-8 -*-
import itchatmp,json
import os
import re
import time
import csv
from itchatmp.content import *
import pandas as pd
import numpy as np
from pandas import DataFrame
# 在注册时增加isGroupChat=True将判定为群聊回复
#总共有单独回复、群聊分析、群发广告、csv群发四块功能。
from pymongo import MongoClient
#zhongjie=[u'浙江邮储杨炳']  #个人发送

client = MongoClient()
client = MongoClient('139.196.79.93', 27017)


db = client.piao
collection = db.piao  #http://www.jb51.net/article/77537.htm
cursor = collection.find()
piao_df= pd.DataFrame(list(cursor))
piao_df=piao_df[['xuhao','ci','shou','chu','shoudai','chudai','shouhui','chuhui']]
piao_df=piao_df.set_index('xuhao')
piao_df=piao_df.sort_index(ascending=True)
print (piao_df)

db2 = client.bank
collection2 = db2.bank   #·½·¨2
cursor2 = collection2.find()
bank_df = pd.DataFrame(list(cursor2))
bank_df=bank_df[['xuhao','yinhang','fenlei1','fenlei2','fenlei3']]
bank_df=bank_df.set_index('xuhao')
bank_df=bank_df.sort_index(ascending=True)
print (bank_df)

db3 = client.piaofen
collection3 = db3.piaofen   #·½·¨2
cursor3 = collection3.find()
piaofen_df = pd.DataFrame(list(cursor3))
print (piaofen_df)
content=[]




itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wxdca1daea0b4961c4',
    appSecret = '4ff455b4b94a7f32e0f3eb04cd29c304'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
     global content
     #return(msg['Content'])
     guang=[]
     count=0
     #friend=itchatmp.search_friends(userName=msg['FromUserName'])
     shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
     shijian2=time.strftime('%H:%M',time.localtime(time.time()))
     hanglei2=0
     hanglei3=0
     hanglei1=0
     shou=0
     chu=0
     shoudai=0
     chudai=0
     shouhui=0
     chuhui=0
     shoufu=0
     chufu=0
     shouli=0
     chuli=0
     shoucun=0
     chucun=0
     yepiao=0
     yefu=0 
     yeli=0
     yecun=0
     shoufa=0
     chufa=0
     shoudaifa=0
     chudaifa=0
     shoufufa=0
     chufufa=0
     shoulifa=0
     chulifa=0
     shoucunfa=0
     chucunfa=0
     shouhuifa=0
     chuhuifa=0
  
     #以下一段是给中介画
     string=re.split(u'；|。|？|！|~~|，| |…',msg['Content'])   #将字符串分割，中午字符串分割需要用u
     num=len(string)     #计量列表长度
     if num<=30:      #为防止数量太大占内存          
         for i in range(0,num): 
            for j in range(1,162):
                c=piao_df.astype(str).loc[j,'ci'].strip()
                   # print(c)
                zhaop= re.search(c,string[i])
                if zhaop:
                      #print(int(piao_df.astype(str).loc[j,'shou'])+shou)                     
                      shou=int(piao_df.astype(str).loc[j,'shou'].strip())+shou
                      chu=int(piao_df.astype(str).loc[j,'chu'].strip())+chu
                      shoudai=int(piao_df.astype(str).loc[j,'shoudai'].strip())+shoudai
                      chudai=int(piao_df.astype(str).loc[j,'chudai'].strip())+chudai
                      shouhui=int(piao_df.astype(str).loc[j,'shouhui'].strip())+shouhui
                      chuhui=int(piao_df.astype(str).loc[j,'chuhui'].strip())+chuhui                    
                      print('11111')
                      break
         if shou!=0:
             shou=1
             chufa=1
         if chu!=0:
             chu=1
             shoufa=1
         if shoudai!=0:
             shoudai=1
             chudaifa=1
         if chudai!=0:
             chudai=1
             shoudaifa=1
         if shouhui!=0:
             shouhui=1
             chuhuifa=1
         if chuhui!=0:
             chuhui=1
             shouhuifa=1
         yepiao=shou+chu+shoudai+chudai+shouhui+chuhui
         if yepiao!=0:
           content.append(msg['Content'])             
           for j2 in range(1,326):
                #if bank_df.astype(str).loc[j2,'yinhang'].strip() in (msg['NickName']): 
                 #      hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                  #     hanglei2=bank_df.astype(str).loc[j2,'fenlei2'].strip()
                   #    hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                    #   break
               # else:
                      if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[num-1]:
                           hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                           hanglei2=bank_df.astype(str).loc[j2,'fenlei2'].strip()
                           hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                           break
                      else:
                            if num-2>=0:
                                if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[num-2]:
                                     hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                     hanglei2=bank_df.astype(str).loc[j2,'fenlei2'].strip()
                                     hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                                     break
                                else:
                                     if num-3>=0:
                                          if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[num-3]:
                                               hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                               hanglei2=bank_df.astype(str).loc[j2,'fenlei2'].strip()
                                               hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                                               break
                                          else:
                                                 if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[0]:
                                                         hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                                         hanglei2=bank_df.astype(str).loc[j2,'fenlei2'].strip()
                                                         hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                                                         break
           #name=msg['nickname']    #ActualNickName换成nickname
           shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
           shijian2=time.strftime('%H:%M',time.localtime(time.time()))
           
           data=pd.DataFrame({'time':[shijian1],
                              'time2':[shijian2],
                              'hanglei2':[hanglei2],
                              'hanglei3':[hanglei3],
                              'hanglei1':[hanglei1],
                             # 'nickname':[name],
                              'shou':[shou],
                              'chu':[chu],
                              'shoudai':[shoudai],
                              'chudai':[chudai],
                              'shouhui':[shouhui],
                              'chuhui':[chuhui],
                              'content':[msg['Content']],
                              'leixing':['1']
                              })
    #hanglei3,hanglei1,name,shou,chu,shoudai,chudai,shouhui,chuhui,shoufu,chufu,shouli,chuli,shoucun,chucun,msg['Content'],'2']
           
           #writer = csv.writer(csvfile)
           #writer.writerow(data)
           #csvfile.close()
           print(data)      
           #print collection
           records = json.loads(data.T.to_json()).values()
           collection3.insert(records)
       
  


     #print（msg['nickname']）
     print（msg['ActualNickName']）
     a=len(piaofen_df)
     print(a)
     if shoufa==1 and chufa==0 and shoudaifa==0 and chudaifa==0 and shoufufa==0 and chufufa==0 and shoulifa==0 and chulifa==0 and shoucunfa==0 and chucunfa==0:
          for i in range(0,a-1):
              if piaofen_df.ix[a-1-i,'shou']==1 and (piaofen_df.ix[a-1-i,'hanglei2']==1 ) and (count<8) and (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                  return('%s,%s:%s'%(piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                  #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                  guang.append(piaofen_df.ix[a-1-i,'content'])      
                  count+=1
     elif shoufa==0 and chufa==1 and shoudaifa==0 and chudaifa==0 and shoufufa==0 and chufufa==0 and shoulifa==0 and chulifa==0 and shoucunfa==0 and chucunfa==0:
          for i in range(0,a-1):
              if piaofen_df.ix[a-1-i,'chu']==1 and (piaofen_df.ix[a-1-i,'hanglei2']==1 ) and (count<8) and (piaofen_df.ix[a-1-i,'content'] not in guang):
                  return('%s,%s:%s'%(piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                  #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                  guang.append(piaofen_df.ix[a-1-i,'content'])      
                  count+=1
     elif shoufa==0 and chufa==0 and shoudaifa==1 and chudaifa==0 and shoufufa==0 and chufufa==0 and shoulifa==0 and chulifa==0 and shoucunfa==0 and chucunfa==0:
          for i in range(0,a-1):
              if piaofen_df.ix[a-1-i,'shoudai']==1 and (piaofen_df.ix[a-1-i,'hanglei2']==1 ) and (count<8) and (piaofen_df.ix[a-1-i,'content'] not in guang):
                  return('%s,%s:%s'%(piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                    #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                  guang.append(piaofen_df.ix[a-1-i,'content'])      
                  count+=1
     elif shoufa==0 and chufa==0 and shoudaifa==0 and chudaifa==1 and shoufufa==0 and chufufa==0 and shoulifa==0 and chulifa==0 and shoucunfa==0 and chucunfa==0:
          for i in range(0,a-1):
              if piaofen_df.ix[a-1-i,'chudai']==1 and (piaofen_df.ix[a-1-i,'hanglei2']==1 ) and (count<8) and (piaofen_df.ix[a-1-i,'content'] not in guang):
                  return('%s,%s:%s'%(piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                    #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                  guang.append(piaofen_df.ix[a-1-i,'content'])      
                  count+=1

  # and(friend['NickName'] !=data.ix[a-1-i,'nickname'] )
     #else:
          #itchat.send(u'不能识别您的广告，或者您发送了多方向广告。发送业务广告精准对接，发送“s”了解收票情况，发送“m”了解卖票情况',msg['FromUserName'])
          #itchat.send('@img@%s' % 'guanggao.png',msg['FromUserName'])






itchatmp.run()

