# -*- coding: cp936 -*-
import pandas as pd
from bs4 import BeautifulSoup
import urllib,time
import requests
from pymongo import MongoClient
import cgi
import re,datetime,json
from math import  floor
#����try�Ĵ���
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

client=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')



def pat():
    db = client.chaijie          #�õ����ݿ�
    collection = db.chaijie      
    cursor = collection.find()
    zhiyamingt = pd.DataFrame(list(cursor))
    zhiyamingt['����'] = pd.to_datetime(zhiyamingt['����']).astype('str')  #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ

    shijian0=str(max(zhiyamingt['����'].tolist()))
    #shijian0=''
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}    
    url2="http://www.chinamoney.com.cn/fe/static/html/column/marketdata/dailyexpress/daily/creditlend/creditLendDaily.html"   #
    req = urllib.request.Request(url2,headers = headers)
    menuCode=urllib.request.urlopen(req).read()  # ����ҳԴ���븳��menuCode     
    soup=BeautifulSoup(menuCode,'html.parser')  # ʹ��html���������н���
    trSoup = soup.findAll("table", class_="market-new-text")

    if(trSoup):
        
#������÷����

        foundAllTr1 = trSoup[1].findAll("tr")

        #�õ�����
        biaoti=foundAllTr1[0].findAll("td")
        #�õ����
        mingzi1= foundAllTr1[1].findAll("td")
        #�õ��������
        shijian=foundAllTr1[len(foundAllTr1)-2].find("td")
        shijian=shijian.get_text()
        shijian=shijian.replace('����ʱ�䣺','')
        shijian=shijian[:6]
        shijian=shijian.replace('\xa0','')
        shijian=shijian.replace('\n','')

        shijian='2019-'+shijian

        shijian=shijian.replace(' ','')
        print(shijian)
        print(shijian0)

        if str(shijian0)==str(shijian):
            print('ͬҵ��軹û�и���')
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
                                '����': [shijian],

                         })
            
           # zong1= zong1.reset_index(drop=True)    #���¶�������
            zong1=zong1[['��Ȩ����(%)','����(����)','Ʒ��','����(��Ԫ)','ƽ���������(��)','��������(%)','�ɽ�����(��)','�ɽ����(��Ԫ)','��������(%)','����']]
            zong1.rename(columns={'Ʒ��':'kind'}, inplace=True)

            records = json.loads(zong1.T.to_json()).values()
            collection.insert(records)





def paz():
    db = client.zhiyashi          #�õ����ݿ�
    collection = db.zhiyashi      
    cursor = collection.find()
    zhiyamingz = pd.DataFrame(list(cursor))
    
    zhiyamingz['����'] = pd.to_datetime(zhiyamingz['����']).astype('str')  #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    print(zhiyamingz)
    shijian0=zhiyamingz.loc[(len(zhiyamingz)-1),'����']
   # shijian0=str(max(zhiyamingz['����'].tolist()))
    print(shijian0)

    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}    
    url2="http://www.chinamoney.com.cn/fe/static/html/column/marketdata/dailyexpress/daily/pledgerepo/pledgeRepoDaily.html"
    req = urllib.request.Request(url2,headers = headers)
    menuCode=urllib.request.urlopen(req).read()  # ����ҳԴ���븳��menuCode     
    soup=BeautifulSoup(menuCode,'html.parser')  # ʹ��html���������н���
    trSoup = soup.findAll("table", class_="market-new-text")

    if(trSoup):
        
#������÷����

        foundAllTr1 = trSoup[2].findAll("tr")

        #�õ�����
        biaoti=foundAllTr1[0].findAll("td")
        #�õ����
        mingzi1= foundAllTr1[1].findAll("td")
        #�õ��������
        shijian=foundAllTr1[len(foundAllTr1)-3].find("td")
        shijian=shijian.get_text()
        shijian=shijian.replace('����ʱ�䣺','')
        shijian=shijian[:6]
        shijian=shijian.replace('\xa0','')
        shijian=shijian.replace('\n','')
        shijian='2019-'+shijian
        print(shijian)
        print(shijian0)

        if shijian0==shijian:
            print('��Ѻʽ�ع���û�и���')
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
                                '����': [shijian],

                         })
           # zong1= zong1.reset_index(drop=True)    #���¶�������
            zong1=zong1[['��Ȩ����(%)','��Ȩƽ������(����ծ)(%)','����(����)','Ʒ��','����(��Ԫ)','ƽ���ع�����(��)','��������(%)','�ɽ�����(��)','�ɽ����(��Ԫ)','��������(%)','����']]
            zong1.rename(columns={'Ʒ��':'kind'}, inplace=True)

            records = json.loads(zong1.T.to_json()).values()
            collection.insert(records)








