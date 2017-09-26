import itchat,re
import time,csv,datetime
from itchat.content import *

import json
import pandas as pd
from pymongo import MongoClient
content=[]


client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')


db = client.piao
collection = db.piao  
cursor = collection.find()
piao_df= pd.DataFrame(list(cursor))
piao_df=piao_df[['xuhao','ci','shou','chu','shoudai','chudai','shouhui','chuhui']]
piao_df=piao_df.set_index('xuhao')
piao_df=piao_df.sort_index(ascending=True)
#print (piao_df)

db2 = client.bank
collection2 = db2.bank   
cursor2 = collection2.find()
bank_df = pd.DataFrame(list(cursor2))
bank_df=bank_df[['xuhao','yinhang','fenlei1','fenlei2','fenlei3']]
bank_df=bank_df.set_index('xuhao')
bank_df=bank_df.sort_index(ascending=True)
#print (bank_df)

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





    

@itchat.msg_register(TEXT, isGroupChat = True)
def groupchat_reply(msg):
    global content
    hanglei1='中介'
    hanglei2=0
    hanglei3=0
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
    co=re.compile(u'[\U00010000-\U0010ffff]')
    co=co.sub(u'',msg['Content'])
    shijian11=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    
   # shijian11=shijian11.strftime("%y-%m-%d")
   # print(shijian11)
    db_piaofen=client.piaofen
    collection3=db_piaofen.piaofen
    cursor = collection3.find({'time':str(shijian11)})
    #cursor = collection3.find({'time':'2017-09-01'})
    df2 = pd.DataFrame(list(cursor))
    #判断df2是否是空的。
    if df2.empty:
      contentyy=[]
    else:
      contentyy=df2['content'].tolist()

    #print(contentyy)
    
    if (co) not in content:
       string=re.split('；|。|？|！|~~|，| |…',co)
       num=len(string)     
       if num<=30:           
         for i in range(0,num):          
                for j in range(1,164):     #############
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



         for i in range(0,num):          
                for j in range(1,40):     
                    c=li_df.astype(str).loc[j,'ci'].strip()
                  
                    zhaop= re.search(c,string[i])
                    if zhaop:
                             
                      shouli=int(li_df.astype(str).loc[j,'shouli'].strip())+shouli
                      chuli=int(li_df.astype(str).loc[j,'chuli'].strip())+chuli
                      break
         if shouli!=0:
             shouli=1
         if chuli!=0:
             chuli=1
         
         yeli=shouli+chuli
  


         for i in range(0,num):          
                for j in range(1,76):     
                    c=fu_df.astype(str).loc[j,'ci'].strip()
                  
                    zhaop= re.search(c,string[i])
                    if zhaop:
                             
                      shoufu=int(fu_df.astype(str).loc[j,'shoufu'].strip())+shoufu
                      chufu=int(fu_df.astype(str).loc[j,'chufu'].strip())+chufu
                      break
         if shoufu!=0:
             shoufu=1
         if chufu!=0:
             chufu=1
         
         yefu=shoufu+chufu
  
         for i in range(0,num):          
                for j in range(1,75):     
                    c=cun_df.astype(str).loc[j,'ci'].strip()
                  
                    zhaop= re.search(c,string[i])
                    if zhaop:
                             
                      shoucun=int(cun_df.astype(str).loc[j,'shoucun'].strip())+shoucun
                      chucun=int(cun_df.astype(str).loc[j,'chucun'].strip())+chucun
                      break
         if shoucun!=0:
             shoucun=1
         if chucun!=0:
             chucun=1
         
         yecun=shoucun+chucun
##################
         
       if (yepiao+yeli+yecun+yefu)!=0:
           content.append(co)               #     
           for j2 in range(1,336):
                if bank_df.astype(str).loc[j2,'yinhang'].strip() in (msg['ActualNickName']): 
                       hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                       hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                       hanglei3=int(bank_df.astype(str).loc[j2,'fenlei3'].strip())
                       break
                else:
                      if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[num-1]:
                           hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                           hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                           hanglei3=int(bank_df.astype(str).loc[j2,'fenlei3'].strip())
                           break
                      else:
                            if num-2>=0:
                                if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[num-2]:
                                     hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                     hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                                     hanglei3=int(bank_df.astype(str).loc[j2,'fenlei3'].strip())
                                     break
                                else:
                                     if num-3>=0:
                                          if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[num-3]:
                                               hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                               hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                                               hanglei3=int(bank_df.astype(str).loc[j2,'fenlei3'].strip())
                                               break
                                          else:
                                                 if bank_df.astype(str).loc[j2,'yinhang'].strip() in string[0]:
                                                         hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                                                         hanglei2=int(bank_df.astype(str).loc[j2,'fenlei2'].strip())
                                                         hanglei3=int(bank_df.astype(str).loc[j2,'fenlei3'].strip())
                                                         break
           name=msg['ActualNickName']    
           shijian1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
           shijian2=time.strftime('%H:%M',time.localtime(time.time()))
           data=pd.DataFrame({'time':[shijian1],
                              'time2':[shijian2],
                              'hanglei2':[hanglei2],
                              'hanglei3':[hanglei3],
                              'hanglei1':[hanglei1],
                              'nickname':[name],
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
                              'leixing':['3']
                              })   

           data.to_csv('record.csv',mode='a',header=False)
#将没有在数据库中的数据存入           
           if co not in contentyy:
                
                
                records = json.loads(data.T.to_json()).values()
                collection3.insert(records)
                
                



#输出票据的广告
           if yepiao!=0:          
               print(shijian1,end='，')
               print(shijian2,end='，')
               print(hanglei3,end='，')
               print(name,end='，')
               print(co,end='，')  
               print('')
               print('')

itchat.auto_login()
itchat.run()



   

