# -*- coding: cp936 -*-
import pandas as pd
from bs4 import BeautifulSoup
import urllib,math,numpy
import requests
from pymongo import MongoClient
import cgi
import re,datetime,json,time
from math import  floor
#设置try的次数
from docx import Document
from docx.shared import Pt
from docx.shared import Inches
from docx.oxml.ns import qn
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  
client=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12) #用于在散点图中输出中文
font_set2 = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=9) #用于在散点图中输出中文
import matplotlib as mpl   #显示中文
from sklearn import metrics
from sklearn import preprocessing, cross_validation, svm
from sklearn.model_selection import train_test_split   #这里是引用了交叉验证 
from sklearn.linear_model import LinearRegression
import json,csv

import statsmodels.api as sm
import numpy as np
import pandas as pd
db = client.jishi  
collection = db.jishi  

db2 = client.huiguang  
collection2 = db2.huiguang  

db3 = client.huiguangzhu  
collection3 = db3.huiguangzhu  

db4 = client.tongxun  
collection4 = db4.tongxun

db5 = client.piaofen
collection5 = db5.piaofen

db6 = client.piaofenxi
collection6 = db6.piaofenxi

db9 = client.zixun
collection9 = db9.zixun

db10=client.tongxun
collection10 = db10.tongxun

db11=client.cundan
collection11 = db11.cundan

db12=client.xianxia
collection12 = db12.xianxia

db13=client.number
collection13 = db13.number

db14=client.piaojiaosuo2
collection14 = db14.piaojiaosuo2

db15=client.cundanbank
collection15 = db15.cundanbank
    
db16=client.guogu
collection16 = db16.guogu

db17=client.yucebiao
collection17 = db17.yucebiao

db18=client.lilvquxian
collection18 = db18.lilvquxian

db19=client.cundanfenxi
collection19 = db19.cundanfenxi

maxTryNum=26

