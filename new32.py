# -*- coding: utf-8 -*-
import itchatmp,json,os,re,time,datetime
from itchatmp.content import *
import pandas as pd
import numpy as np
from pandas import DataFrame
from pymongo import MongoClient
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
#cursor3 = collection3.find({"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]})
#cursor3 = collection3.find({"$or":[{'time':'2017-08-28'},{'time':'2017-08-29'}]})
#piaofen_df = pd.DataFrame(list(cursor3))
content=[]

db4 = client.cundanfenxi
collection4 = db4.cundanfenxi 



#连接订阅号
itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wxdca1daea0b4961c4',
    appSecret = '4ff455b4b94a7f32e0f3eb04cd29c304'))


#分析订阅号文本信息
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
     global content,collection3,collection4,piaofen_df,shijian11,shijian10,shijian0,shijian01,shijian02,zixun_df,biao0
     guang=[]
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
     print(shijian11)
     print(shijian0)
     print(shijian01)
     print(shijian02)
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
     zixun='最新资讯（如需正文，发送获取号即可）：'
     co=re.compile(u'[\U00010000-\U0010ffff]')
     co=co.sub(u'',msg['Content'])
     string=re.split('；|：|:|。|！|~~|，| |…',co)   #将字符串分割，中午字符串分割需要用u
     while '' in string:
        string.remove('')   #删除空的元素
     num=len(string)     #计量列表长
     print(num)
     if num>8:
         return('请勿输入过多语句，请控制在8个句子以内。')#为防止数量太大占内存          
     else:
       if co=='资讯':
          db3 = client.zixun
          collection3 = db3.zixun   
          cursor3 = collection3.find({"$and":[{'爬取日期':{'$gte':str(shijian0)}},{'权重':{'$ne':'宏观'}}
                                              ]})    
          zixun_df = pd.DataFrame(list(cursor3))
          if zixun_df.empty:
            return('暂无当日数据，请稍后再试。')          #做表
          zixun_df = zixun_df.sort_values(by='时间', ascending=True)
          zixun_df =  zixun_df.reset_index(drop=True)  
          a=len(zixun_df)
          len0=min(a,18)
          print(len0)
          for i in range(0,len0):       
                           huifu0=('%s,%s\n获取号：%s'%(zixun_df.ix[a-1-i,'时间'],zixun_df.ix[a-1-i,'标题'],zixun_df.ix[a-1-i,'获取号']))
                           print(huifu0)
                           zixun=('%s\n\n%s')%(zixun,huifu0)
                           count+=1
          print(zixun)
          return(zixun)
         
       #获取单个新闻                                           
       if string[0].isdigit() is True:
          db3 = client.zixun
          collection3 = db3.zixun   
          cursor3 = collection3.find({'获取号':int(string[0])})                           
          zixun_df = pd.DataFrame(list(cursor3))
          print(zixun_df)
          neirong=str(zixun_df.ix[0,'内容'])
          chang=len(neirong)
          print(chang)
          chang=min(len(neirong),580)
          print(chang)
          neirong=str(neirong)[0:chang]
          laiyuan=zixun_df.ix[0,'序号']
          biaoti=zixun_df.ix[0,'标题']
          shijian=zixun_df.ix[0,'时间']
          huiful=('%s,《%s》,来源“%s”：\n%s……\n%s'%(shijian,biaoti,laiyuan,neirong,zixun_df.ix[0,'链接']))
          print(huiful)
          return (huiful)
            
                                              
     #资讯搜索                                           
       if string[0]=='资讯':
          sousuo=string[1]
          db3 = client.zixun
          collection3 = db3.zixun   
          cursor3 = collection3.find({"$and":[{'爬取日期':{'$gte':str(shijian014)}},{'标题':{'$regex':sousuo}}]})    
          zixun_df = pd.DataFrame(list(cursor3))
          if zixun_df.empty:
                return('未检索到相关资讯~')
          zixun_df = zixun_df.sort_values(by='爬取日期', ascending=True)
            
          zixun_df =  zixun_df.reset_index(drop=True)  
         # print(zixun_df)
            
          a=len(zixun_df)
          print(a)
          len0=min(a,16)
          print(len0)

          for i in range(0,len0): 
                           ti=zixun_df.ix[a-1-i,'标题']
                           chang1=min(len(zixun_df.ix[a-1-i,'标题']),30)
                           ti=str(ti)[0:chang1]
                           huifu0=('%s,%s\n获取号：%s'%(zixun_df.ix[a-1-i,'爬取日期'],ti,int(zixun_df.ix[a-1-i,'获取号'])))
                           print(huifu0)
                           zixun=('%s\n\n%s')%(zixun,huifu0)
                           count+=1
          zixun=('共搜索出%s条相关资讯：\n%s')%(a,zixun)
          return(zixun)                                              
                                              
            
            
            
       elif string[0]=='票据分析':
      #    shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
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
       elif string[0]=='福费廷分析':
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
       elif string[0]=='存单分析':
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
      
       elif string[0]=='理财分析':
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
    
    
#以下提供广告
#以下一段分析票据
       elif string[0]=='票据':
         for i in range(0,num): 
            for j in range(1,164):
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
            if(shou+chu+shoudai+chudai+shouhui+chuhui)>0:
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
         if (shou+chu+shoudai+chudai+shouhui+chuhui)!=0:
             for j2 in range(1,336):
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
            return('未能识别广告。\n如:\n“票据：收跨年票，**银行0571-88888888”。\n如有疑问请联系微信号：18969901812。')
      #   shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
       #  shijian2=time.strftime('%H:%M',time.localtime(time.time()))
        # print(shijian11)
        # print(shijian1) 
         db3=client.piaofen
         collection3=db3.piaofen
         cursor = collection3.find({'time':str(shijian11)})
         df2 = pd.DataFrame(list(cursor))
         contentyy=df2['content'].tolist()
         if(hanglei2==0):
               return('请在广告最后附上所在银行（中介结构暂时不行）。')
         else:
               if (co not in contentyy):
                  data=pd.DataFrame({'time':[shijian11],
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
                              'content':[co],
                              'leixing':['1']
                              })    
                  
                 # records = json.loads(data.T.to_json()).values()
                #  collection3.insert(records)
                #  print(data)     
                
