# -*- coding: cp936 -*-
import pandas as pd
from bs4 import BeautifulSoup
import urllib,time
import requests
from pymongo import MongoClient
import cgi
import re,datetime,json
from math import  floor
#设置try的次数
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

client=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')



def pat():
    db = client.chaijie          #得到数据库
    collection = db.chaijie      
    cursor = collection.find()
    zhiyamingt = pd.DataFrame(list(cursor))
    zhiyamingt['日期'] = pd.to_datetime(zhiyamingt['日期']).astype('str')  #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式

    shijian0=str(max(zhiyamingt['日期'].tolist()))
    #shijian0=''
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}    
    url2="http://www.chinamoney.com.cn/fe/static/html/column/marketdata/dailyexpress/daily/creditlend/creditLendDaily.html"   #
    req = urllib.request.Request(url2,headers = headers)
    menuCode=urllib.request.urlopen(req).read()  # 将网页源代码赋予menuCode     
    soup=BeautifulSoup(menuCode,'html.parser')  # 使用html解析器进行解析
    trSoup = soup.findAll("table", class_="market-new-text")

    if(trSoup):
        
#二、获得分类表

        foundAllTr1 = trSoup[1].findAll("tr")

        #得到标题
        biaoti=foundAllTr1[0].findAll("td")
        #得到表标
        mingzi1= foundAllTr1[1].findAll("td")
        #得到表的内容
        shijian=foundAllTr1[len(foundAllTr1)-2].find("td")
        shijian=shijian.get_text()
        shijian=shijian.replace('更新时间：','')
        shijian=shijian[:6]
        shijian=shijian.replace('\xa0','')
        shijian=shijian.replace('\n','')

        shijian='2019-'+shijian

        shijian=shijian.replace(' ','')
        print(shijian)
        print(shijian0)

        if str(shijian0)==str(shijian):
            print('同业拆借还没有更新')
        else:    
          for i in range(2,len(foundAllTr1)-2):
            Td1=foundAllTr1[i].findAll("td")
           # print(Td1.get_text())
           #print(Td1[9].get_text())
          
            zong1=pd.DataFrame({mingzi1[0].get_text(): [Td1[0].get_text()],
                                mingzi1[1].get_text(): [Td1[1].get_text()],
                                mingzi1[2].get_text(): [Td1[2].get_text()],
                                mingzi1[3].get_text(): [Td1[3].get_text()],
                                mingzi1[4].get_text(): [Td1[4].get_text()],
                                mingzi1[5].get_text(): [Td1[5].get_text()],
                                mingzi1[6].get_text(): [Td1[6].get_text()],
                                mingzi1[7].get_text(): [Td1[7].get_text()],
                                mingzi1[8].get_text(): [Td1[8].get_text()],
                              #  mingzi1[9].get_text(): [Td1[9].get_text()],
                                '日期': [shijian],

                         })
            
           # zong1= zong1.reset_index(drop=True)    #重新定义索引
            zong1=zong1[['加权利率(%)','升降(基点)','品种','增减(亿元)','平均拆借期限(天)','开盘利率(%)','成交笔数(笔)','成交金额(亿元)','收盘利率(%)','日期']]
            zong1.rename(columns={'品种':'kind'}, inplace=True)

            records = json.loads(zong1.T.to_json()).values()
            collection.insert(records)





def paz():
    db = client.zhiyashi          #得到数据库
    collection = db.zhiyashi      
    cursor = collection.find()
    zhiyamingz = pd.DataFrame(list(cursor))
    
    zhiyamingz['日期'] = pd.to_datetime(zhiyamingz['日期']).astype('str')  #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    print(zhiyamingz)
    shijian0=zhiyamingz.loc[(len(zhiyamingz)-1),'日期']
   # shijian0=str(max(zhiyamingz['日期'].tolist()))
    print(shijian0)

    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}    
    url2="http://www.chinamoney.com.cn/fe/static/html/column/marketdata/dailyexpress/daily/pledgerepo/pledgeRepoDaily.html"
    req = urllib.request.Request(url2,headers = headers)
    menuCode=urllib.request.urlopen(req).read()  # 将网页源代码赋予menuCode     
    soup=BeautifulSoup(menuCode,'html.parser')  # 使用html解析器进行解析
    trSoup = soup.findAll("table", class_="market-new-text")

    if(trSoup):
        
