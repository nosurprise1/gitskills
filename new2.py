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
from pymongo import MongoClient
#client = MongoClient()
client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')
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
cursor3 = collection3.find()
piaofen_df = pd.DataFrame(list(cursor3))
print (piaofen_df)
    
    

content=[]



#连接订阅号
itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wx7860b4c7296dcbdf',
    appSecret = 'a8db85056d55d3e74d662667b9b015ea'))

#分析订阅号文本信息
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    #从数据导入piaofen
     db3 = client.piaofen
     collection3 = db3.piaofen   
     cursor3 = collection3.find()
     piaofen_df = pd.DataFrame(list(cursor3))
     #print (piaofen_df)
    
     global content
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
     #shoudaifa=0
     #chudaifa=0
     #shoufufa=0
     #chufufa=0
     #shoulifa=0
     #chulifa=0
     #shoucunfa=0
     #chucunfa=0
     #shouhuifa=0
     #chuhuifa=0
     huifu=''
     string=re.split(u'；|。|？|！|~~|，| |…',msg['Content'])   #将字符串分割，中午字符串分割需要用u
     num=len(string)     #计量列表长度
     if num<=30:      #为防止数量太大占内存          
         for i in range(0,num): 
            for j in range(1,162):
                c=piao_df.astype(str).loc[j,'ci'].strip()
                   # print(c)
                zhaop= re.search(c,string[i])
                if zhaop:
                                        
                      shou=int(piao_df.astype(str).loc[j,'shou'].strip())+shou
                      chu=int(piao_df.astype(str).loc[j,'chu'].strip())+chu
                      shoudai=int(piao_df.astype(str).loc[j,'shoudai'].strip())+shoudai
                      chudai=int(piao_df.astype(str).loc[j,'chudai'].strip())+chudai
                      shouhui=int(piao_df.astype(str).loc[j,'shouhui'].strip())+shouhui
                      chuhui=int(piao_df.astype(str).loc[j,'chuhui'].strip())+chuhui                    
                      break
         if shou!=0:
             shou=1
           #  chufa=1
         if chu!=0:
             chu=1
          #   shoufa=1
         if shoudai!=0:
             shoudai=1
          #   chudaifa=1
         if chudai!=0:
             chudai=1
          #   shoudaifa=1
         if shouhui!=0:
             shouhui=1
          #   chuhuifa=1
         if chuhui!=0:
             chuhui=1
            # shouhuifa=1
         yepiao=shou+chu+shoudai+chudai+shouhui+chuhui
        
        #分析福费廷
         for i in range(0,num): 
            for j in range(1,74):
                c=fu_df.astype(str).loc[j,'ci'].strip()
                   # print(c)
                zhao= re.search(c,string[i])
                if zhao:                 
                      shoufu=int(fu_df.astype(str).loc[j,'shoufu'].strip())+shoufu
                      chufu=int(fu_df.astype(str).loc[j,'chufu'].strip())+chufu           
                      break
         if shoufu!=0:
             shoufu=1
            # chufufa=1
         if chufu!=0:
             chufu=1
            # shoufufa=1       
         yefu=shoufu+chufu
         
        #分析存单
         for i in range(0,num): 
            for j in range(1,75):
                c=cun_df.astype(str).loc[j,'ci'].strip()
                   # print(c)
                zhao= re.search(c,string[i])
                if zhao:                 
                      shoucun=int(cun_df.astype(str).loc[j,'shoucun'].strip())+shoucun
                      chucun=int(cun_df.astype(str).loc[j,'chucun'].strip())+chucun           
                      break
         if shoucun!=0:
                 shoucun=1
                # chucunfa=1
         if chucun!=0:
                 chucun=1
                 #shoucunfa=1       
         yecun=shoucun+chucun
            
         #分析理财
         for i in range(0,num): 
            for j in range(1,39):
                c=li_df.astype(str).loc[j,'ci'].strip()
                   # print(c)
                zhao= re.search(c,string[i])
                if zhao:                 
                      shouli=int(li_df.astype(str).loc[j,'shouli'].strip())+shouli
                      chuli=int(li_df.astype(str).loc[j,'chuli'].strip())+chuli           
                      break
         if shouli!=0:
                 shouli=1
                 #chulifa=1
         if chuli!=0:
                 chuli=1
                # shoulifa=1       
         yeli=shouli+chuli                               
               
            
            
         if (yepiao+yefu+yeli+yecun)!=0:
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
                           hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                           hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                           break
                      else:
                            if num-2>=0:
                                if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[num-2]:
                                     hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                     hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                                     hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                                     break
                                else:
                                     if num-3>=0:
                                          if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[num-3]:
                                               hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                               hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                                               hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                                               break
                                          else:
                                                 if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[0]:
                                                         hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                                         hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                                                         hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                                                         break
           #name=msg['nickname']    #ActualNickName换成nickname
           shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
           shijian2=time.strftime('%H:%M',time.localtime(time.time()))
           if hanglei2!=0:
               data=pd.DataFrame({'time':[shijian1],
                              'time2':[shijian2],
                              'hanglei2':[hanglei2],
                              'hanglei3':[hanglei3],
                              'hanglei1':[hanglei1],
                              'nickname':['none'],
                              'shou':[shou],
                              'chu':[chu],
                              'shoudai':[shoudai],
                              'chudai':[chudai],
                              'shouhui':[shouhui],
                              'chuhui':[chuhui],
                              'shoufu':[shoufu],
                              'chufu':[chufu],
                              'shouli':[shouli],
                              'chuli':[chuli],
                              'shoucun':[shoucun],
                              'chucun':[chucun],
                              'content':[msg['Content']],
                              'leixing':['1']
                              })
               print(data)      
               records = json.loads(data.T.to_json()).values()
               collection3.insert(records)
       
  

         
               a=len(piaofen_df)
               print(a)
               print(type(piaofen_df.ix[a-1-1,'shou']))
               print(type(piaofen_df.ix[a-50,'shou']))
               print(type(piaofen_df.ix[a-1-1,'hanglei2']))
               print(type(piaofen_df.ix[a-50,'hanglei2']))
               print(piaofen_df.ix[a-1,'shou']),
               print(piaofen_df.ix[a-1,'hanglei2']),
               print(piaofen_df.ix[a-1,'content'])
               print(piaofen_df.ix[a-1,'time2'])
               print('----------------------')
            
               print(piaofen_df.ix[a-1-1,'shou']),
               print(piaofen_df.ix[a-1-1,'hanglei2']),
               print(piaofen_df.ix[a-1-1,'content'])
               print(piaofen_df.ix[a-2,'time2'])
                
               if shou==0 and chu==1 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==0:
                    for i in range(0,a-1):
                       if (int(piaofen_df.ix[a-1-i,'shou'])==1) and (int(piaofen_df.ix[a-1-i,'hanglei2'])==1 ) and (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           #print(i)
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                          
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1 
                           
                           if (count==8) or(i>=100):
                               print(i)
                               print(huifu)
                                #return(huifu)
                               break
                               
                            
             


itchatmp.run()

