# -*- coding: cp936 -*-
import pandas as pd
#from bs4 import BeautifulSoup
import urllib,math,numpy
import requests
#from pymongo import MongoClient
#import cgi
import re,datetime,json,time
#from math import  floor

    

maxTryNum=30
username='18957170906'
password0 ='123'
url0='http://www.51tradecloud.com/'
password = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password.add_password(None,url0,username,password0)
handler=urllib.request.HTTPBasicAuthHandler(password)
opener = urllib.request.build_opener(handler)  
urllib.request.install_opener(opener)


shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
import datetime
shijian=datetime.datetime.strptime(shijian , "%Y-%m-%d")#תΪ���ڸ�ʽ
    #2.1������ȡʱ��
jin=input('    ������Ҫ������,�����ʽΪ��2017-01-01����������Ĭ��Ϊ����:')
if jin!='':
        shijian0=jin
        shijian=datetime.datetime.strptime(jin , "%Y-%m-%d")

shijian=str(shijian.strftime("%Y-%m-%d"))
duifang=input('    �������ļ����������׺.xlsx����')
url=('%s.xlsx'%duifang)
jia_df2=pd.read_excel(url,'����',encoding='GB18030')
jia_df2=jia_df2.dropna(axis=1,how='all')
jia_df2=jia_df2.dropna(axis=0,how='all')

jia_df2= jia_df2.reset_index(drop=True)    #���¶�������
jia_df2['ҵ������']='��ͬ��'


jia_df3=pd.read_excel(url,'���',encoding='GB18030')
jia_df3=jia_df3.dropna(axis=1,how='all')
jia_df3=jia_df3.dropna(axis=0,how='all')

jia_df3= jia_df3.reset_index(drop=True)    #���¶�������
jia_df3['ҵ������']='��ͬ��'



biao= pd.concat([jia_df2,jia_df3], axis=0)

biao=biao[['��ҹ','7D','14D','1M','2M','3M','6M','1Y','����','ҵ������']]
biao= biao.reset_index(drop=True)    #���¶�������
biao=biao.where(biao.notnull(), '')  #��NAN���ɿո�

biao=biao[biao['����'] !='']     
biao = json.loads(biao.T.to_json()).values()
url = url0+'41?maiyin='+urllib.parse.quote(str(biao))+'&shijian='+urllib.parse.quote(str(shijian))

for tries in range(maxTryNum):
            try:
                res_data = urllib.request.urlopen(url,timeout=35)
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    print("    ��������ϲ�޷�����")
                    break

    
res = res_data.read()
huifu=res.decode('utf-8')
print('    ͬҵͨ�����ݸ�����ɡ�')