#回复广告  因为回复方式是return 所以回复必须放在最后一位。                

               if chu==1:
                  # shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
                 #  shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                  # shijian0=shijian11-datetime.timedelta(days=1)
                 #  shijian01=shijian11-datetime.timedelta(days=2)
                 #  shijian02=shijian11-datetime.timedelta(days=3)
                 #  shijian11=shijian11.strftime("%Y-%m-%d")  
                 #  shijian0=shijian0.strftime("%Y-%m-%d")
                 #  shijian01=shijian01.strftime("%Y-%m-%d")  
                 #  shijian02=shijian02.strftime("%Y-%m-%d")  
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
               elif shou==1:
              #     shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
               #    shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
                #   shijian0=shijian11-datetime.timedelta(days=1)
                 #  shijian01=shijian11-datetime.timedelta(days=2)
                 #  shijian02=shijian11-datetime.timedelta(days=3)
                 #  shijian11=shijian11.strftime("%Y-%m-%d")  
                 #  shijian0=shijian0.strftime("%Y-%m-%d")
                 #  shijian01=shijian01.strftime("%Y-%m-%d")  
                 #  shijian02=shijian02.strftime("%Y-%m-%d")  
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
               elif shouhui==1:
             #      shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
              #     shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
               #    shijian0=shijian11-datetime.timedelta(days=1)
                #   shijian01=shijian11-datetime.timedelta(days=2)
                 #  shijian02=shijian11-datetime.timedelta(days=3)
                  # shijian11=shijian11.strftime("%Y-%m-%d")  
                  # shijian0=shijian0.strftime("%Y-%m-%d")
                  # shijian01=shijian01.strftime("%Y-%m-%d")  
                  # shijian02=shijian02.strftime("%Y-%m-%d")  
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
               elif chuhui==1:
             #      shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
              #     shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
               #    shijian0=shijian11-datetime.timedelta(days=1)
                #   shijian01=shijian11-datetime.timedelta(days=2)
                 #  shijian02=shijian11-datetime.timedelta(days=3)
                  # shijian11=shijian11.strftime("%Y-%m-%d")  
     #              shijian0=shijian0.strftime("%Y-%m-%d")
      #             shijian01=shijian01.strftime("%Y-%m-%d")  
       #            shijian02=shijian02.strftime("%Y-%m-%d")  
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
               elif shoudai==1:
          #         shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
           #        shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
            #       shijian0=shijian11-datetime.timedelta(days=1)
             #      shijian01=shijian11-datetime.timedelta(days=2)
              #     shijian02=shijian11-datetime.timedelta(days=3)
               #    shijian11=shijian11.strftime("%Y-%m-%d")  
                #   shijian0=shijian0.strftime("%Y-%m-%d")
                 #  shijian01=shijian01.strftime("%Y-%m-%d")  
                  # shijian02=shijian02.strftime("%Y-%m-%d")  
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
               elif  chudai==1:
        #           shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
         #          shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
          #         shijian0=shijian11-datetime.timedelta(days=1)
           #        shijian01=shijian11-datetime.timedelta(days=2)
            #       shijian02=shijian11-datetime.timedelta(days=3)
             #      shijian11=shijian11.strftime("%Y-%m-%d")  
              #     shijian0=shijian0.strftime("%Y-%m-%d")
               #    shijian01=shijian01.strftime("%Y-%m-%d")  
                #   shijian02=shijian02.strftime("%Y-%m-%d")  
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
       elif string[0]=='福费廷':  
         for i in range(0,num): 
           for j in range(1,76):
                c=fu_df.astype(str).loc[j,'ci'].strip()
                zhao= re.search(c,string[i])
                if zhao:                 
                      shoufu=int(fu_df.astype(str).loc[j,'shoufu'].strip())+shoufu
                      chufu=int(fu_df.astype(str).loc[j,'chufu'].strip())+chufu           
                      break   
           if (shoufu+chufu)>0:
                break
         if shoufu!=0:
             shoufu=1
         if chufu!=0:
             chufu=1
         yefu=shoufu+chufu
         if yefu!=0:
             for j2 in range(1,336):
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
                                     break   #是否要跳出二层循环
         else:
            return('未能识别广告。\n例如:\n“福费廷：收证，**银行0571-88888888”。\n如有疑问请联系微信号：18969901812。')
     #    shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
     #    shijian2=time.strftime('%H:%M',time.localtime(time.time()))
      #   print(shijian11)
      #   print(shijian1) 
         db3=client.piaofen
         collection3=db3.piaofen
         cursor = collection3.find({'time':str(shijian11)})
         df2 = pd.DataFrame(list(cursor))
         contentyy=df2['content'].tolist()
         if(hanglei2==0):
               return('请在广告最后附上所在银行（中介机构暂时不行）。')
         else:
               if (co not in contentyy):
                  data=pd.DataFrame({'time':[shijian11],
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
                              'content':[co],
                              'leixing':['1']
                              })    
                  
                 # records = json.loads(data.T.to_json()).values()
                #  collection3.insert(records)
                #  print(data)     
                
       #回复广告  因为回复方式是return 所以回复必须放在最后一位。                
           
  #             print('shou,%s'%shou)
   #            print('chu,%s'%chu)
    #           print('shouhui,%s'%shouhui)
     #          print('chuhui,%s'%chuhui)
      #         print('shoudai,%s'%shoudai)
       #        print('chudai,%s'%chudai)
        #       print('shoucun,%s'%shoucun)
         #      print('chucun,%s'%chucun)
          #     print('shoufu,%s'%shoufu)
           #    print('chufu,%s'%chufu)
            #   print('shouli,%s'%shouli)
            #   print('chuli,%s'%chuli)               
               if chufu==1:
 #                  shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
  #                 shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
   #                shijian0=shijian11-datetime.timedelta(days=1)
    #               shijian01=shijian11-datetime.timedelta(days=2)
     #              shijian02=shijian11-datetime.timedelta(days=3)
      #             shijian11=shijian11.strftime("%Y-%m-%d")  
       #            shijian0=shijian0.strftime("%Y-%m-%d")
        #           shijian01=shijian01.strftime("%Y-%m-%d")  
         #          shijian02=shijian02.strftime("%Y-%m-%d")  
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
               elif shoufu==1:
    #               shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
     #              shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
      #             shijian0=shijian11-datetime.timedelta(days=1)
       #            shijian01=shijian11-datetime.timedelta(days=2)
        #           shijian02=shijian11-datetime.timedelta(days=3)
         #          shijian11=shijian11.strftime("%Y-%m-%d")  
          #         shijian0=shijian0.strftime("%Y-%m-%d")
           #        shijian01=shijian01.strftime("%Y-%m-%d")  
            #       shijian02=shijian02.strftime("%Y-%m-%d")  
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
                        
                          
#以下一段分析理财                        
       elif string[0]=='理财':     
         for i in range(0,num): 
           for j in range(1,40):
                c=li_df.astype(str).loc[j,'ci'].strip()
                zhao= re.search(c,string[i])
                if zhao:                 
                      shouli=int(li_df.astype(str).loc[j,'shouli'].strip())+shouli
                      chuli=int(li_df.astype(str).loc[j,'chuli'].strip())+chuli           
                      break   
           if (shouli+chuli)>0:
                break
         if shouli!=0:
             shouli=1
         if chuli!=0:
             chuli=1
         yeli=shouli+chuli
         if yeli!=0:
             for j2 in range(1,336):
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
                                     break   #是否要跳出二层循环
         else:
            return('未能识别广告。\n例如:\n“理财：收非保本理财，**银行0571-88888888”。\n如有疑问请联系微信号：18969901812。')
    #     shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
     #    shijian2=time.strftime('%H:%M',time.localtime(time.time()))
      #   print(shijian11)
       #  print(shijian1) 
         db3=client.piaofen
         collection3=db3.piaofen
         cursor = collection3.find({'time':str(shijian11)})
         df2 = pd.DataFrame(list(cursor))
         contentyy=df2['content'].tolist()
         if(hanglei2==0):
               return('请在广告最后附上所在银行（中介机构暂时不行）。')
         else:
               if (co not in contentyy):
                  data=pd.DataFrame({'time':[shijian11],
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
                              'content':[co],
                              'leixing':['1']
                              })    
                  
          #        records = json.loads(data.T.to_json()).values()
           #       collection3.insert(records)
            #      print(data)     
                
       #回复广告  因为回复方式是return 所以回复必须放在最后一位。                
           
 #              print('shou,%s'%shou)
  #             print('chu,%s'%chu)
   #            print('shouhui,%s'%shouhui)
    #           print('chuhui,%s'%chuhui)
     #          print('shoudai,%s'%shoudai)
      #         print('chudai,%s'%chudai)
       #        print('shoucun,%s'%shoucun)
        #       print('chucun,%s'%chucun)
          #     print('shoufu,%s'%shoufu)
           #    print('chufu,%s'%chufu)
            #   print('shouli,%s'%shouli)
             #  print('chuli,%s'%chuli)               
               if chuli==1:
  #                 shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
   #                shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
    #               shijian0=shijian11-datetime.timedelta(days=1)
     #              shijian01=shijian11-datetime.timedelta(days=2)
      #             shijian02=shijian11-datetime.timedelta(days=3)
       #            shijian11=shijian11.strftime("%Y-%m-%d")  
        #           shijian0=shijian0.strftime("%Y-%m-%d")
         #          shijian01=shijian01.strftime("%Y-%m-%d")  
          #         shijian02=shijian02.strftime("%Y-%m-%d")  
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
               elif shouli==1:
