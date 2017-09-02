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
     global content,collection3,piaofen_df,shijian11,shijian0,shijian01,shijian02
#只看某几个银行

     if '只看工行' in msg['Content']: 
         kanhang='工行'
         cursor4=collection3.find
        
     guang=[]
     count=0
     shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
     shijian2=time.strftime('%H:%M',time.localtime(time.time()))
     hanglei2=0
     hanglei3=0
     hanglei1='中介'
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
     huifu='对应广告：'
     string=re.split(u'；|。|？|！|~~|，| |…',msg['Content'])   #将字符串分割，中午字符串分割需要用u
     num=len(string)     #计量列表长度
     if num<=30:      #为防止数量太大占内存          
         for i in range(0,num): 
            for j in range(1,163):
                c=piao_df.astype(str).loc[j,'ci'].strip()
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
         if chu!=0:
             chu=1
         if shoudai!=0:
             shoudai=1
         if chudai!=0:
             chudai=1
         if shouhui!=0:
             shouhui=1
         if chuhui!=0:
             chuhui=1
         yepiao=shou+chu+shoudai+chudai+shouhui+chuhui
           
        #分析福费廷
         for i in range(0,num): 
            for j in range(1,74):
                c=fu_df.astype(str).loc[j,'ci'].strip()
                zhao= re.search(c,string[i])
                if zhao:                 
                      shoufu=int(fu_df.astype(str).loc[j,'shoufu'].strip())+shoufu
                      chufu=int(fu_df.astype(str).loc[j,'chufu'].strip())+chufu           
                      break
         if shoufu!=0:
             shoufu=1
         if chufu!=0:
             chufu=1
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
         if chucun!=0:
                 chucun=1    
         yecun=shoucun+chucun
            
         #分析理财
         for i in range(0,num): 
            for j in range(1,39):
                c=li_df.astype(str).loc[j,'ci'].strip()
                zhao= re.search(c,string[i])
                if zhao:                 
                      shouli=int(li_df.astype(str).loc[j,'shouli'].strip())+shouli
                      chuli=int(li_df.astype(str).loc[j,'chuli'].strip())+chuli           
                      break
         if shouli!=0:
                 shouli=1
         if chuli!=0:
                 chuli=1    
         yeli=shouli+chuli                               
               
            
         ####   
         if (yepiao+yefu+yeli+yecun)!=0: 
           print(num)
           for j2 in range(1,326):
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
           shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
           shijian2=time.strftime('%H:%M',time.localtime(time.time()))
           print(content)
           if hanglei2!=0 and (msg['Content'] not in content):
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
                  
                  records = json.loads(data.T.to_json()).values()
                  collection3.insert(records)
                  content.append(msg['Content'])  
                  print(data)
                
                
                
#回复广告                
           if hanglei2!=0:
               
               if shou==0 and chu==1 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shou':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return('111')
                               print('已发送')
                               break
               elif shou==1 and chu==0 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chu':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
               elif shou==0 and chu==0 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==0 and shouhui==1 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chuhui':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
               elif shou==0 and chu==0 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==1:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shouhui':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
               elif shou==0 and chu==0 and shoudai==1 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chudai':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
               elif shou==0 and chu==0 and shoudai==0 and chudai==1 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shoudai':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
                        
      #福费廷
               elif shou==0 and chu==0 and shoudai==0 and chudai==0 and shoufu==0 and chufu==1 and shouli==0 and chuli==0 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shoufu':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
               elif shou==0 and chu==0 and shoudai==0 and chudai==0 and shoufu==1 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chufu':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6) or (i>=1):
                               print(i)
                               return huifu
                               
                               break

                        
                        
               elif shou==0 and chu==0 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==1 and chuli==0 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chuli':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
               elif shou==0 and chu==0 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==1 and shoucun==0 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shouli':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break

                        
               elif shou==0 and chu==0 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==1 and chucun==0 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chucun':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
               elif shou==0 and chu==0 and shoudai==0 and chudai==0 and shoufu==0 and chufu==0 and shouli==0 and chuli==0 and shoucun==0 and chucun==1 and shouhui==0 and chuhui==0:
                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                   shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                   shijian0=shijian11-datetime.timedelta(days=1)
                   shijian01=shijian11-datetime.timedelta(days=2)
                   shijian02=shijian11-datetime.timedelta(days=3)
                   shijian11=shijian11.strftime("%Y-%m-%d")  
                   shijian0=shijian0.strftime("%Y-%m-%d")
                   shijian01=shijian01.strftime("%Y-%m-%d")  
                   shijian02=shijian02.strftime("%Y-%m-%d")  
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shoucun':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   print(piaofen_df)
                   a=len(piaofen_df)
                   for i in range(0,a):
                       if (piaofen_df.ix[a-1-i,'content'] not in guang):                  
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           #print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           guang.append(piaofen_df.ix[a-1-i,'content'])      
                           count+=1
                           if (count==6)or (i>=a):
                               return huifu
                               print('已发送')
                               break
itchatmp.run()