#二、获得分类表

        foundAllTr1 = trSoup[2].findAll("tr")

        #得到标题
        biaoti=foundAllTr1[0].findAll("td")
        #得到表标
        mingzi1= foundAllTr1[1].findAll("td")
        #得到表的内容
        shijian=foundAllTr1[len(foundAllTr1)-3].find("td")
        shijian=shijian.get_text()
        shijian=shijian.replace('更新时间：','')
        shijian=shijian[:6]
        shijian=shijian.replace('\xa0','')
        shijian=shijian.replace('\n','')
        shijian='2019-'+shijian
        print(shijian)
        print(shijian0)

        if shijian0==shijian:
            print('质押式回购还没有更新')
        else:    
          for i in range(2,len(foundAllTr1)-3):
            Td1=foundAllTr1[i].findAll("td")
           # print(Td1.get_text())
           #print(Td1[9].get_text())
          
            zong1=pd.DataFrame({mingzi1[0].get_text(): [Td1[0].get_text()],
                                mingzi1[1].get_text(): [Td1[1].get_text()],
                                mingzi1[2].get_text(): [Td1[2].get_text()],
                                mingzi1[3].get_text(): [Td1[3].get_text()],
                                mingzi1[4].get_text(): [Td1[4].get_text()],
                                mingzi1[5].get_text(): [Td1[5].get_text()],
                                mingzi1[6].get_text(): [Td1[6].get_text()],
                                mingzi1[7].get_text(): [Td1[7].get_text()],
                                mingzi1[8].get_text(): [Td1[8].get_text()],
                                mingzi1[9].get_text(): [Td1[9].get_text()],
                                '日期': [shijian],

                         })
           # zong1= zong1.reset_index(drop=True)    #重新定义索引
            zong1=zong1[['加权利率(%)','加权平均利率(利率债)(%)','升降(基点)','品种','增减(亿元)','平均回购期限(天)','开盘利率(%)','成交笔数(笔)','成交金额(亿元)','收盘利率(%)','日期']]
            zong1.rename(columns={'品种':'kind'}, inplace=True)

            records = json.loads(zong1.T.to_json()).values()
            collection.insert(records)








def huatuz():
    db = client.zhiyashi          #得到数据库
    collection = db.zhiyashi      
    cursor = collection.find()
    result = pd.DataFrame(list(cursor))    
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=13) #用于在散点图中输出中文
    result=result[(result['kind']=='R001')|(result['kind']=='R007')|(result['kind']=='R014')]
    result['日期'] = pd.to_datetime(result['日期'])   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    shijian2=time.strftime('%y-%m-%d',time.localtime(time.time()))
    shijian2 = datetime.datetime.strptime(shijian2, "%y-%m-%d")

    shijian3=shijian2-datetime.timedelta(days=30)
    
    shijian3=str(shijian3.strftime("%Y-%m-%d"))

    result=result[result['日期']>=str(shijian3)]
 
    result['成交金额(亿元)'] = result['成交金额(亿元)'].astype('float') 
    result['加权利率(%)'] =result['加权利率(%)'].astype('float')  
   

    result['日期'] = pd.to_datetime(result['日期']).astype('str')  #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    test5 = result['成交金额(亿元)'].groupby([result['日期'],result['kind']]).sum().unstack('kind').fillna(0)

    test6= result['加权利率(%)'].groupby([result['日期'],result['kind']]).sum().unstack('kind').fillna(0)




    test6=test6.reset_index(drop=False)


    y1=test6['R001'].tolist()
    y2=test6['R007'].tolist()
    y3=test6['R014'].tolist()

    print(y1)
    print(test5)

    test6.plot(kind='bar', alpha=0.4,stacked=True)
    plt.xlabel('')
    plt.ylabel('发行量（亿）',fontproperties=font_set)
    plt.title('质押式回购走势（曲线为利率，柱状图为发行量堆叠）', fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt2=plt.twinx()
    plt2.plot(y1,alpha=0.7)
    plt2.plot(y2,alpha=0.7)
    plt2.plot(y3,alpha=0.7)

    plt2.set_ylabel('加权利率(%)',fontproperties=font_set)
    fig =plt.gcf()
    fig.set_size_inches(6, 4)
    fig.savefig('images/zhiya.png')  #C:/Users/yangbing/wangye/wangye/static/images/

    fig.show()

def huatut():

    shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))        #
    shijian2 = datetime.datetime.strptime(shijian2, "%Y-%m-%d")
    shijian3=shijian2-datetime.timedelta(days=3)
    shijian3=str(shijian3.strftime("%Y-%m-%d"))
    shijian4=shijian2-datetime.timedelta(days=29)
    shijian4=str(shijian4.strftime("%Y-%m-%d"))
    shijian2=str(shijian2.strftime("%Y-%m-%d"))    
    db = client.chaijie          #得到数据库
    collection = db.chaijie      
    cursor = collection.find()
    result = pd.DataFrame(list(cursor))
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=13) #用于在散点图中输出中文

    result=result[(result['kind']=='IBO001')|(result['kind']=='IBO007')|(result['kind']=='IBO014')]
      #    result['日期'] = pd.to_datetime(result['日期'])   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式

    result['日期'] = pd.to_datetime(result['日期']).astype('str')  #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    print(result)
    
    zuixins=(max(result['日期'].tolist()))

    result=result[result['日期']>=str(shijian4)]
    test5 = result['成交金额(亿元)'].groupby([result['日期'],result['kind']]).sum().unstack('日期')
    test5= test5.reset_index(drop=False)    #重新定义索引
    
    datenames=test5.columns.values.tolist()[1:]
    yinnames=test5['kind'].tolist()
    testzs=test5.set_index('kind').T.to_dict('list')
    
    test6 = result['加权利率(%)'].groupby([result['日期'],result['kind']]).sum().unstack('日期')
    test6= test6.reset_index(drop=False)    #重新定义索引
    
    datenamels=test6.columns.values.tolist()[1:]
    yinnamels=test6['kind'].tolist()
    testzls=test6.set_index('kind').T.to_dict('list')
    print(datenamels)

paz()
pat()
huatuz()
huatut()