#                   shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
 #                  shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
  #                 shijian0=shijian11-datetime.timedelta(days=1)
   #                shijian01=shijian11-datetime.timedelta(days=2)
    #               shijian02=shijian11-datetime.timedelta(days=3)
     #              shijian11=shijian11.strftime("%Y-%m-%d")  
      #             shijian0=shijian0.strftime("%Y-%m-%d")
       #            shijian01=shijian01.strftime("%Y-%m-%d")  
        #           shijian02=shijian02.strftime("%Y-%m-%d")  
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
       elif string[0]=='存单':     
         for i in range(0,num): 
           for j in range(1,75):
                c=cun_df.astype(str).loc[j,'ci'].strip()
                zhao= re.search(c,string[i])
                if zhao:                 
                      shoucun=int(cun_df.astype(str).loc[j,'shoucun'].strip())+shoucun
                      chucun=int(cun_df.astype(str).loc[j,'chucun'].strip())+chucun          
                      break   
           if (shoucun+chucun)>0:
                break
         if shoucun!=0:
             shoucun=1
         if chucun!=0:
             chucun=1
         yecun=shoucun+chucun
         if yecun!=0:
             for j2 in range(1,336):
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
                                     break   #是否要跳出二层循环
         else:
            return('未能识别广告。\n例如:\n“存单：收3个月存单，**银行0571-88888888”。\n如有疑问请联系微信号：18969901812。')
 #        shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
  #       shijian2=time.strftime('%H:%M',time.localtime(time.time()))
   #      print(shijian11)
    #     print(shijian1) 
         db3=client.piaofen
         collection3=db3.piaofen
         cursor = collection3.find({'time':str(shijian11)})
         df2 = pd.DataFrame(list(cursor))
         contentyy=df2['content'].tolist()
         if(hanglei2==0):
               return('请在广告最后附上所在银行（中介机构暂时不行）。')
         else:
               if (co not in contentyy):
                  data=pd.DataFrame({'time':[shijian11],
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
                              'content':[co],
                              'leixing':['1']
                              })    
                  
               #   records = json.loads(data.T.to_json()).values()
                #  collection3.insert(records)
                #  print(data)     
                
       #回复广告  因为回复方式是return 所以回复必须放在最后一位。                
           
