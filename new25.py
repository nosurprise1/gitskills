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
     zixun='最新资讯：\r\n'
     co=re.compile(u'[\U00010000-\U0010ffff]')
     co=co.sub(u'',msg['Content'])
     string=re.split('；|：|。|？|！|~~|，| |…',co)   #将字符串分割，中午字符串分割需要用u
     while '' in string:
        string.remove('')
     num=len(string)     #计量列表长
     print(num)
     if num>8:
         return('欢迎您使用汇票交易发送广告，我提供票据、福费廷、存单、理财四种广告对接业务。\n为了提高效率，您在发送给我广告时，请勿输入过多短句，请控制在8个句子以内。')#为防止数量太大占内存          
     else:
       
    
    
       if co=='资讯':
          shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          shijiand=time.strftime('%H:%M:%S',time.localtime(time.time()))  
          print(shijiand)
          if  shijiand <='08:35:00':  #早间新闻
              print('早间新闻')
              db3 = client.zixun
              collection3 = db3.zixun   
              cursor3 = collection3.find({"$and":[{'标签1':'金融资讯'},{'时间':{'$lte':'06:00:00'}},
                                             {'爬取日期':str(shijian2)}
                                              ]})    
              zixun_df = pd.DataFrame(list(cursor3))
              zixun_df = zixun_df.sort_values(by='时间', ascending=True)
              zixun_df =  zixun_df.reset_index(drop=True)  
              a=len(zixun_df)
              len0=min(a,18)
              print(len0)
              for i in range(0,len0):       
                           huifu0=('%s,%s 获取号：%s'%(zixun_df.ix[a-1-i,'时间'],zixun_df.ix[a-1-i,'标题'],zixun_df.ix[a-1-i,'获取号']))
                           print(huifu0)
                           zixun=('%s\r\n%s')%(zixun,huifu0)
                           count+=1
              print(zixun)
              return(zixun)
          elif  shijiand >'8:05:00'  and  shijiand <='10:00:00':  #6点到8点的新闻
              db3 = client.zixun
              collection3 = db3.zixun   
              cursor3 = collection3.find({"$and":[{'标签1':'金融资讯'},{'时间':{'$lte':'08:00:00'}},
                                             {'爬取日期':str(shijian2)}
                                              ]})    
              zixun_df = pd.DataFrame(list(cursor3))
              zixun_df = zixun_df.sort_values(by='时间', ascending=True)
              zixun_df =  zixun_df.reset_index(drop=True)  
              a=len(zixun_df)
              len0=min(a,18)
              print(len0)
              for i in range(0,len0):       
                           huifu0=('%s,%s 获取号：%s'%(zixun_df.ix[a-1-i,'时间'],zixun_df.ix[a-1-i,'标题'],zixun_df.ix[a-1-i,'获取号']))
                           print(huifu0)
                           zixun=('%s\r\n%s')%(zixun,huifu0)
                           count+=1
              print(zixun)
              return(zixun) 
          elif  shijiand >'10:00:00'  and  shijiand <='12:00:00':  #8点到9点的新闻
              db3 = client.zixun
              collection3 = db3.zixun   
              cursor3 = collection3.find({"$and":[{'标签1':'金融资讯'},{'时间':{'$lte':'09:00:00'}},
                                             {'爬取日期':str(shijian2)}
                                              ]})    
              zixun_df = pd.DataFrame(list(cursor3))
              zixun_df = zixun_df.sort_values(by='时间', ascending=True)
              zixun_df =  zixun_df.reset_index(drop=True)  
              a=len(zixun_df)
              len0=min(a,18)
              print(len0)
              for i in range(0,len0):       
                           huifu0=('%s,%s 获取号：%s'%(zixun_df.ix[a-1-i,'时间'],zixun_df.ix[a-1-i,'标题'],zixun_df.ix[a-1-i,'获取号']))
                           print(huifu0)
                           zixun=('%s\r\n%s')%(zixun,huifu0)
                           count+=1
              print(zixun)
              return(zixun) 
                                                  
          elif  shijiand >'12:00:00'  and  shijiand <='14:00:00':  #
              db3 = client.zixun
              collection3 = db3.zixun   
              cursor3 = collection3.find({"$and":[{'标签1':'金融资讯'},{'时间':{'$lte':'11:00:00'}},
                                             {'爬取日期':str(shijian2)}
                                              ]})    
              zixun_df = pd.DataFrame(list(cursor3))
              zixun_df = zixun_df.sort_values(by='时间', ascending=True)
              zixun_df =  zixun_df.reset_index(drop=True)  
              a=len(zixun_df)
              len0=min(a,18)
              print(len0)
              for i in range(0,len0):       
                           huifu0=('%s,%s 获取号：%s'%(zixun_df.ix[a-1-i,'时间'],zixun_df.ix[a-1-i,'标题'],zixun_df.ix[a-1-i,'获取号']))
                           print(huifu0)
                           zixun=('%s\r\n%s')%(zixun,huifu0)
                           count+=1
              print(zixun)
              return(zixun)  
          elif  shijiand >'14:00:00'  and  shijiand <='15:00:00':  #11点到15点的新闻
              db3 = client.zixun
              collection3 = db3.zixun   
              cursor3 = collection3.find({"$and":[{'标签1':'金融资讯'},{'时间':{'$lte':'15:00:00'}},
                                             {'爬取日期':str(shijian2)}
                                              ]})    
              zixun_df = pd.DataFrame(list(cursor3))
              zixun_df = zixun_df.sort_values(by='时间', ascending=True)
              zixun_df =  zixun_df.reset_index(drop=True)  
              a=len(zixun_df)
              len0=min(a,18)
              print(len0)
              for i in range(0,len0):       
                           huifu0=('%s,%s 获取号：%s'%(zixun_df.ix[a-1-i,'时间'],zixun_df.ix[a-1-i,'标题'],zixun_df.ix[a-1-i,'获取号']))
                           print(huifu0)
                           zixun=('%s\r\n%s')%(zixun,huifu0)
                           count+=1
              print(zixun)
              return(zixun)                                          
          elif  shijiand >'15:00:00' :  #看15点的新闻
              print('晚间新闻')
              db3 = client.zixun
              collection3 = db3.zixun   
              cursor3 = collection3.find({"$and":[{'标签1':'金融资讯'},
                                             {'爬取日期':str(shijian2)}
                                              ]})    
              zixun_df = pd.DataFrame(list(cursor3))
              zixun_df=zixun_df[['时间','标题','获取号']]
              zixun_df = zixun_df.sort_values(by='时间', ascending=True)
              zixun_df =  zixun_df.reset_index(drop=True)    #在排序后如果要按照新的顺序必须把原来的索引删除
              print(zixun_df)
              a=len(zixun_df)
              len0=min(a,18)
              print(len0)
              for i in range(0,len0):       
                           huifu0=('%s,%s  获取号:%s'%(zixun_df.ix[a-1-i,'时间'],zixun_df.ix[a-1-i,'标题'],zixun_df.ix[a-1-i,'获取号']))
                           print(huifu0)
                           zixun=('%s\r\n%s')%(zixun,huifu0)
                           count+=1
              print(zixun)
              return(zixun)                                            
                                                  
                                                  
       if string[0]=='获取号':
          shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          db3 = client.zixun
          collection3 = db3.zixun   
          cursor3 = collection3.find({"$and":[{'标签1':'金融资讯'},
                                             {"$or":[{'爬取日期':str(shijian2)},{'爬取日期':str(shijian0)}]}
                                              ]})    
          zixun_df = pd.DataFrame(list(cursor3))
          a=len(zixun_df)
          for i in range(0,len(zixun_df)):
               if string[1] == str(zixun_df.ix[a-1-i,'获取号']):
                   print('zhaodaole')
                   return(zixun_df.ix[a-1-i,'链接'])
                   
            
            
       elif string[0]=='票据分析':
          shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian2)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          if piaofen_df.empty:
            return('暂无当日数据，请稍后再试。')
        #做表
          huatudata3=piaofen_df[['hanglei1','shou','chu','shoudai','chudai','shouhui','chuhui']]
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shou': '收', 'chu': '出', 'shoudai': '收代', 'chudai': '出代', 'shouhui':'收回',  'chuhui':'出回'}) 
          huatudata4=huatudata4.set_index('机构')
          print(huatudata4)
          return(str(huatudata4))
       elif string[0]=='福费廷分析':
          shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian2)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          if piaofen_df.empty:
            return('暂无当日数据，请稍后再试。')          #做表
          huatudata3=piaofen_df[['hanglei1','shoufu','chufu']]
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shoufu': '收', 'chufu': '出'}) 
          huatudata4=huatudata4.set_index('机构')
          print(huatudata4)
          return(str(huatudata4))            
       elif string[0]=='存单分析':
          shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian2)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          if piaofen_df.empty:
            return('暂无当日数据，请稍后再试。')          #做表
          huatudata3=piaofen_df[['hanglei1','shoucun','chucun']]
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shoucun': '收', 'chucun': '出'}) 
          huatudata4=huatudata4.set_index('机构')
          print(huatudata4)
          return(str(huatudata4))     
       elif string[0]=='理财分析':
          shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian2)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          if piaofen_df.empty:
            return('暂无当日数据，请稍后再试。')          #做表
          huatudata3=piaofen_df[['hanglei1','shouli','chuli']]
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shouli': '收', 'chuli': '出'}) 
          huatudata4=huatudata4.set_index('机构')
          print(huatudata4)
          return(str(huatudata4))     
        
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
            return('抱歉，未能识别您的广告。\n我提供票据、福费廷、存单、理财四种广告对接业务。例如“票据。收跨年票，**银行0571-88888888”。\n如有疑问请联系微信号：18969901812。')
         shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
         shijian2=time.strftime('%H:%M',time.localtime(time.time()))
         print(shijian11)
         print(shijian1) 
         db3=client.piaofen
         collection3=db3.piaofen
         cursor = collection3.find({'time':str(shijian11)})
         df2 = pd.DataFrame(list(cursor))
         contentyy=df2['content'].tolist()
         if(hanglei2==0):
               return('请您务必广告最后带上所在银行及联系方式。')
         else:
               if (co not in contentyy):
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
                              'content':[co],
                              'leixing':['1']
                              })    
                  
                  records = json.loads(data.T.to_json()).values()
                  collection3.insert(records)
                  print(data)     
                
