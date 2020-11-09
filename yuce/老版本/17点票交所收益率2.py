import pandas as pd
from bs4 import BeautifulSoup
import urllib
import requests
from pymongo import MongoClient
import cgi
import re,datetime,json
from math import  floor
#设置try的次数
maxTryNum=20
maxTryNum1=6
st=0
import time, sched
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from collections import Counter

#import jieba,os,codecs,re
#import jieba.analyse,time
#import json,csv,re,time,datetime
#from wordcloud import WordCloud

import arrow #datatime的加强版
xlsname=''


#二、用下载下来 excel更新数据

nomonth = arrow.now()   #当前月
yuefen=[]
yuefen.append(nomonth.month)
for i in range(1,13): 
    yuefen.append(nomonth.shift(months=i).month)
print(yuefen)
qixianxin=['月内(%s月到期)'%yuefen[0],'1M/12月','2M/12月','3M/1月','4M/2月','5M/3月','6M/4月','7M/5月','8M/6月','9M/7月','10M/8月','11M/9月','10M/10月']
print(qixianxin)

import matplotlib as mpl   #显示中文

from matplotlib.font_manager import FontProperties  
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=9) #用于在散点图中输出中文


font_set2 = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=9) #用于在散点图中输出中文
shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
shijian = datetime.datetime.strptime(shijian, "%Y-%m-%d")
shijian2=shijian-datetime.timedelta(days=7)
shijian2=str(shijian2.strftime("%Y-%m-%d"))
shijian=str(shijian.strftime("%Y-%m-%d"))

zixun=''
client=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')
db = client.piaofen
collection = db.piaofen

db18=client.lilvquxian
collection18 = db18.lilvquxian

#一、更新利率曲线    
shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
import datetime
shijian = datetime.datetime.strptime(shijian, "%Y-%m-%d")

jin=input('    请输入当日日期,输入格式为“2017-01-01”，不输入默认为今天:')
if jin!='':
        shijian0=jin
        shijian=datetime.datetime.strptime(jin , "%Y-%m-%d")

shijian=str(shijian.strftime("%Y-%m-%d"))





headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}    
url2="http://www.shcpe.com.cn/index_132.html"

for tries in range(maxTryNum):
            try:
                req = urllib.request.Request(url2,headers = headers)
                menuCode=urllib.request.urlopen(req).read()  # 将网页源代码赋予menuCode     
                soup=BeautifulSoup(menuCode,'html.parser')  # 使用html解析器进行解析
                data = soup.prettify()
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    print("Has tried %d times to access url %s, all failed!", maxTryNum, url2)
                    print(tries)
                    break

link_list =re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')" ,data)  # 利用正则查找所有连接
for url in link_list:
      if ('uploadfiles' in url) and( '.xls'  in url):
          url=url2+url
          url=url.replace('index_132.html/','')
          print(url)
          
          time.sleep(1)  # 暂停一秒，避免访问过快被反爬机制认为是蜘蛛
          xlsname=url[(len(url)-22):]
          if shijian.replace('-','') not in xlsname:
              print(shijian.replace('-',''))
              print(xlsname)
              print('还没有更新，停止')
              break
          urllib.request.urlretrieve(url,xlsname)