def guogu():
    global collection
    print('开始执行明天足年国股价格预测程序……')
    zhiling=input('    请输入指令“1”来确认执行：')
    if zhiling!='1':
       print('    终止。')
       return
    cursor = collection16.find({'类型':'日终'})
    guogu_df= pd.DataFrame(list(cursor))
    guogu_df['价格日期'] = pd.to_datetime(guogu_df['价格日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    guogu_df = guogu_df.sort_values(by='价格日期', ascending=True)
    guogu_df= guogu_df.reset_index(drop=True)    #重新定义索引

    print(guogu_df)
    cursor = collection16.find({'类型':'预估'})
    ygguogu_df= pd.DataFrame(list(cursor))
    ygguogu_df['价格日期'] = pd.to_datetime(ygguogu_df['价格日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    ygguogu_df = ygguogu_df.sort_values(by='价格日期', ascending=True)
    ygguogu_df= ygguogu_df.reset_index(drop=True)    #重新定义索引

    
    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    import datetime
    shijian = datetime.datetime.strptime(shijian, "%Y-%m-%d")

    jin=input('    请输入当日日期,输入格式为“2017-01-01”，不输入默认为今天:')
    if jin!='':
        shijian0=jin
        shijian=datetime.datetime.strptime(jin , "%Y-%m-%d")

    shijian=str(shijian.strftime("%Y-%m-%d"))
    guoguj=input('    %s日终，足年国股为%s；%s预估，价格为%s。\n    请输入今日终的足年国股价格：'%(guogu_df.loc[(len(guogu_df)-1),'价格日期'],guogu_df.loc[(len(guogu_df)-1),'足年国股'],ygguogu_df.loc[(len(ygguogu_df)-1),'价格日期'],ygguogu_df.loc[(len(ygguogu_df)-1),'足年国股']))

    if (guoguj!=''):

        collection16.remove({ "$and":[{'价格日期':str(shijian)},{'类型':'日终'}] })
        guogu_df=pd.DataFrame({'统计日期': [shijian],
                   '足年国股': [guoguj],
                           '类型':'日终',
                           '价格日期':[shijian]
                  })
        
        records = json.loads(guogu_df.T.to_json()).values()
        collection16.insert(records)    
        print('    已经更新。')

    cursor = collection16.find({'类型':'日终'})
    guogu_df= pd.DataFrame(list(cursor))
    guogu_df['价格日期'] = pd.to_datetime(guogu_df['价格日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    guogu_df = guogu_df.sort_values(by='价格日期', ascending=True)
    guogu_df= guogu_df.reset_index(drop=True)    #重新定义索引
    
    model_guogu_df=guogu_df[['价格日期','足年国股']]
    model_guogu_df['价格日期'] = pd.to_datetime(model_guogu_df['价格日期']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式
    zunian=float(model_guogu_df.loc[(len(model_guogu_df)-1),'足年国股'])
    zunianshijian=model_guogu_df.loc[(len(model_guogu_df)-1),'价格日期']    
    model_guogu_df=model_guogu_df.set_index(['价格日期'])
    model_guogu_df['足年国股'] = model_guogu_df['足年国股'].astype('float')     
    print(model_guogu_df)
    



#2.点击次数

    cursor = collection.find()
    jishi = pd.DataFrame(list(cursor))
    jishi.rename(columns={'登录日期':'统计日期'}, inplace=True)
    jishi['统计日期'] = pd.to_datetime(jishi['统计日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    jishi1=jishi[jishi['业务方向']=='shou']
    jishi1=jishi1.groupby(['统计日期','业务方向']).size()
    jishi2=jishi[jishi['业务方向']=='chu']
    jishi2=jishi2.groupby(['统计日期','业务方向']).size()
    jishi1=jishi1.reset_index(drop = False)
    jishi2=jishi2.reset_index(drop = False)
    jishi1=jishi1.set_index(['统计日期'],drop=True)
    jishi2=jishi2.set_index(['统计日期'],drop=True)
    jishi= pd.concat([jishi1, jishi2], axis=1)
    jishi['kanchu/kanshou']=jishi.iloc[:,3]/jishi.iloc[:,1]  #根据列的外置取数
    jishi['kanshou']=jishi.iloc[:,1]
    jishi['kanchu']=jishi.iloc[:,3]    
    jishi=jishi[['kanshou','kanchu','kanchu/kanshou']]
    jishi=jishi[(jishi['kanshou']>10) & (jishi['kanchu']>10)]    
    
#2.收票/出票
    global collection6
    cursor = collection6.find()
    piaofenxi = pd.DataFrame(list(cursor))
    piaofenxi['统计日期'] = pd.to_datetime(piaofenxi['统计日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    piaofenxi=piaofenxi[piaofenxi['机构']!='中介']
    piaofenxi1=piaofenxi['收票'].groupby([piaofenxi['统计日期']]).sum()
    piaofenxi2=piaofenxi['出票'].groupby([piaofenxi['统计日期']]).sum()
    piaofenxi2=piaofenxi2.reset_index(drop = False)
    piaofenxi1=piaofenxi1.reset_index(drop = False)
    piaofenxi1=piaofenxi1.set_index('统计日期')
    piaofenxi2=piaofenxi2.set_index('统计日期')
    piaofenxi3=pd.concat([piaofenxi1,piaofenxi2], axis=1)
    print(piaofenxi3)


#3.票交所发行量
    global collection14,collection19
    cursor = collection14.find()
    piaojiaosuo2 = pd.DataFrame(list(cursor))
    piaojiaosuo2['提取日期'] = pd.to_datetime(piaojiaosuo2['提取日期']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式
    piaojiaosuo2 = piaojiaosuo2.sort_values(by=['提取日期'], ascending=True)
    piaojiaosuo2=piaojiaosuo2[piaojiaosuo2['数据']=='当日']
    piaojiaosuo2=piaojiaosuo2[['提取日期','承兑金额/亿元','贴现金额/亿元','交易金额/亿元']]
    piaojiaosuo2=piaojiaosuo2.drop_duplicates('提取日期', keep='last')  #删除重复值
    model_piaojiaosuo_df=piaojiaosuo2.set_index('提取日期')
    print(model_piaojiaosuo_df)

#生成fen.csv

    cursor2 = collection19.find()
    result0= pd.DataFrame(list(cursor2))
    result0= result0.reset_index(drop=True)    #重新定义索引



    result0=result0[result0['银行分类']!='外资行']
    result0= result0.reset_index(drop=True)    #重新定义索引

    guogu=['工商银行','农行','建行','交通银行','邮储银行','中国银行']
    gufen=['光大银行','广发银行','民生银行','浦发银行','平安银行','兴业银行','中信银行','招商银行','华夏']
    for i in range(0, len(result0)):

        if (result0.loc[i,'银行分类'] in guogu):
            result0.loc[i,'银行分类2']='国股行'

        elif(result0.loc[i,'银行分类']in gufen):
            result0.loc[i,'银行分类2']='股份行'
        
        elif(result0.loc[i,'银行分类']=='城商'):
            result0.loc[i,'银行分类2']='城商'

        elif(result0.loc[i,'银行分类']=='农商行'):
            result0.loc[i,'银行分类2']='农商行'
    result0['shi']=result0['实际发行(亿)']*result0['实际加权利率(%)AAA']
    result0['ji']=result0['计划发行(亿)']*result0['计划加权利率(%)AAA']


    result0=result0.groupby(['xz','发行日','期限','银行分类2']).sum()  #在这一步，空白的开始变成数值0

    result0['实际加权利率2(%)AAA']=result0['shi']/result0['实际发行(亿)']
    result0['计划加权利率2(%)AAA']=result0['ji']/result0['计划发行(亿)']


    re11=result0.query('xz==1')
    re11=re11.reset_index(["xz"],drop=True)
    re11=re11[['实际发行(亿)','计划发行(亿)','实际加权利率2(%)AAA','计划加权利率2(%)AAA']]

    re22=result0.query('xz==2')
    re22=re22.reset_index(["xz"],drop=True)
    re22=re22[['计划加权利率2(%)AAA','计划发行(亿)']]
    re22.rename(columns={'计划发行(亿)': '原计划发行(亿)','计划加权利率2(%)AAA':'原计划加权利率2(%)AAA'}, inplace=True) 

    
    result0 = pd.concat([re11, re22], axis=1)
    result0=result0.reset_index(drop=False)

#画图的时候把0替换成NAN
    for i in range(0,len(result0)):
        if result0.loc[i,'原计划加权利率2(%)AAA']==0:
               result0.loc[i,'原计划加权利率2(%)AAA'] =numpy.nan
        if result0.loc[i,'实际加权利率2(%)AAA']==0:
               result0.loc[i,'实际加权利率2(%)AAA'] =numpy.nan




  
    model_cundan_df=result0[result0['银行分类2']=='股份行']
    model_cundan_df=model_cundan_df[['发行日','期限','原计划加权利率2(%)AAA']]
    model_cundan_df['发行日'] = pd.to_datetime(model_cundan_df['发行日']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式
    model_cundan_df=model_cundan_df.set_index(['发行日'],drop=True)

    cundan1=model_cundan_df[model_cundan_df['期限']=='1月']
    cundan2=model_cundan_df[model_cundan_df['期限']=='3月']
    cundan3=model_cundan_df[model_cundan_df['期限']=='6月']
    cundan4=model_cundan_df[model_cundan_df['期限']=='1年']
    model_cundan_df=pd.concat([cundan1,cundan2,cundan3,cundan4], axis=1,join='outer') #默认是outer

    model_cundan_df['1个月存单利率']=model_cundan_df.iloc[:,1]
    model_cundan_df['3个月存单利率']=model_cundan_df.iloc[:,3]
    model_cundan_df['6个月存单利率']=model_cundan_df.iloc[:,5]
    model_cundan_df['1年存单利率']=model_cundan_df.iloc[:,7]
    model_cundan_df=model_cundan_df[['1个月存单利率','3个月存单利率','6个月存单利率','1年存单利率']]

    print(model_cundan_df)

#质押式回购
    global model_zhiya_df
    db20=client.zhiyashi
    collection20= db20.zhiyashi
    cursor2 = collection20.find()
    model_zhiya_df= pd.DataFrame(list(cursor2))
    model_zhiya_df=model_zhiya_df[['日期','kind','加权利率(%)','收盘利率(%)']]
    model_zhiya_df['日期'] = pd.to_datetime(model_zhiya_df['日期']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式

    zhiya1=model_zhiya_df[model_zhiya_df['kind']=='R001']
    zhiya1=zhiya1.drop_duplicates('日期', keep='last')  #删除重复值
    zhiya1=zhiya1.set_index('日期')

    zhiya2=model_zhiya_df[model_zhiya_df['kind']=='R007']
    zhiya2=zhiya2.drop_duplicates('日期', keep='last')  #删除重复值
    zhiya2=zhiya2.set_index('日期')
    model_zhiya_df=pd.concat([zhiya1,zhiya2], axis=1,join='outer') #默认是outer

    model_zhiya_df['隔夜质押加权利率']=model_zhiya_df.iloc[:,1]
    model_zhiya_df['隔夜质押收盘利率']=model_zhiya_df.iloc[:,2]
    model_zhiya_df['7天质押加权利率']=model_zhiya_df.iloc[:,4]
    model_zhiya_df['7天质押收盘利率']=model_zhiya_df.iloc[:,5]
    model_zhiya_df=model_zhiya_df[['隔夜质押加权利率','隔夜质押收盘利率','7天质押加权利率','7天质押收盘利率']]




#二、构建模型
    print('开始使用3个月存单和收票/出票模型……')
    df00=pd.concat([model_cundan_df,piaofenxi3,model_zhiya_df,jishi,model_piaojiaosuo_df,model_guogu_df], axis=1,join='outer')
    df00=df00.reset_index(drop = False)
    df00.rename(columns={'index':'日期'}, inplace=True)
    df00.to_csv('模型原始数据.csv',header=True)

#制作预测的显示表格

    df001=df00[(len(df00)-1):]
    df001=df001.reset_index(drop = False)
    collection17.remove({'日期':df001.loc[0,'日期']})
    records = json.loads(df001.T.to_json()).values()
    collection17.insert(records)

    df002=df00[(len(df00)-2):(len(df00)-1)]
    df002=df002.reset_index(drop = False)
    collection17.remove({'日期':df002.loc[0,'日期']})
    records = json.loads(df002.T.to_json()).values()
    collection17.insert(records)

    df003=df00[(len(df00)-3):(len(df00)-2)]
    df003=df003.reset_index(drop = False)
    collection17.remove({'日期':df003.loc[0,'日期']})
    records = json.loads(df003.T.to_json()).values()
    collection17.insert(records)
    
    dfm=df00[['日期','1个月存单利率','3个月存单利率','6个月存单利率','1年存单利率','足年国股','收票','出票']]
    dfm=dfm[dfm['日期']>='2018-01-08']
    dfm=dfm.fillna(method='ffill')  #用缺失值前面的数字填充缺失值
    dfm=dfm.reset_index(drop = True)
    dfm['收票/出票']=dfm['收票']/dfm['出票']
    
    for i in range(0,len(dfm)-1):
        if (dfm.loc[i+1,'足年国股'] !='') and (dfm.loc[i,'足年国股'] !=''):   #第二天的转贴利率变动，和今天相比的变动
             dfm.loc[i,'足年国股利率变动']=(dfm.loc[i+1,'足年国股']-dfm.loc[i,'足年国股'])/dfm.loc[i,'足年国股']
        if (dfm.loc[i+1,'1个月存单利率'] !='') and (dfm.loc[i,'1个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
             dfm.loc[i,'1个月存单利率变动']=(dfm.loc[i+1,'1个月存单利率']-dfm.loc[i,'1个月存单利率'])/dfm.loc[i,'1个月存单利率']
        if (dfm.loc[i+1,'3个月存单利率'] !='') and (dfm.loc[i,'3个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
             dfm.loc[i,'3个月存单利率变动']=(dfm.loc[i+1,'3个月存单利率']-dfm.loc[i,'3个月存单利率'])/dfm.loc[i,'3个月存单利率']
        if (dfm.loc[i+1,'6个月存单利率'] !='') and (dfm.loc[i,'6个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
             dfm.loc[i,'6个月存单利率变动']=(dfm.loc[i+1,'6个月存单利率']-dfm.loc[i,'6个月存单利率'])/dfm.loc[i,'6个月存单利率']
        if (dfm.loc[i+1,'1年存单利率'] !='') and (dfm.loc[i,'1年存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
             dfm.loc[i,'1年存单利率变动']=(dfm.loc[i+1,'1年存单利率']-dfm.loc[i,'1年存单利率'])/dfm.loc[i,'1年存单利率']
         

    dfm=dfm.reset_index(drop = True)
    dfm=dfm.dropna(how='any')
    dfm.to_csv('xiaomoxing.csv',header=True)





#画图
    mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
    mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号，如果是plt画图，则将mlp换成plt
    model_guogu_df2=dfm[['日期','1个月存单利率','3个月存单利率','6个月存单利率','1年存单利率','足年国股']]

    model_guogu_df2['日期'] = pd.to_datetime(model_guogu_df2['日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式

    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    model_guogu_df2=model_guogu_df2.set_index(['日期'])

    model_guogu_df2.plot(kind='line', alpha=0.8)
    plt.xlabel('')
    plt.ylabel('利率（%）',fontproperties=font_set2)
    plt.title('2018年足年国股价格走势（%s）'%shijian, fontproperties=font_set2) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
  
    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('images/guogupiaojia.png')   #images/
    fig.show()




    #2.1构建模型
    X=dfm.loc[:,('1个月存单利率变动','3个月存单利率变动','6个月存单利率变动','1年存单利率变动','收票/出票')]
    y=dfm.loc[:,'足年国股利率变动']
    print('输出样本量：')
    print(len(dfm))





    #2.2构建训练集和测试集
    X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.01,random_state=1)
    print ('X_train.shape={}\n y_train.shape ={}\n X_test.shape={}\n,  y_test.shape={}'.format(X_train.shape,y_train.shape, X_test.shape,y_test.shape))

    #2.3回归模型
    linreg = LinearRegression()
    model=linreg.fit(X_train, y_train)
    congidence=linreg.score(X_test, y_test)  #查看测试模型的准确率
    print('输出模型:')
    print (model)
    print('输出准确率：')
    print(congidence)
    # 训练后模型截距
    print('输出截距：')
    print (linreg.intercept_)
    # 训练后模型权重（特征个数无变化）
    print('输出权重：')
    print (linreg.coef_)
    
    print('根据最后一天的足年国股日终利率预测：')
    print(zunianshijian)
    print(zunian)

    print('根据最后两天的存单利率预测：')
    dfcun=df00[['日期','1个月存单利率','3个月存单利率','6个月存单利率','1年存单利率']]
    print(dfcun)
    dfcun=dfcun.fillna(method='ffill')  #用缺失值前面的数字填充缺失值
    dfcun=dfcun.dropna(how='any')
    dfcun=dfcun.reset_index(drop = True)
    
    xcun1=(dfcun.loc[(len(dfcun)-1),'1个月存单利率']-dfcun.loc[(len(dfcun)-2),'1个月存单利率'])/dfcun.loc[(len(dfcun)-2),'1个月存单利率']
    xcun3=(dfcun.loc[(len(dfcun)-1),'3个月存单利率']-dfcun.loc[(len(dfcun)-2),'3个月存单利率'])/dfcun.loc[(len(dfcun)-2),'3个月存单利率']
    xcun6=(dfcun.loc[(len(dfcun)-1),'6个月存单利率']-dfcun.loc[(len(dfcun)-2),'6个月存单利率'])/dfcun.loc[(len(dfcun)-2),'6个月存单利率']
    xcun12=(dfcun.loc[(len(dfcun)-1),'1年存单利率']-dfcun.loc[(len(dfcun)-2),'1年存单利率'])/dfcun.loc[(len(dfcun)-2),'1年存单利率']


    print('根据最后时刻的收票/出票预测：')
    dfshouchu=df00[['日期','收票','出票']]
    dfshouchu=dfshouchu.dropna(how='any')
    dfshouchu=dfshouchu.reset_index(drop = True)
    dfshouchu['收票/出票']=dfshouchu['收票']/dfshouchu['出票']
    print(len(dfshouchu))
    print(dfshouchu[(len(dfshouchu)-1):])   #输出最后一行
    xshouchu=dfshouchu.loc[(len(dfshouchu)-1),'收票/出票']

    y_pred = linreg.predict([[xcun1,xcun3,xcun6,xcun12,xshouchu]])
    print('模型预测，明天利率相比今天增长：')
    print(y_pred) 
    print(float(y_pred)) 

    print(y_pred[0])
    print(float(y_pred[0]))
    yzunian=zunian+float(y_pred[0])*zunian
    shijian0=time.strftime('%Y-%m-%d',time.localtime(time.time()))

    import datetime
    shijian = datetime.datetime.strptime(shijian, "%Y-%m-%d")
    shijian0 = datetime.datetime.strptime(shijian0, "%Y-%m-%d")

    shijianm=shijian+datetime.timedelta(days=1)
    shijian0=str(shijian0.strftime("%Y-%m-%d"))
    shijianm=str(shijianm.strftime("%Y-%m-%d"))
    ming=input('    请输入要统计下期日期（请跳过节假日）,输入格式为“2017-11-01”不输入自定义为明天:')
    if ming!='':
       shijianm=ming
    print(yzunian) 


    collection16.remove({ "$and":[{'价格日期':str(shijianm)},{'类型':'预估'}] })
    guogu_df=pd.DataFrame({'统计日期': [shijian0],
                   '足年国股': [float(yzunian)],
                           '类型':'预估',
                           '价格日期':[shijianm]
                  })
    records = json.loads(guogu_df.T.to_json()).values()
    collection16.insert(records)    
    print('    已经更新。')






    #画图
    y_pred = linreg.predict(X_test)
    sum_mean=0
    for i in range(len(y_pred)):
        sum_mean+=(y_pred[i]-y_test.values[i])**2
    sum_erro=np.sqrt(sum_mean/20)  #这个10是你测试级的数量
    # calculate RMSE by hand
    print ("RMSE by hand:",sum_erro)
    #做ROC曲线
   # plt.figure()
   # plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
   # plt.plot(range(len(y_pred)),y_test,'r',label="test")
   # plt.legend(loc="upper right") #显示图中的标签
   # plt.xlabel("the number of sales")
   # plt.ylabel('value of sales')
   # plt.show()














#一周内的价格走势图
def yizhouguogu():
    print('开始14天的足年国股价格日终和预测程序……')
    zhiling=input('    请输入指令“1”来确认执行：')
    if zhiling!='1':
       print('    终止。')
       return

    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    import datetime
    shijian=datetime.datetime.strptime(shijian , "%Y-%m-%d")#转为日期格式
    shijian=str(shijian.strftime("%Y-%m-%d"))

    
    cursor = collection16.find()
    guogu_df= pd.DataFrame(list(cursor))
    guogu_df['价格日期'] = pd.to_datetime(guogu_df['价格日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    guogu_df = guogu_df.sort_values(by='价格日期', ascending=True)
    guogu_df=guogu_df.iloc[len(guogu_df)-14:,:]   #取最后14行

    print(guogu_df)
    model_guogu_df=guogu_df[['价格日期','类型','足年国股']]
    model_guogu_df['价格日期'] = pd.to_datetime(model_guogu_df['价格日期']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式
    model_guogu_df=model_guogu_df.set_index(['价格日期'])
    model_guogu_df['足年国股'] = model_guogu_df['足年国股'].astype('float')     


    model_guogu_df1=model_guogu_df[model_guogu_df['类型']=='日终']
    model_guogu_df1.rename(columns={'足年国股':'日终'}, inplace=True)
    model_guogu_df1=model_guogu_df1[['日终']]
    print(model_guogu_df1)
    model_guogu_df2=model_guogu_df[model_guogu_df['类型']=='预估']
    model_guogu_df2.rename(columns={'足年国股':'预估'}, inplace=True)
    model_guogu_df2=model_guogu_df2[['预估']]

    print(model_guogu_df2)

    model_guogu_df= pd.concat([model_guogu_df1,model_guogu_df2], axis=1)



    
   #model_guogu_df['预估第二天价格'] = model_guogu_df['预估第二天价格'].astype('float') 
    print(model_guogu_df)
    mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
    mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号，如果是plt画图，则将mlp换成plt

    model_guogu_df.plot(kind='line', alpha=0.8)
    plt.xlabel('')
    plt.ylabel('利率（%）',fontproperties=font_set2)
    plt.title('近14天足年国股价格走势（%s）'%shijian, fontproperties=font_set2) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记

    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('images/guogupiaojia2.png')   #images/

    fig.show()

guogu()
yizhouguogu()
