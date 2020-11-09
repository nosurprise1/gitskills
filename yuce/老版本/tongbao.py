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
shijian=datetime.datetime.strptime(shijian , "%Y-%m-%d")#转为日期格式
    #2.1输入提取时间
jin=input('    请输入要报价日,输入格式为“2017-01-01”，不输入默认为今天:')
if jin!='':
        shijian0=jin
        shijian=datetime.datetime.strptime(jin , "%Y-%m-%d")

shijian=str(shijian.strftime("%Y-%m-%d"))
duifang=input('    请输入文件名（无需后缀.xlsx）：')
url=('%s.xlsx'%duifang)
jia_df2=pd.read_excel(url,'吸收',encoding='GB18030')
jia_df2=jia_df2.dropna(axis=1,how='all')
jia_df2=jia_df2.dropna(axis=0,how='all')

jia_df2= jia_df2.reset_index(drop=True)    #重新定义索引
jia_df2['业务类型']='收同存'


jia_df3=pd.read_excel(url,'存出',encoding='GB18030')
jia_df3=jia_df3.dropna(axis=1,how='all')
jia_df3=jia_df3.dropna(axis=0,how='all')

jia_df3= jia_df3.reset_index(drop=True)    #重新定义索引
jia_df3['业务类型']='出同存'



biao= pd.concat([jia_df2,jia_df3], axis=0)

biao=biao[['隔夜','7D','14D','1M','2M','3M','6M','1Y','机构','业务类型']]
biao= biao.reset_index(drop=True)    #重新定义索引
biao=biao.where(biao.notnull(), '')  #把NAN换成空格

biao=biao[biao['机构'] !='']     
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
                    print("    您的网络较差，无法连接")
                    break

    
res = res_data.read()
huifu=res.decode('utf-8')
print('    同业通宝数据更新完成。')