#               print('shou,%s'%shou)
 #              print('chu,%s'%chu)
  #             print('shouhui,%s'%shouhui)
   #            print('chuhui,%s'%chuhui)
    #           print('shoudai,%s'%shoudai)
     #          print('chudai,%s'%chudai)
      #         print('shoucun,%s'%shoucun)
       #        print('chucun,%s'%chucun)
        #       print('shoufu,%s'%shoufu)
         #      print('chufu,%s'%chufu)
          #     print('shouli,%s'%shouli)
           #    print('chuli,%s'%chuli)               
               if chucun==1:
            #       shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
             #      shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
              #     shijian0=shijian11-datetime.timedelta(days=1)
               #    shijian01=shijian11-datetime.timedelta(days=2)
                #   shijian02=shijian11-datetime.timedelta(days=3)
                 #  shijian11=shijian11.strftime("%Y-%m-%d")  
                  # shijian0=shijian0.strftime("%Y-%m-%d")
         #          shijian01=shijian01.strftime("%Y-%m-%d")  
          #         shijian02=shijian02.strftime("%Y-%m-%d")  
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
               elif shoucun==1:
  #                 shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
   #                shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
    #               shijian0=shijian11-datetime.timedelta(days=1)
     #              shijian01=shijian11-datetime.timedelta(days=2)
      #             shijian02=shijian11-datetime.timedelta(days=3)
       #            shijian11=shijian11.strftime("%Y-%m-%d")  
        #           shijian0=shijian0.strftime("%Y-%m-%d")
         #          shijian01=shijian01.strftime("%Y-%m-%d")  
          #         shijian02=shijian02.strftime("%Y-%m-%d")  
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
                           #itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                           count+=1
                   print(huifu)
                   return(huifu)           
                
                
                
                
                
                
                
                
                
                
                
                
       else:
           return('您可发送指令获得服务。指令可以是单个短句，也可以是多个短句，中间用空格或标点隔开。\n目前您可使用如下11条指令\n“资讯”——获得最新金融新闻。\n“资讯”+“搜索关键词”——检索文章。\n“获取号”——获得单篇资讯。\n“票据分析”——获得票据市场数据。\n“票据”+“广告”——获得对应方向广告。\n“理财分析”——获得理财市场数据。\n“理财”+“广告”——获得对应方向广告。\n“福费廷分析”——获得福费廷市场数据。\n“福费廷”+“广告”——获得对应方向广告。\n“存单分析”——获得存单市场数据。\n“存单”+“广告”——获得对应方向广告。')
itchatmp.run()