def lilvgengxin():
    global lilvd,collection18
    print('开始执利率曲线更新程序……')
    zhiling=input('    请输入指令“1”来确认执行：')
    if zhiling!='1':
       print('    终止。')
       return
    url='li.csv'


    lilv=pd.read_excel(xlsname,encoding='GB18030')


    for i in range(2,len(lilv)):
        lilv.loc[i,'关键期限']=lilv.loc[i,'关键期限'].replace('1Y','12M').replace('M','月')
        #lilv.loc[i,'关键期限']='%s月'%yuefen[int(lilv.loc[i,'关键期限'].replace('M',''))]

    print(lilv)


    lilv['日期'] = pd.to_datetime(lilv['日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    print(lilv.loc[1,'日期'])
    cursor = collection18.find({ "$and":[{'日期':str(lilv.loc[1,'日期'])} ] })
    lilvd=lilv[['关键期限','利率（%）']]
    lilvqu= pd.DataFrame(list(cursor))
    print(lilvqu)
    
    lilvd = lilvd.set_index('关键期限').T.to_dict('list')
    print(lilvd)
    zong1=pd.DataFrame({lilv.loc[0,'关键期限']: [lilv.loc[0,'利率（%）']],
                             lilv.loc[1,'关键期限']: [lilv.loc[1,'利率（%）']],
                             lilv.loc[2,'关键期限']: [lilv.loc[2,'利率（%）']],
                             lilv.loc[3,'关键期限']: [lilv.loc[3,'利率（%）']],
                             lilv.loc[4,'关键期限']: [lilv.loc[4,'利率（%）']],
                             lilv.loc[5,'关键期限']: [lilv.loc[5,'利率（%）']],
                             lilv.loc[6,'关键期限']: [lilv.loc[6,'利率（%）']],
                             lilv.loc[7,'关键期限']: [lilv.loc[7,'利率（%）']],
                             lilv.loc[8,'关键期限']: [lilv.loc[8,'利率（%）']],
                             lilv.loc[9,'关键期限']: [lilv.loc[9,'利率（%）']],
                             lilv.loc[10,'关键期限']: [lilv.loc[10,'利率（%）']],
                             lilv.loc[11,'关键期限']: [lilv.loc[11,'利率（%）']],
                             lilv.loc[12,'关键期限']: [lilv.loc[12,'利率（%）']],
                             lilv.loc[13,'关键期限']: [lilv.loc[13,'利率（%）']],

                            '日期':[lilv.loc[1,'日期']]
                            
                         })


    if lilvqu.empty:
        records = json.loads(zong1.T.to_json()).values()
        collection18.insert(records)
    else:
        print('已经更新过')


#二、画利率曲线图
def lilvhuatu():
    global collection18,shijian2
    print('开始执利率曲线画图程序……')
    zhiling=input('    请输入指令“1”来确认执行：')
    if zhiling!='1':
       print('    终止。')
       return       
    cursor = collection18.find({'日期':{'$gte':str(shijian2)}})
    lilvqu= pd.DataFrame(list(cursor)) 
    from datetime import datetime
    lilvqu['日期'] = pd.to_datetime(lilvqu['日期']).astype('str')  #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    lilvqu = lilvqu.sort_values(by='日期', ascending=False)
    lilvqu= lilvqu.reset_index(drop=True)    #重新定义索引

    print(lilvqu)
    

    

    for i in range(0,len(lilvqu)):
      y1 = [float(lilvqu.loc[i,'1D']),float(lilvqu.loc[i,'7D']),float(lilvqu.loc[i,'1月']),float(lilvqu.loc[i,'2月']),float(lilvqu.loc[i,'3月']),float(lilvqu.loc[i,'4月']),float(lilvqu.loc[i,'5月']),float(lilvqu.loc[i,'6月']),float(lilvqu.loc[i,'7月']),float(lilvqu.loc[i,'8月']),float(lilvqu.loc[i,'9月']),float(lilvqu.loc[i,'10月']),float(lilvqu.loc[i,'11月']),float(lilvqu.loc[i,'12月'])]
      x = [1,7,30,60,90,120,150,180,210,240,270,300,330,360]
      plt.plot(x,y1,alpha=(1/(i+1)),label='%s'%lilvqu.loc[i,'日期'])
    plt.legend(prop=font_set2)  #显示lable
    plt.ylabel('利率（%）', fontproperties=font_set)
    plt.xlabel('期限（天）', fontproperties=font_set)
    plt.title('%s票交所收益率曲线'%shijian, fontproperties=font_set) 

    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('images/lshouyiquxian.png')   #images/
    fig.show()
    
    #三维图
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(0,len(lilvqu)):
        lilvqu.loc[i,'日期']=round(float(lilvqu.loc[i,'日期'].replace('2019-','').replace('2018-','').replace('-','.')),2)
    print(lilvqu)
    for i in range(0,2):
      zs = [float(lilvqu.loc[i,'1D']),float(lilvqu.loc[i,'7D']),float(lilvqu.loc[i,'1月']),float(lilvqu.loc[i,'2月']),float(lilvqu.loc[i,'3月']),float(lilvqu.loc[i,'4月']),float(lilvqu.loc[i,'5月']),float(lilvqu.loc[i,'6月']),float(lilvqu.loc[i,'7月']),float(lilvqu.loc[i,'8月']),float(lilvqu.loc[i,'9月']),float(lilvqu.loc[i,'10月']),float(lilvqu.loc[i,'11月']),float(lilvqu.loc[i,'12月'])]
      ys = [1,7,30,60,90,120,150,180,210,240,270,300,330,360]
      xs =[i, i, i, i, i, i, i, i, i, i, i, i, i, i]
      ax.plot(xs,ys,zs)
 
    ax.set_xlabel('曲线日期', fontproperties=font_set)
    ax.set_ylabel('期限（天）', fontproperties=font_set)
    ax.set_zlabel('利率（%）', fontproperties=font_set)
    ax.view_init(elev=0, azim=0)
    plt.show()



 




#一、中介卖票
def qixianhuatu():
    global lilvd 
    print('开始执利率群消息期限画图程序……')
    zhiling=input('    请输入指令“1”来确认执行：')
    if zhiling!='1':
       print('    终止。')
       return       
    print('开始中介卖票')
    cursor = collection.find({"$and":[{'time':{'$gte':shijian}},{'hanglei2':0},{'chu':1}]})
    df = pd.DataFrame(list(cursor))

    df = df.sort_values(by='time2', ascending=True)
    df=df.drop_duplicates(['content'],keep='last')   #删除连接中的重复行
    df=df[['content']]
    mai=[]
    mai2=[]
    mai3=[]
    mai4=[]
    mai5=[]
    mai6=[]
    mai61=[]
    mai7=[]
    mai8=[]

    a=len(df)
    df= df.reset_index(drop=True)    #重新定义索引

    for i in range(0,a):
      cp=df.loc[i,'content'].replace('两','2').replace('十二','12').replace('十一','11').replace('十','10').replace('九','9').replace('八','8').replace('七','7').replace('六','6').replace('五','5').replace('四','4').replace('三','3').replace('二','2').replace('一','1')
      cp=cp.replace('足年','1年')
      
      zhaop= re.search('^((?!(谁|有人)).)*(?:出|卖)(?P<name>([^。,，！…；~？]*?)(?:票|电银|足月|1年|\d月|农商|国股|城商))((?!(买返|买入返售|回购|代持|吗|么|找|联系|？)).)*$',cp)
      if zhaop:
          zhaop2= re.findall('([\d]{1,2}(?:-|至|~|、|，|,)[\d]{1,2}(?:月))',cp)  #如11-12月
          if zhaop2:
              mai2=mai2+zhaop2

          
          zhaop3= re.findall('([\d]{1,2}(?:月)(?:-|至|~)[\d]{1,2}(?:月))',cp)  #如11月-12月
          if zhaop3:
              mai3=mai3+zhaop3
              
              
          zhaop4= re.findall('([\d]{1,2}(?:-|至|~|、|，|,)[\d]{1,2}(?:M|个月|m))',cp)  #如4、5个月
          if zhaop4:
              mai4=mai4+zhaop4

          zhaop5= re.findall('(?:1年|一年|足年|半年)',cp)  #足年或者足月或者3个月,(?:)里面不能再嵌套（？：）
          if zhaop5:
             mai5=mai5+zhaop5


          zhaop51= re.findall('([\d]{1,2}个月)',cp)  #足年或者足月或者3个月
          if zhaop51:
             mai5=mai5+zhaop51

          zhaop6= re.findall('[\d]{1,2}月',cp)  #3月
          if zhaop6:
             mai6=mai6+zhaop6


          zhaop7= re.findall('(?:明年%s月|19年%s月)'%(nomonth.month,nomonth.month),cp)  #明年当月到期
          if zhaop7:
             mai7=mai7+zhaop7

          zhaop8= re.findall('(?:月内|当月|跨月|本月|托收|今年%s月|18年%s月)'%(nomonth.month,nomonth.month),cp)  #当月到期票
          if zhaop8:
             mai8=mai8+zhaop8


    print(mai8)
    if mai6:
      while ('%s月'%nomonth.month) in mai6:
        mai6.remove(('%s月'%nomonth.month))

      for i in range(0,len(mai6)):
       if int(mai6[i].replace('月',''))>12:
           print(int(mai6[i].replace('月','')))
           for j in range(0,len(mai6[i].replace('月',''))):
               print('%s月'%(mai6[i].replace('月','')[j]))
               mai6.append('%s月'%(mai6[i].replace('月','')[j]))

           mai6.remove(mai6[i])



   
    if mai7:
      for i in range(0,len(mai7)):
         mai7[i]=('%s月'%nomonth.month)

    if mai8:
      for i in range(0,len(mai8)):
         mai8[i]='当月'


    if mai4:
      yuanl=len(mai4)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai4[i]))
          for j in range(0,(int(zan[1].replace('个月','').replace('M','').replace('m',''))-int(zan[0]))):
             zanhou="%s个月"%(int(zan[0])+j)
             mai4.append(zanhou)
      mai4=mai4[(yuanl):]


    if mai4:
      for i in range(0,len(mai4)):
            if ('个月') in mai4[i]:
              mai4[i]= ('%s月'%(nomonth.shift(months=int(mai4[i].replace('个月',''))).month))



    if mai2:
      yuanl=len(mai2)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai2[i]))
          for j in range(1,(int(zan[1].replace('月',''))-int(zan[0]))): #去掉尾
             zanhou="%s月"%(int(zan[0])+j)
             mai2.append(zanhou)
      mai2=mai2[(yuanl):]



    if mai3:
      yuanl=len(mai3)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai3[i]))
          for j in range(1,(int(zan[1].replace('月',''))-int(zan[0].replace('月','')))):   #去掉头、尾
             zanhou="%s月"%(int(zan[0].replace('月',''))+j)
             mai3.append(zanhou)
      mai3=mai3[(yuanl):]


    if mai5:
      for i in range(0,len(mai5)):


            if mai5[i]=='1年':
               mai5[i]= ('%s月'%(nomonth.shift(months=12).month))
            if ('个月') in mai5[i]:
              mai5[i]= ('%s月'%(nomonth.shift(months=int(mai5[i].replace('个月',''))).month))
            if mai5[i]=='半年':
               mai5[i]= ('%s月'%(nomonth.shift(months=6).month))
               print(mai5[i])
    mai=mai2+mai3+mai4+mai5+mai6+mai7+mai8  #形成最终的关键词列表
    lista=Counter(mai).most_common(30)  #统计出最高频的关键词

    qixianm0=pd.DataFrame({'期限': [lista[0][0]],
                    '中介卖票':[lista[0][1]]
                  })

    for i in range(1,len(lista)):
      qixianm=pd.DataFrame({'期限': [lista[i][0]],
                    '中介卖票':[lista[i][1]]
                  })
      qixianm0= pd.concat([qixianm,qixianm0], axis=0)

    qixian1= qixianm0.reset_index(drop=True)    #重新定义索引
    qixian1=qixian1.set_index(['期限'])

          
    print(qixian1)
      