#回复广告  因为回复方式是return 所以回复必须放在最后一位。                
           
               print('shou,%s'%shou)
               print('chu,%s'%chu)
               print('shouhui,%s'%shouhui)
               print('chuhui,%s'%chuhui)
               print('shoudai,%s'%shoudai)
               print('chudai,%s'%chudai)
               print('shoucun,%s'%shoucun)
               print('chucun,%s'%chucun)
               print('shoufu,%s'%shoufu)
               print('chufu,%s'%chufu)
               print('shouli,%s'%shouli)
               print('chuli,%s'%chuli)               
               if chu==1:
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
               elif shou==1:
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
               elif shouhui==1:
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
               elif chuhui==1:
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
               elif shoudai==1:
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
               elif  chudai==1:
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
            return('抱歉，未能识别您的广告。\n我提供票据、福费廷、存单、理财四种广告对接业务。例如“福费廷。收证，**银行0571-88888888”。\n如有疑问请联系微信号：18969901812。')
         shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
         shijian2=time.strftime('%H:%M',time.localtime(time.time()))
         print(shijian11)
         print(shijian1) 
         db3=client.piaofen
         collection3=db3.piaofen
         cursor = collection3.find({'time':str(shijian11)})
         df2 = pd.DataFrame(list(cursor))
         contentyy=df2['content'].tolist()
         if(hanglei2==0):
               return('请您务必广告最后带上所在银行及联系方式。')
         else:
               if (co not in contentyy):
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
                              'content':[co],
                              'leixing':['1']
                              })    
                  
                  records = json.loads(data.T.to_json()).values()
                  collection3.insert(records)
                  print(data)     
                
       #回复广告  因为回复方式是return 所以回复必须放在最后一位。                
           
               print('shou,%s'%shou)
               print('chu,%s'%chu)
               print('shouhui,%s'%shouhui)
               print('chuhui,%s'%chuhui)
               print('shoudai,%s'%shoudai)
               print('chudai,%s'%chudai)
               print('shoucun,%s'%shoucun)
               print('chucun,%s'%chucun)
               print('shoufu,%s'%shoufu)
               print('chufu,%s'%chufu)
               print('shouli,%s'%shouli)
               print('chuli,%s'%chuli)               
               if chufu==1:
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
            return('抱歉，未能识别您的广告。\n我提供票据、福费廷、存单、理财四种广告对接业务。例如“理财。收非保本理财，**银行0571-88888888”。\n如有疑问请联系微信号：18969901812。')
         shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
         shijian2=time.strftime('%H:%M',time.localtime(time.time()))
         print(shijian11)
         print(shijian1) 
         db3=client.piaofen
         collection3=db3.piaofen
         cursor = collection3.find({'time':str(shijian11)})
         df2 = pd.DataFrame(list(cursor))
         contentyy=df2['content'].tolist()
         if(hanglei2==0):
               return('请您务必广告最后带上所在银行及联系方式。')
         else:
               if (co not in contentyy):
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
                              'content':[co],
                              'leixing':['1']
                              })    
                  
                  records = json.loads(data.T.to_json()).values()
                  collection3.insert(records)
                  print(data)     
                
       #回复广告  因为回复方式是return 所以回复必须放在最后一位。                
           
               print('shou,%s'%shou)
               print('chu,%s'%chu)
               print('shouhui,%s'%shouhui)
               print('chuhui,%s'%chuhui)
               print('shoudai,%s'%shoudai)
               print('chudai,%s'%chudai)
               print('shoucun,%s'%shoucun)
               print('chucun,%s'%chucun)
               print('shoufu,%s'%shoufu)
               print('chufu,%s'%chufu)
               print('shouli,%s'%shouli)
               print('chuli,%s'%chuli)               
               if chuli==1:
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
            return('抱歉，未能识别您的广告。\n我提供票据、福费廷、存单、理财四种广告对接业务。例如“存单。收3个月存单，**银行0571-88888888”。\n如有疑问请联系微信号：18969901812。')
         shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
         shijian2=time.strftime('%H:%M',time.localtime(time.time()))
         print(shijian11)
         print(shijian1) 
         db3=client.piaofen
         collection3=db3.piaofen
         cursor = collection3.find({'time':str(shijian11)})
         df2 = pd.DataFrame(list(cursor))
         contentyy=df2['content'].tolist()
         if(hanglei2==0):
               return('请您务必广告最后带上所在银行及联系方式。')
         else:
               if (co not in contentyy):
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
                              'content':[co],
                              'leixing':['1']
                              })    
                  
                  records = json.loads(data.T.to_json()).values()
                  collection3.insert(records)
                  print(data)     
                
       #回复广告  因为回复方式是return 所以回复必须放在最后一位。                
           
               print('shou,%s'%shou)
               print('chu,%s'%chu)
               print('shouhui,%s'%shouhui)
               print('chuhui,%s'%chuhui)
               print('shoudai,%s'%shoudai)
               print('chudai,%s'%chudai)
               print('shoucun,%s'%shoucun)
               print('chucun,%s'%chucun)
               print('shoufu,%s'%shoufu)
               print('chufu,%s'%chufu)
               print('shouli,%s'%shouli)
               print('chuli,%s'%chuli)               
               if chucun==1:
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
           return('欢迎您使用汇票交易广告撮合功能。\n请在您想要发送的广告前面加上“票据。”，“福费廷。”，“存单。”或“理财。”，\n选择一个业务方向，我才能为您对接广告。\n例如“票据。收各期限国股承兑电银，工行***0571-88888888”，\n注意：如果您想别人能及时联系到您，发送广告务必带上联系方式！\n没有业务需求时，也可以通过发送‘票据分析’、“福费廷分析”、“存单分析”或"理财分析"单独指令来了解当日实时的市场情况。')
         

       
           
           
                
        
        
itchatmp.run()

