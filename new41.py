# -*- coding: utf-8 -*-
import itchatmp,json,os,re,time,datetime
from itchatmp.content import *
import pandas as pd
import numpy as np
from pandas import DataFrame
from pymongo import MongoClient
client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')


    #从数据导入piaofen
db3 = client.piaofen
collection3 = db3.piaofen   



#连接订阅号
itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wxdca1daea0b4961c4',
    appSecret = '4ff455b4b94a7f32e0f3eb04cd29c304'))


#分析订阅号文本信息
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
     huifu='对应广告：'
     global content,collection3,collection4,piaofen_df,shijian11,shijian10,shijian0,shijian01,shijian02,zixun_df,biao0
     count=0
     shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
     shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
     shijian10=shijian11-datetime.timedelta(days=1)  #明天
     shijian0=shijian11-datetime.timedelta(days=1)
     shijian01=shijian11-datetime.timedelta(days=2)
     shijian02=shijian11-datetime.timedelta(days=3)
     shijian014=shijian11-datetime.timedelta(days=13)

     shijian11=shijian11.strftime("%Y-%m-%d")  #今天
     shijian0=shijian0.strftime("%Y-%m-%d")     #昨天
     shijian01=shijian01.strftime("%Y-%m-%d")   #前天
     shijian02=shijian02.strftime("%Y-%m-%d")   #大前天

     shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
     shijian2=time.strftime('%H:%M',time.localtime(time.time()))

     co=re.compile(u'[\U00010000-\U0010ffff]')
     co=co.sub(u'',msg['Content'])
     if co=='票据分析':
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian11)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          if piaofen_df.empty:
            return('暂无当日数据，请稍后再试。')
        #做表
          huatudata3=piaofen_df[['hanglei1','hanglei2','shou','chu','shoudai','chudai']]
          huatudata5=huatudata3.groupby(['hanglei2']).sum()
          print(huatudata5.ix[1,'shou'])
          print(huatudata5.ix[1,'chu'])
          shouchubi=round(huatudata5.ix[1,'shou']/(huatudata5.ix[1,'chu']+0.0001),2)
            
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shou': '收', 'chu': '出', 'shoudai': '收代持', 'chudai': '出代持'}) 

          
          huatuhui=('当前银行收票数为%s，出票数为%s，收票/出票为%s。以下为具体广告计数（已排除重复广告）。\n\n机构  收票  出票  收代持  出代持'%(huatudata5.ix[1,'shou'],huatudata5.ix[1,'chu'],shouchubi)     )
          for i in range(0,len(huatudata4)):
                huatuhui0=('%s      %s      %s      %s      %s'%(huatudata4.ix[i,'机构'],huatudata4.ix[i,'收'],huatudata4.ix[i,'出'],huatudata4.ix[i,'收代持'],huatudata4.ix[i,'出代持']))
                huatuhui=('%s\n%s'%(huatuhui,huatuhui0))
                
          return(str( huatuhui))
     elif co=='福费廷分析':
         # shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian11)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          if piaofen_df.empty:
            return('暂无当日数据，请稍后再试。')          #做表
          huatudata3=piaofen_df[['hanglei1','hanglei2','shoufu','chufu']]
          huatudata5=huatudata3.groupby(['hanglei2']).sum()
          print(huatudata5.ix[1,'shoufu'])
          print(huatudata5.ix[1,'chufu'])
          shouchubi=round(huatudata5.ix[1,'shoufu']/(huatudata5.ix[1,'chufu']+0.0001),2)
            
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)

          huatuhui=('当前银行收福费廷数为%s，出福费廷数为%s，收福费廷/出福费廷为%s。以下为具体广告计数（已排除重复广告）。\n\n机构  收福费廷  出福费廷'%(huatudata5.ix[1,'shoufu'],huatudata5.ix[1,'chufu'],shouchubi)     )
          for i in range(0,len(huatudata4)):
                huatuhui0=('%s      %s      %s'%(huatudata4.ix[i,'hanglei1'],huatudata4.ix[i,'shoufu'],huatudata4.ix[i,'chufu']))
                huatuhui=('%s\n%s'%(huatuhui,huatuhui0))
          return(str( huatuhui))
     elif co=='存单分析':
       #   shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian11)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          if piaofen_df.empty:
            return('暂无当日市场数据，请稍后再试。')          #做表
          huatudata3=piaofen_df[['hanglei1','hanglei2','shoucun','chucun']]
          huatudata5=huatudata3.groupby(['hanglei2']).sum()
          print(huatudata5.ix[1,'shoucun'])
          print(huatudata5.ix[1,'chucun'])
          shouchubi=round(huatudata5.ix[1,'shoucun']/(huatudata5.ix[1,'chucun']+0.0001),2)
            
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)

          huatuhui=('当前银行收存单数为%s，出存单数为%s，收存单/出存单为%s。以下为具体广告计数（已排除重复广告）。\n\n机构  收存单  出存单'%(huatudata5.ix[1,'shoucun'],huatudata5.ix[1,'chucun'],shouchubi)     )
          for i in range(0,len(huatudata4)):
                huatuhui0=('%s      %s      %s'%(huatudata4.ix[i,'hanglei1'],huatudata4.ix[i,'shoucun'],huatudata4.ix[i,'chucun']))
                huatuhui=('%s\n%s'%(huatuhui,huatuhui0))
          return(str( huatuhui))
      
     elif co=='理财分析':
         # shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian11)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          if piaofen_df.empty:
            return('暂无当日数据，请稍后再试。')          #做表
          huatudata3=piaofen_df[['hanglei1','hanglei2','shouli','chuli']]
          huatudata5=huatudata3.groupby(['hanglei2']).sum()
          print(huatudata5.ix[1,'shouli'])
          print(huatudata5.ix[1,'chuli'])
          shouchubi=round(huatudata5.ix[1,'shouli']/(huatudata5.ix[1,'chuli']+0.0001),2)
            
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)

          huatuhui=('当前银行收理财数为%s，出理财数为%s，收理财/出理财为%s。以下为具体广告计数（已排除重复广告）。\n\n机构  收理财  出理财'%(huatudata5.ix[1,'shouli'],huatudata5.ix[1,'chuli'],shouchubi)     )
          for i in range(0,len(huatudata4)):
                huatuhui0=('%s      %s      %s'%(huatudata4.ix[i,'hanglei1'],huatudata4.ix[i,'shouli'],huatudata4.ix[i,'chuli']))
                huatuhui=('%s\n%s'%(huatuhui,huatuhui0))
          return(str( huatuhui))        

     elif (co=='11') or(co=='21'):
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
                   len0=min(a,6)
                   print(len0)
                   for i in range(0,len0):       
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           print(huifu0)
                           huifu=('%s\r\n***\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           count+=1
                   print(huifu)
                   return(huifu)
     elif (co=='12') or (co=='22'):
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
                   len0=min(a,6)
                   print(len0)
                   for i in range(0,len0):       
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           print(huifu0)
                           huifu=('%s\r\n***\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           count+=1
                   print(huifu)
                   return(huifu)
                  
                
                
 #以下一段分析福费廷                       
     elif (co=='13') or(co=='23'):
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
                   len0=min(a,6)
                   print(len0)
                   for i in range(0,len0):       
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           count+=1
                   print(huifu)
                   return(huifu)
     elif (co=='14') or(co=='24'):

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
                   len0=min(a,6)
                   print(len0)
                   for i in range(0,len0):       
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           count+=1
                   print(huifu)
                   return(huifu)   
                        
       
     elif (co=='15') or(co=='25'):

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
                   len0=min(a,6)
                   print(len0)
                   for i in range(0,len0):       
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           count+=1
                   print(huifu)
                   return(huifu)
     elif (co=='16') or(co=='26'):

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
                   len0=min(a,6)
                   print(len0)
                   for i in range(0,len0):       
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           count+=1
                   print(huifu)
                   return(huifu)  
                
#以下一段分析存单                        
     elif (co=='17') or(co=='27'):
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
                   len0=min(a,6)
                   print(len0)
                   for i in range(0,len0):       
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           count+=1
                   print(huifu)
                   return(huifu)
     elif (co=='18') or(co=='28'):

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
                   len0=min(a,6)
                   print(len0)
                   for i in range(0,len0):       
                           huifu0=('%s,%s,%s:%s'%(piaofen_df.ix[a-1-i,'time'],piaofen_df.ix[a-1-i,'time2'],piaofen_df.ix[a-1-i,'nickname'],piaofen_df.ix[a-1-i,'content']))
                           print(huifu0)
                           huifu=('%s\r\n***************\r\n%s')%(huifu,huifu0)
                           count+=1
                   print(huifu)
                   return(huifu)           
          
                
     else:
           return('您可发送如下指令：\n"票据分析"——获得票据数据。\n"理财分析"——获得理财数据。\n"福费廷分析"——获得福费廷数据。\n"存单分析"——获得存单数据。\n\n"11"——我要出票，我是银行。\n"12"——我要收票，我是银行。\n"13"——我要出证，我是银行。\n"14"——我要收证，我是银行。\n"15"——我要出理财，我是银行。\n"16"——我要收理财，我是银行。\n"17"——我要出存单，我是银行。\n"18"——我要收存单，我是银行。\n\n"21"——我要出票，我不是银行。\n"22"——我要收票，我不是银行。\n"23"——我要出证，我不是银行。\n"24"——我要收证，我不是银行。\n"25"——我要出理财，我不是银行。\n"26"——我要收理财，我不是银行。\n"27"——我要出存单，我不是银行。\n"28"——我要收存单，我不是银行。')   
itchatmp.run()