#二、银行卖票
    print('开始银行卖票')
    cursor = collection.find({"$and":[{'time':{'$gte':shijian}},{'hanglei2':1},{'chu':1}]})
    df = pd.DataFrame(list(cursor))
    mai=[]
    mai2=[]
    mai3=[]
    mai4=[]
    mai5=[]
    mai6=[]
    mai61=[]
    mai7=[]
    mai8=[]

    df = df.sort_values(by='time2', ascending=True)
    df=df.drop_duplicates(['content'],keep='last')   #删除连接中的重复行
    df=df[['content']]

    a=len(df)
    df= df.reset_index(drop=True)    #重新定义索引

    for i in range(0,a):
      cp=df.loc[i,'content'].replace('两','2').replace('十二','12').replace('十一','11').replace('十','10').replace('九','9').replace('八','8').replace('七','7').replace('六','6').replace('五','5').replace('四','4').replace('三','3').replace('二','2').replace('一','1')
      cp=cp.replace('足年','1年')
      zhaop= re.search('^((?!(谁|有人)).)*(?:出|卖)(?P<name>([^。,，！…；~？]*?)(?:票|电银|足月|1年|\d月|农商|国股|城商))((?!(买返|买入返售|回购|代持|吗|么|找|联系|？)).)*$',cp)
      if zhaop:
          zhaop2= re.findall('([\d]{1,2}(?:-|至|~|、|，|,)[\d]{1,2}(?:月))',cp)  #如11-12月
          if zhaop2:
              mai2=mai2+zhaop2

          
          zhaop3= re.findall('([\d]{1,2}(?:月)(?:-|至|~)[\d]{1,2}(?:月))',cp)  #如11月-12月
          if zhaop3:
              mai3=mai3+zhaop3
              
              
          zhaop4= re.findall('([\d]{1,2}(?:-|至|~|、|，|,)[\d]{1,2}(?:M|个月|m))',cp)  #如4、5个月
          if zhaop4:
              mai4=mai4+zhaop4

          zhaop5= re.findall('(?:1年|一年|足年|半年)',cp)  #足年或者足月或者3个月,(?:)里面不能再嵌套（？：）
          if zhaop5:
             mai5=mai5+zhaop5


          zhaop51= re.findall('([\d]{1,2}个月)',cp)  #足年或者足月或者3个月
          if zhaop51:
             mai5=mai5+zhaop51


          zhaop6= re.findall('[\d]{1,2}月',cp)  #3月
          if zhaop6:
             mai6=mai6+zhaop6

          zhaop7= re.findall('(?:明年%s月|19年%s月)'%(nomonth.month,nomonth.month),cp)  #明年当月到期
          if zhaop7:
             mai7=mai7+zhaop7

          zhaop8= re.findall('(?:月内|当月|跨月|本月|托收|今年%s月|18年%s月)'%(nomonth.month,nomonth.month),cp)  #当月到期票
          if zhaop8:
             mai8=mai8+zhaop8


    print(mai8)
    if mai6:
      while ('%s月'%nomonth.month) in mai6:
        mai6.remove(('%s月'%nomonth.month))
      for i in range(0,len(mai6)):
       if int(mai6[i].replace('月',''))>12:
           print(int(mai6[i].replace('月','')))
           for j in range(0,len(mai6[i].replace('月',''))):
               print('%s月'%(mai6[i].replace('月','')[j]))
               mai6.append('%s月'%(mai6[i].replace('月','')[j]))
           mai6.remove(mai6[i])

    if mai7:
      for i in range(0,len(mai7)):
         mai7[i]=('%s月'%nomonth.month)

    if mai8:
      for i in range(0,len(mai8)):
         mai8[i]='当月'

    if mai4:
      yuanl=len(mai4)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai4[i]))
          for j in range(0,(int(zan[1].replace('个月','').replace('M','').replace('m',''))-int(zan[0]))):
             zanhou="%s个月"%(int(zan[0])+j)
             mai4.append(zanhou)
      mai4=mai4[(yuanl):]


    if mai4:
      for i in range(0,len(mai4)):


            if ('个月') in mai4[i]:
              mai4[i]= ('%s月'%(nomonth.shift(months=int(mai4[i].replace('个月',''))).month))


    if mai2:
      yuanl=len(mai2)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai2[i]))
          for j in range(1,(int(zan[1].replace('月',''))-int(zan[0]))):
             zanhou="%s月"%(int(zan[0])+j)
             mai2.append(zanhou)
      mai2=mai2[(yuanl):]



    if mai3:
      yuanl=len(mai3)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai3[i]))
          for j in range(1,(int(zan[1].replace('月',''))-int(zan[0].replace('月','')))):
             zanhou="%s月"%(int(zan[0].replace('月',''))+j)
             mai3.append(zanhou)
      mai3=mai3[(yuanl):]

    if mai5:
      for i in range(0,len(mai5)):


            if mai5[i]=='1年':
               mai5[i]= ('%s月'%(nomonth.shift(months=12).month))
            if ('个月') in mai5[i]:
              mai5[i]= ('%s月'%(nomonth.shift(months=int(mai5[i].replace('个月',''))).month))
            if mai5[i]=='半年':
               mai5[i]= ('%s月'%(nomonth.shift(months=6).month))
               print(mai5[i])
    mai=mai2+mai3+mai4+mai5+mai6+mai7+mai8  #形成最终的关键词列表
    lista=Counter(mai).most_common(30)

    qixianm0=pd.DataFrame({'期限': [lista[0][0]],
                    '银行卖票':[lista[0][1]]
                  })

    for i in range(1,len(lista)):
      qixianm=pd.DataFrame({'期限': [lista[i][0]],
                    '银行卖票':[lista[i][1]]
                  })
      qixianm0= pd.concat([qixianm,qixianm0], axis=0)

    qixian2= qixianm0.reset_index(drop=True)    #重新定义索引
    qixian2=qixian2.set_index(['期限'])

          
    print(qixian2)




      