def huatuz():
    db = client.zhiyashi          #�õ����ݿ�
    collection = db.zhiyashi      
    cursor = collection.find()
    result = pd.DataFrame(list(cursor))    
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=13) #������ɢ��ͼ���������
    result=result[(result['kind']=='R001')|(result['kind']=='R007')|(result['kind']=='R014')]
    result['����'] = pd.to_datetime(result['����'])   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    shijian2=time.strftime('%y-%m-%d',time.localtime(time.time()))
    shijian2 = datetime.datetime.strptime(shijian2, "%y-%m-%d")

    shijian3=shijian2-datetime.timedelta(days=30)
    
    shijian3=str(shijian3.strftime("%Y-%m-%d"))

    result=result[result['����']>=str(shijian3)]
 
    result['�ɽ����(��Ԫ)'] = result['�ɽ����(��Ԫ)'].astype('float') 
    result['��Ȩ����(%)'] =result['��Ȩ����(%)'].astype('float')  
   

    result['����'] = pd.to_datetime(result['����']).astype('str')  #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    test5 = result['�ɽ����(��Ԫ)'].groupby([result['����'],result['kind']]).sum().unstack('kind').fillna(0)

    test6= result['��Ȩ����(%)'].groupby([result['����'],result['kind']]).sum().unstack('kind').fillna(0)




    test6=test6.reset_index(drop=False)


    y1=test6['R001'].tolist()
    y2=test6['R007'].tolist()
    y3=test6['R014'].tolist()

    print(y1)
    print(test5)

    test6.plot(kind='bar', alpha=0.4,stacked=True)
    plt.xlabel('')
    plt.ylabel('���������ڣ�',fontproperties=font_set)
    plt.title('��Ѻʽ�ع����ƣ�����Ϊ���ʣ���״ͼΪ�������ѵ���', fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��
    plt2=plt.twinx()
    plt2.plot(y1,alpha=0.7)
    plt2.plot(y2,alpha=0.7)
    plt2.plot(y3,alpha=0.7)

    plt2.set_ylabel('��Ȩ����(%)',fontproperties=font_set)
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
    db = client.chaijie          #�õ����ݿ�
    collection = db.chaijie      
    cursor = collection.find()
    result = pd.DataFrame(list(cursor))
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=13) #������ɢ��ͼ���������

    result=result[(result['kind']=='IBO001')|(result['kind']=='IBO007')|(result['kind']=='IBO014')]
      #    result['����'] = pd.to_datetime(result['����'])   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ

    result['����'] = pd.to_datetime(result['����']).astype('str')  #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    print(result)
    
    zuixins=(max(result['����'].tolist()))

    result=result[result['����']>=str(shijian4)]
    test5 = result['�ɽ����(��Ԫ)'].groupby([result['����'],result['kind']]).sum().unstack('����')
    test5= test5.reset_index(drop=False)    #���¶�������
    
    datenames=test5.columns.values.tolist()[1:]
    yinnames=test5['kind'].tolist()
    testzs=test5.set_index('kind').T.to_dict('list')
    
    test6 = result['��Ȩ����(%)'].groupby([result['����'],result['kind']]).sum().unstack('����')
    test6= test6.reset_index(drop=False)    #���¶�������
    
    datenamels=test6.columns.values.tolist()[1:]
    yinnamels=test6['kind'].tolist()
    testzls=test6.set_index('kind').T.to_dict('list')
    print(datenamels)

paz()
pat()
huatuz()
huatut()
