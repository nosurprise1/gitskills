import os
import re
import time
import csv
from itchatmp.content import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
# 在注册时增加isGroupChat=True将判定为群聊回复
#总共有单独回复、群聊分析、群发广告、csv群发四块功能。

zhongjie=[u'浙江邮储杨炳']  #个人发送
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties  
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)  
  #用于在散点图中输出中文




itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wxdca1daea0b4961c4',
    appSecret = 'c0254c2306907abf729b98c38e9eaf55'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
     return(msg['Content'])
     return("1")
     guang=[]
     count=0
     friend=itchatmp.search_friends(userName=msg['FromUserName'])
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
             with open('piao.csv','rb') as csvfile:   #一、以下一段是查找银行类别
                reader = csv.DictReader(csvfile)    #用dictreader根据行内容查找
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
         if shou<>0:
             shou=1
             chufa=1
         if chu<>0:
             chu=1
             shoufa=1
         if shoudai<>0:
             shoudai=1
             chudaifa=1
         if chudai<>0:
             chudai=1
             shoudaifa=1
         if shouhui<>0:
             shouhui=1
             chuhuifa=1
         if chuhui<>0:
             chuhui=1
             shouhuifa=1
         yepiao=shou+chu+shoudai+chudai+shouhui+chuhui
         if yepiao!=0:
           content.append(msg['Content'])             
           for j2 in range(1,326):
                if bank_df.astype(str).loc[j2,'yinhang'].strip() in (msg['ActualNickName']): 
                       hanglei1=bank_df.astype(str).loc[j2,'fenlei1'].strip()
                       hanglei2=bank_df.astype(str).loc[j2,'fenlei2'].strip()
                       hanglei3=bank_df.astype(str).loc[j2,'fenlei3'].strip()
                       break
                else:
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
           name=msg['ActualNickName']    #ËÄ¡¢¼ÇÂ¼µ½csvÉÏ£¬Ö®ËùÒÔÓÃ¼¸¸ö±äÁ¿£¬ÊÇÒªÓÃ±àÂëGB18030£¬ÏÔµÃ¶ÌÒ»µã
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
                              'content':[msg['Content']],
                              'leixing':['2']
                              })
    #hanglei3,hanglei1,name,shou,chu,shoudai,chudai,shouhui,chuhui,shoufu,chufu,shouli,chuli,shoucun,chucun,msg['Content'],'2']
           
           #writer = csv.writer(csvfile)
           #writer.writerow(data)
           #csvfile.close()
           print(data)      
           #print collection
           records = json.loads(data.T.to_json()).values()
           collection3.insert(records)
       
  


    
     

     if shoufa==1 and chufa==0 and shoudaifa==0 and chudaifa==0 and shoufufa==0 and chufufa==0 and shoulifa==0 and chulifa==0 and shoucunfa==0 and chucunfa==0:
          for i in range(0,a-1):
              if data.ix[a-1-i,'shou']==1 and (data.ix[a-1-i,'hanglei2']==1 ) and (count<8) and (data.ix[a-1-i,'content'] not in guang)and (friend['NickName'] <> data.ix[a-1-i,'nickname'] ):                  
                  itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                  guang.append(data.ix[a-1-i,'content'])      
                  count+=1
     elif shoufa==0 and chufa==1 and shoudaifa==0 and chudaifa==0 and shoufufa==0 and chufufa==0 and shoulifa==0 and chulifa==0 and shoucunfa==0 and chucunfa==0:
          for i in range(0,a-1):
              if data.ix[a-1-i,'chu']==1 and (data.ix[a-1-i,'hanglei2']==1 ) and (count<8) and (data.ix[a-1-i,'content'] not in guang)and(friend['NickName'] <> data.ix[a-1-i,'nickname'] ):
                  itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                  guang.append(data.ix[a-1-i,'content'])      
                  count+=1
     elif shoufa==0 and chufa==0 and shoudaifa==1 and chudaifa==0 and shoufufa==0 and chufufa==0 and shoulifa==0 and chulifa==0 and shoucunfa==0 and chucunfa==0:
          for i in range(0,a-1):
              if data.ix[a-1-i,'shoudai']==1 and (data.ix[a-1-i,'hanglei2']==1 ) and (count<8) and (data.ix[a-1-i,'content'] not in guang)and(friend['NickName'] <>data.ix[a-1-i,'nickname'] ):
                  itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                  guang.append(data.ix[a-1-i,'content'])      
                  count+=1
     elif shoufa==0 and chufa==0 and shoudaifa==0 and chudaifa==1 and shoufufa==0 and chufufa==0 and shoulifa==0 and chulifa==0 and shoucunfa==0 and chucunfa==0:
          for i in range(0,a-1):
              if data.ix[a-1-i,'chudai']==1 and (data.ix[a-1-i,'hanglei2']==1 ) and (count<8) and (data.ix[a-1-i,'content'] not in guang)and(friend['NickName'] <>data.ix[a-1-i,'nickname'] ):
                  itchatmp.send('%s,%s:%s'%(data.ix[a-1-i,'time2'],data.ix[a-1-i,'nickname'],data.ix[a-1-i,'content']),msg['FromUserName'])
                  guang.append(data.ix[a-1-i,'content'])      
                  count+=1

   
     #else:
          #itchat.send(u'不能识别您的广告，或者您发送了多方向广告。发送业务广告精准对接，发送“s”了解收票情况，发送“m”了解卖票情况',msg['FromUserName'])
          #itchat.send('@img@%s' % 'guanggao.png',msg['FromUserName'])
#银行客户的私人群功能







itchatmp.run()