#三、中介收票
    mai=[]
    mai2=[]
    mai3=[]
    mai4=[]
    mai5=[]
    mai6=[]
    mai61=[]
    mai7=[]
    mai8=[]

    cursor = collection.find({"$and":[{'time':{'$gte':shijian}},{'hanglei2':0},{'shou':1}]})
    df = pd.DataFrame(list(cursor))

    df = df.sort_values(by='time2', ascending=True)
    df=df.drop_duplicates(['content'],keep='last')   #删除连接中的重复行
    df=df[['content']]

    a=len(df)
    df= df.reset_index(drop=True)    #重新定义索引

    for i in range(0,a):
      cp=df.loc[i,'content'].replace('两','2').replace('十二','12').replace('十一','11').replace('十','10').replace('九','9').replace('八','8').replace('七','7').replace('六','6').replace('五','5').replace('四','4').replace('三','3').replace('二','2').replace('一','1')
      cp=cp.replace('足年','1年')
      zhaop= re.search('^((?!(谁|有人)).)*(?:收|买)(?P<name>([^。,，！…；~？]*?)(?:票|电银|足月|1年|\d月|农商|国股|城商))((?!(买返|买入返售|回购|代持|吗|么|找|联系|？)).)*$',cp)
      if zhaop:
          zhaop2= re.findall('([\d]{1,2}(?:-|至|~|、|，|,)[\d]{1,2}(?:月))',cp)  #如11-12月
          if zhaop2:
              mai2=mai2+zhaop2

          
          zhaop3= re.findall('([\d]{1,2}(?:月)(?:-|至|~)[\d]{1,2}(?:月))',cp)  #如11月-12月
          if zhaop3:
              mai3=mai3+zhaop3
              
              
          zhaop4= re.findall('([\d]{1,2}(?:-|至|~|、|，|,)[\d]{1,2}(?:M|个月|m))',cp)  #如4、5个月
          if zhaop4:
              mai4=mai4+zhaop4

          zhaop5= re.findall('(?:1年|一年|足年|半年)',cp)  #足年或者足月或者3个月,(?:)里面不能再嵌套（？：）
          if zhaop5:
             mai5=mai5+zhaop5


          zhaop51= re.findall('([\d]{1,2}个月)',cp)  #足年或者足月或者3个月
          if zhaop51:
             mai5=mai5+zhaop51


          zhaop6= re.findall('[\d]{1,2}月',cp)  #3月
          if zhaop6:
             mai6=mai6+zhaop6

          zhaop7= re.findall('(?:明年%s月|19年%s月)'%(nomonth.month,nomonth.month),cp)  #明年当月到期
          if zhaop7:
             mai7=mai7+zhaop7

          zhaop8= re.findall('(?:月内|当月|跨月|本月|托收|今年%s月|18年%s月)'%(nomonth.month,nomonth.month),cp)  #当月到期票
          if zhaop8:
             mai8=mai8+zhaop8

    print(mai8)

    if mai6:
      while ('%s月'%nomonth.month) in mai6:
        mai6.remove(('%s月'%nomonth.month))
      for i in range(0,len(mai6)):
       if int(mai6[i].replace('月',''))>12:
           print(int(mai6[i].replace('月','')))
           for j in range(0,len(mai6[i].replace('月',''))):
               print('%s月'%(mai6[i].replace('月','')[j]))
               mai6.append('%s月'%(mai6[i].replace('月','')[j]))
           mai6.remove(mai6[i])

    if mai7:
      for i in range(0,len(mai7)):
         mai7[i]=('%s月'%nomonth.month)

    if mai8:
      for i in range(0,len(mai8)):
         mai8[i]='当月'

    if mai4:
      yuanl=len(mai4)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai4[i]))
          for j in range(0,(int(zan[1].replace('个月','').replace('M','').replace('m',''))-int(zan[0]))):
             zanhou="%s个月"%(int(zan[0])+j)
             mai4.append(zanhou)
      mai4=mai4[(yuanl):]


    if mai4:
      for i in range(0,len(mai4)):

            if ('个月') in mai4[i]:
              mai4[i]= ('%s月'%(nomonth.shift(months=int(mai4[i].replace('个月',''))).month))




    if mai2:
      yuanl=len(mai2)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai2[i]))
          for j in range(1,(int(zan[1].replace('月',''))-int(zan[0]))):
             zanhou="%s月"%(int(zan[0])+j)
             mai2.append(zanhou)
      mai2=mai2[(yuanl):]



    if mai3:
      yuanl=len(mai3)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai3[i]))
          for j in range(1,(int(zan[1].replace('月',''))-int(zan[0].replace('月','')))):
             zanhou="%s月"%(int(zan[0].replace('月',''))+j)
             mai3.append(zanhou)
      mai3=mai3[(yuanl):]

    if mai5:
      for i in range(0,len(mai5)):


            if mai5[i]=='1年':
               mai5[i]= ('%s月'%(nomonth.shift(months=12).month))
            if ('个月') in mai5[i]:
              print(mai5[i])

              mai5[i]= ('%s月'%(nomonth.shift(months=int(mai5[i].replace('个月',''))).month))
            if mai5[i]=='半年':
               mai5[i]= ('%s月'%(nomonth.shift(months=6).month))
    mai=mai2+mai3+mai4+mai5+mai6+mai7+mai8  #形成最终的关键词列表
    lista=Counter(mai).most_common(30)

    qixianm0=pd.DataFrame({'期限': [lista[0][0]],
                    '中介收票':[lista[0][1]]
                  })

    for i in range(1,len(lista)):
      qixianm=pd.DataFrame({'期限': [lista[i][0]],
                    '中介收票':[lista[i][1]]
                  })
      qixianm0= pd.concat([qixianm,qixianm0], axis=0)

    qixian3= qixianm0.reset_index(drop=True)    #重新定义索引
    qixian3=qixian3.set_index(['期限'])

          
    print(qixian3)




#四、银行收票
    mai=[]
    mai2=[]
    mai3=[]
    mai4=[]
    mai5=[]
    mai6=[]
    mai61=[]
    mai7=[]
    mai8=[]

    print('开始银行收票：')
    cursor = collection.find({"$and":[{'time':{'$gte':shijian}},{'hanglei2':1},{'shou':1}]})
    df = pd.DataFrame(list(cursor))

    df = df.sort_values(by='time2', ascending=True)
    df=df.drop_duplicates(['content'],keep='last')   #删除连接中的重复行
    df=df[['content']]

    a=len(df)
    df= df.reset_index(drop=True)    #重新定义索引

    for i in range(0,a):
      cp=df.loc[i,'content'].replace('两','2').replace('十二','12').replace('十一','11').replace('十','10').replace('九','9').replace('八','8').replace('七','7').replace('六','6').replace('五','5').replace('四','4').replace('三','3').replace('二','2').replace('一','1')
      cp=cp.replace('足年','1年')
      zhaop= re.search('^((?!(谁|有人)).)*(?:收|买)(?P<name>([^。,，！…；~？]*?)(?:票|电银|足月|1年|\d月|农商|国股|城商))((?!(买返|买入返售|回购|代持|吗|么|找|联系|？)).)*$',cp)
      if zhaop:
          zhaop2= re.findall('([\d]{1,2}(?:-|至|~|、|，|,)[\d]{1,2}(?:月))',cp)  #如11-12月
          if zhaop2:
              mai2=mai2+zhaop2

          
          zhaop3= re.findall('([\d]{1,2}(?:月)(?:-|至|~)[\d]{1,2}(?:月))',cp)  #如11月-12月
          if zhaop3:
              mai3=mai3+zhaop3
              
              
          zhaop4= re.findall('([\d]{1,2}(?:-|至|~|、|，|,)[\d]{1,2}(?:M|个月|m))',cp)  #如4、5个月
          if zhaop4:
              mai4=mai4+zhaop4

          zhaop5= re.findall('(?:1年|一年|足年|半年)',cp)  #足年或者足月或者3个月,(?:)里面不能再嵌套（？：）
          if zhaop5:
             mai5=mai5+zhaop5


          zhaop51= re.findall('([\d]{1,2}个月)',cp)  #足年或者足月或者3个月
          if zhaop51:
             mai5=mai5+zhaop51


          zhaop6= re.findall('[\d]{1,2}月',cp)  #3月
          if zhaop6:
             mai6=mai6+zhaop6

          zhaop7= re.findall('(?:明年%s月|19年%s月)'%(nomonth.month,nomonth.month),cp)  #明年当月到期
          if zhaop7:
             mai7=mai7+zhaop7

          zhaop8= re.findall('(?:月内|当月|跨月|本月|托收|今年%s月|18年%s月)'%(nomonth.month,nomonth.month),cp)  #当月到期票
          if zhaop8:
             mai8=mai8+zhaop8


    print(mai8)

    if mai6:
      while ('%s月'%nomonth.month) in mai6:
        mai6.remove(('%s月'%nomonth.month))
      for i in range(0,len(mai6)):
       if int(mai6[i].replace('月',''))>12:
           print(int(mai6[i].replace('月','')))
           for j in range(0,len(mai6[i].replace('月',''))):
               print('%s月'%(mai6[i].replace('月','')[j]))
               mai6.append('%s月'%(mai6[i].replace('月','')[j]))
           mai6.remove(mai6[i])

    if mai7:
      for i in range(0,len(mai7)):
         mai7[i]=('%s月'%nomonth.month)

    if mai8:
      for i in range(0,len(mai8)):
         mai8[i]='当月'



    print(mai4)         

    if mai4:
      yuanl=len(mai4)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai4[i]))
          print(zan)
          for j in range(0,(int(zan[1].replace('个月','').replace('M','').replace('m',''))-int(zan[0]))):
             zanhou="%s个月"%(int(zan[0])+j)
             mai4.append(zanhou)
      mai4=mai4[(yuanl):]


    if mai4:
      for i in range(0,len(mai4)):
            if ('个月') in mai4[i]:
              mai4[i]= ('%s月'%(nomonth.shift(months=int(mai4[i].replace('个月',''))).month))



    if mai2:
      yuanl=len(mai2)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai2[i]))
          for j in range(1,(int(zan[1].replace('月',''))-int(zan[0]))):

             try:   #假如错误就跳过。
                 zanhou="%s月"%(int(zan[0])+j)
                 mai2.append(zanhou)
             except ValueError:
                 pass
             continue



                 
      mai2=mai2[(yuanl):]


    if mai3:
      yuanl=len(mai3)
      for i in range(0,yuanl):
          zan=re.split('-|至|~|、|，|,',str(mai3[i]))
          for j in range(1,(int(zan[1].replace('月',''))-int(zan[0].replace('月','')))):   #去掉头尾
             zanhou="%s月"%(int(zan[0].replace('月',''))+j)
             mai3.append(zanhou)
      mai3=mai3[(yuanl):]

    if mai5:
      print(mai5)

      for i in range(0,len(mai5)):
            if mai5[i]=='1年':
               mai5[i]= ('%s月'%(nomonth.shift(months=12).month))
            if ('个月') in mai5[i]:
              mai5[i]= ('%s月'%(nomonth.shift(months=int(mai5[i].replace('个月',''))).month))
            if mai5[i]=='半年':
               mai5[i]= ('%s月'%(nomonth.shift(months=6).month))
    mai=mai2+mai3+mai4+mai5+mai6+mai7+mai8  #形成最终的关键词列表
    lista=Counter(mai).most_common(30)
    print(mai)
    qixianm0=pd.DataFrame({'期限': [lista[0][0]],
                    '银行收票':[lista[0][1]]
                  })

    for i in range(1,len(lista)):
      qixianm=pd.DataFrame({'期限': [lista[i][0]],
                    '银行收票':[lista[i][1]]
                  })
      qixianm0= pd.concat([qixianm,qixianm0], axis=0)

    qixian4= qixianm0.reset_index(drop=True)    #重新定义索引
    qixian4=qixian4.set_index(['期限'])

          
    print(qixian4)



    qixianz= pd.concat([qixian1,qixian2,qixian3,qixian4], axis=1)

    qixianz= qixianz.reset_index(drop=False)    #重新定义索引

    for i in range(0,len(qixianz)):
      if qixianz.loc[i,'index']=='当月':
          qixianz.loc[i,'shun']=-1
      else:
        qixianz.loc[i,'shun']=int(qixianz.loc[i,'index'].replace('月',''))
        if (qixianz.loc[i,'shun']-nomonth.month)<=0:
            qixianz.loc[i,'shun']=qixianz.loc[i,'shun']+12-nomonth.month
        else:
            qixianz.loc[i,'shun']=qixianz.loc[i,'shun']-nomonth.month

    qixianz = qixianz.sort_values(by='shun', ascending=True)
#qixianz= qixianz.reset_index(drop=True)    #重新定义索引

    y3=qixianz['index'].tolist()

    qixianz=qixianz.set_index(['index'])

    qixianz1=qixianz[['中介卖票','中介收票']]

    mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
    qixianz1.plot(kind='bar', alpha=0.5,stacked=False,label='')
    plt.legend(prop=font_set2)  #显示lable位置,loc='upper left'
    plt.xlabel('到期月',fontproperties=font_set)




#plt.ylabel('计划发行(亿)',fontproperties=font_set)
    plt.title('%s中介广告中涉及的到期月'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('images/zhongjieqixian.png')   #images/
    fig.show()



    for i in range(0,len(y3)):
    #print(y1[i])
        if y3[i] in lilvd:
            y3[i]=lilvd.get(y3[i])[0]
     #  print(lilvqu.loc[0,y1[i]])
        else:
            y3[i]=None
    print(y3)
    
    qixianz2=qixianz[['银行卖票','银行收票']]
    mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
    qixianz2.plot(kind='bar', alpha=0.5,stacked=False,label='')
    plt.legend(prop=font_set2)  #显示lable位置,loc='upper left'
    plt.xlabel('到期月',fontproperties=font_set)
    plt2=plt.twinx()
    plt2.plot(y3)
    plt2.set_ylabel('利率(%)',fontproperties=font_set)
    plt.title('%s银行广告中涉及的到期月及票交所收益率曲线'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记

    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('images/yinhangqixian.png')   #images/
    fig.show()
lilvgengxin()
lilvhuatu()
qixianhuatu()
