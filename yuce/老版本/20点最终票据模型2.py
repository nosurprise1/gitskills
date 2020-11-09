# -*- coding: cp936 -*-
import pandas as pd
from bs4 import BeautifulSoup
import urllib,math,numpy
import requests
from pymongo import MongoClient
import cgi
import re,datetime,json,time
from math import  floor
#����try�Ĵ���
from docx import Document
from docx.shared import Pt
from docx.shared import Inches
from docx.oxml.ns import qn
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  
client=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12) #������ɢ��ͼ���������
font_set2 = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=9) #������ɢ��ͼ���������
import matplotlib as mpl   #��ʾ����
from sklearn import metrics
from sklearn import preprocessing, cross_validation, svm
from sklearn.model_selection import train_test_split   #�����������˽�����֤ 
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
    print('��ʼִ������������ɼ۸�Ԥ����򡭡�')
    zhiling=input('    ������ָ�1����ȷ��ִ�У�')
    if zhiling!='1':
       print('    ��ֹ��')
       return
    cursor = collection16.find({'����':'����'})
    guogu_df= pd.DataFrame(list(cursor))
    guogu_df['�۸�����'] = pd.to_datetime(guogu_df['�۸�����']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    guogu_df = guogu_df.sort_values(by='�۸�����', ascending=True)
    guogu_df= guogu_df.reset_index(drop=True)    #���¶�������

    print(guogu_df)
    cursor = collection16.find({'����':'Ԥ��'})
    ygguogu_df= pd.DataFrame(list(cursor))
    ygguogu_df['�۸�����'] = pd.to_datetime(ygguogu_df['�۸�����']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    ygguogu_df = ygguogu_df.sort_values(by='�۸�����', ascending=True)
    ygguogu_df= ygguogu_df.reset_index(drop=True)    #���¶�������

    
    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    import datetime
    shijian = datetime.datetime.strptime(shijian, "%Y-%m-%d")

    jin=input('    �����뵱������,�����ʽΪ��2017-01-01����������Ĭ��Ϊ����:')
    if jin!='':
        shijian0=jin
        shijian=datetime.datetime.strptime(jin , "%Y-%m-%d")

    shijian=str(shijian.strftime("%Y-%m-%d"))
    guoguj=input('    %s���գ��������Ϊ%s��%sԤ�����۸�Ϊ%s��\n    ����������յ�������ɼ۸�'%(guogu_df.loc[(len(guogu_df)-1),'�۸�����'],guogu_df.loc[(len(guogu_df)-1),'�������'],ygguogu_df.loc[(len(ygguogu_df)-1),'�۸�����'],ygguogu_df.loc[(len(ygguogu_df)-1),'�������']))

    if (guoguj!=''):

        collection16.remove({ "$and":[{'�۸�����':str(shijian)},{'����':'����'}] })
        guogu_df=pd.DataFrame({'ͳ������': [shijian],
                   '�������': [guoguj],
                           '����':'����',
                           '�۸�����':[shijian]
                  })
        
        records = json.loads(guogu_df.T.to_json()).values()
        collection16.insert(records)    
        print('    �Ѿ����¡�')

    cursor = collection16.find({'����':'����'})
    guogu_df= pd.DataFrame(list(cursor))
    guogu_df['�۸�����'] = pd.to_datetime(guogu_df['�۸�����']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    guogu_df = guogu_df.sort_values(by='�۸�����', ascending=True)
    guogu_df= guogu_df.reset_index(drop=True)    #���¶�������
    
    model_guogu_df=guogu_df[['�۸�����','�������']]
    model_guogu_df['�۸�����'] = pd.to_datetime(model_guogu_df['�۸�����']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ
    zunian=float(model_guogu_df.loc[(len(model_guogu_df)-1),'�������'])
    zunianshijian=model_guogu_df.loc[(len(model_guogu_df)-1),'�۸�����']    
    model_guogu_df=model_guogu_df.set_index(['�۸�����'])
    model_guogu_df['�������'] = model_guogu_df['�������'].astype('float')     
    print(model_guogu_df)
    



#2.�������

    cursor = collection.find()
    jishi = pd.DataFrame(list(cursor))
    jishi.rename(columns={'��¼����':'ͳ������'}, inplace=True)
    jishi['ͳ������'] = pd.to_datetime(jishi['ͳ������']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    jishi1=jishi[jishi['ҵ����']=='shou']
    jishi1=jishi1.groupby(['ͳ������','ҵ����']).size()
    jishi2=jishi[jishi['ҵ����']=='chu']
    jishi2=jishi2.groupby(['ͳ������','ҵ����']).size()
    jishi1=jishi1.reset_index(drop = False)
    jishi2=jishi2.reset_index(drop = False)
    jishi1=jishi1.set_index(['ͳ������'],drop=True)
    jishi2=jishi2.set_index(['ͳ������'],drop=True)
    jishi= pd.concat([jishi1, jishi2], axis=1)
    jishi['kanchu/kanshou']=jishi.iloc[:,3]/jishi.iloc[:,1]  #�����е�����ȡ��
    jishi['kanshou']=jishi.iloc[:,1]
    jishi['kanchu']=jishi.iloc[:,3]    
    jishi=jishi[['kanshou','kanchu','kanchu/kanshou']]
    jishi=jishi[(jishi['kanshou']>10) & (jishi['kanchu']>10)]    
    
#2.��Ʊ/��Ʊ
    global collection6
    cursor = collection6.find()
    piaofenxi = pd.DataFrame(list(cursor))
    piaofenxi['ͳ������'] = pd.to_datetime(piaofenxi['ͳ������']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    piaofenxi=piaofenxi[piaofenxi['����']!='�н�']
    piaofenxi1=piaofenxi['��Ʊ'].groupby([piaofenxi['ͳ������']]).sum()
    piaofenxi2=piaofenxi['��Ʊ'].groupby([piaofenxi['ͳ������']]).sum()
    piaofenxi2=piaofenxi2.reset_index(drop = False)
    piaofenxi1=piaofenxi1.reset_index(drop = False)
    piaofenxi1=piaofenxi1.set_index('ͳ������')
    piaofenxi2=piaofenxi2.set_index('ͳ������')
    piaofenxi3=pd.concat([piaofenxi1,piaofenxi2], axis=1)
    print(piaofenxi3)


#3.Ʊ����������
    global collection14,collection19
    cursor = collection14.find()
    piaojiaosuo2 = pd.DataFrame(list(cursor))
    piaojiaosuo2['��ȡ����'] = pd.to_datetime(piaojiaosuo2['��ȡ����']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ
    piaojiaosuo2 = piaojiaosuo2.sort_values(by=['��ȡ����'], ascending=True)
    piaojiaosuo2=piaojiaosuo2[piaojiaosuo2['����']=='����']
    piaojiaosuo2=piaojiaosuo2[['��ȡ����','�жҽ��/��Ԫ','���ֽ��/��Ԫ','���׽��/��Ԫ']]
    piaojiaosuo2=piaojiaosuo2.drop_duplicates('��ȡ����', keep='last')  #ɾ���ظ�ֵ
    model_piaojiaosuo_df=piaojiaosuo2.set_index('��ȡ����')
    print(model_piaojiaosuo_df)

#����fen.csv

    cursor2 = collection19.find()
    result0= pd.DataFrame(list(cursor2))
    result0= result0.reset_index(drop=True)    #���¶�������



    result0=result0[result0['���з���']!='������']
    result0= result0.reset_index(drop=True)    #���¶�������

    guogu=['��������','ũ��','����','��ͨ����','�ʴ�����','�й�����']
    gufen=['�������','�㷢����','��������','�ַ�����','ƽ������','��ҵ����','��������','��������','����']
    for i in range(0, len(result0)):

        if (result0.loc[i,'���з���'] in guogu):
            result0.loc[i,'���з���2']='������'

        elif(result0.loc[i,'���з���']in gufen):
            result0.loc[i,'���з���2']='�ɷ���'
        
        elif(result0.loc[i,'���з���']=='����'):
            result0.loc[i,'���з���2']='����'

        elif(result0.loc[i,'���з���']=='ũ����'):
            result0.loc[i,'���з���2']='ũ����'
    result0['shi']=result0['ʵ�ʷ���(��)']*result0['ʵ�ʼ�Ȩ����(%)AAA']
    result0['ji']=result0['�ƻ�����(��)']*result0['�ƻ���Ȩ����(%)AAA']


    result0=result0.groupby(['xz','������','����','���з���2']).sum()  #����һ�����հ׵Ŀ�ʼ�����ֵ0

    result0['ʵ�ʼ�Ȩ����2(%)AAA']=result0['shi']/result0['ʵ�ʷ���(��)']
    result0['�ƻ���Ȩ����2(%)AAA']=result0['ji']/result0['�ƻ�����(��)']


    re11=result0.query('xz==1')
    re11=re11.reset_index(["xz"],drop=True)
    re11=re11[['ʵ�ʷ���(��)','�ƻ�����(��)','ʵ�ʼ�Ȩ����2(%)AAA','�ƻ���Ȩ����2(%)AAA']]

    re22=result0.query('xz==2')
    re22=re22.reset_index(["xz"],drop=True)
    re22=re22[['�ƻ���Ȩ����2(%)AAA','�ƻ�����(��)']]
    re22.rename(columns={'�ƻ�����(��)': 'ԭ�ƻ�����(��)','�ƻ���Ȩ����2(%)AAA':'ԭ�ƻ���Ȩ����2(%)AAA'}, inplace=True) 

    
    result0 = pd.concat([re11, re22], axis=1)
    result0=result0.reset_index(drop=False)

#��ͼ��ʱ���0�滻��NAN
    for i in range(0,len(result0)):
        if result0.loc[i,'ԭ�ƻ���Ȩ����2(%)AAA']==0:
               result0.loc[i,'ԭ�ƻ���Ȩ����2(%)AAA'] =numpy.nan
        if result0.loc[i,'ʵ�ʼ�Ȩ����2(%)AAA']==0:
               result0.loc[i,'ʵ�ʼ�Ȩ����2(%)AAA'] =numpy.nan




  
    model_cundan_df=result0[result0['���з���2']=='�ɷ���']
    model_cundan_df=model_cundan_df[['������','����','ԭ�ƻ���Ȩ����2(%)AAA']]
    model_cundan_df['������'] = pd.to_datetime(model_cundan_df['������']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ
    model_cundan_df=model_cundan_df.set_index(['������'],drop=True)

    cundan1=model_cundan_df[model_cundan_df['����']=='1��']
    cundan2=model_cundan_df[model_cundan_df['����']=='3��']
    cundan3=model_cundan_df[model_cundan_df['����']=='6��']
    cundan4=model_cundan_df[model_cundan_df['����']=='1��']
    model_cundan_df=pd.concat([cundan1,cundan2,cundan3,cundan4], axis=1,join='outer') #Ĭ����outer

    model_cundan_df['1���´浥����']=model_cundan_df.iloc[:,1]
    model_cundan_df['3���´浥����']=model_cundan_df.iloc[:,3]
    model_cundan_df['6���´浥����']=model_cundan_df.iloc[:,5]
    model_cundan_df['1��浥����']=model_cundan_df.iloc[:,7]
    model_cundan_df=model_cundan_df[['1���´浥����','3���´浥����','6���´浥����','1��浥����']]

    print(model_cundan_df)

#��Ѻʽ�ع�
    global model_zhiya_df
    db20=client.zhiyashi
    collection20= db20.zhiyashi
    cursor2 = collection20.find()
    model_zhiya_df= pd.DataFrame(list(cursor2))
    model_zhiya_df=model_zhiya_df[['����','kind','��Ȩ����(%)','��������(%)']]
    model_zhiya_df['����'] = pd.to_datetime(model_zhiya_df['����']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ

    zhiya1=model_zhiya_df[model_zhiya_df['kind']=='R001']
    zhiya1=zhiya1.drop_duplicates('����', keep='last')  #ɾ���ظ�ֵ
    zhiya1=zhiya1.set_index('����')

    zhiya2=model_zhiya_df[model_zhiya_df['kind']=='R007']
    zhiya2=zhiya2.drop_duplicates('����', keep='last')  #ɾ���ظ�ֵ
    zhiya2=zhiya2.set_index('����')
    model_zhiya_df=pd.concat([zhiya1,zhiya2], axis=1,join='outer') #Ĭ����outer

    model_zhiya_df['��ҹ��Ѻ��Ȩ����']=model_zhiya_df.iloc[:,1]
    model_zhiya_df['��ҹ��Ѻ��������']=model_zhiya_df.iloc[:,2]
    model_zhiya_df['7����Ѻ��Ȩ����']=model_zhiya_df.iloc[:,4]
    model_zhiya_df['7����Ѻ��������']=model_zhiya_df.iloc[:,5]
    model_zhiya_df=model_zhiya_df[['��ҹ��Ѻ��Ȩ����','��ҹ��Ѻ��������','7����Ѻ��Ȩ����','7����Ѻ��������']]




#��������ģ��
    print('��ʼʹ��3���´浥����Ʊ/��Ʊģ�͡���')
    df00=pd.concat([model_cundan_df,piaofenxi3,model_zhiya_df,jishi,model_piaojiaosuo_df,model_guogu_df], axis=1,join='outer')
    df00=df00.reset_index(drop = False)
    df00.rename(columns={'index':'����'}, inplace=True)
    df00.to_csv('ģ��ԭʼ����.csv',header=True)

#����Ԥ�����ʾ���

    df001=df00[(len(df00)-1):]
    df001=df001.reset_index(drop = False)
    collection17.remove({'����':df001.loc[0,'����']})
    records = json.loads(df001.T.to_json()).values()
    collection17.insert(records)

    df002=df00[(len(df00)-2):(len(df00)-1)]
    df002=df002.reset_index(drop = False)
    collection17.remove({'����':df002.loc[0,'����']})
    records = json.loads(df002.T.to_json()).values()
    collection17.insert(records)

    df003=df00[(len(df00)-3):(len(df00)-2)]
    df003=df003.reset_index(drop = False)
    collection17.remove({'����':df003.loc[0,'����']})
    records = json.loads(df003.T.to_json()).values()
    collection17.insert(records)
    
    dfm=df00[['����','1���´浥����','3���´浥����','6���´浥����','1��浥����','�������','��Ʊ','��Ʊ']]
    dfm=dfm[dfm['����']>='2018-01-08']
    dfm=dfm.fillna(method='ffill')  #��ȱʧֵǰ����������ȱʧֵ
    dfm=dfm.reset_index(drop = True)
    dfm['��Ʊ/��Ʊ']=dfm['��Ʊ']/dfm['��Ʊ']
    
    for i in range(0,len(dfm)-1):
        if (dfm.loc[i+1,'�������'] !='') and (dfm.loc[i,'�������'] !=''):   #�ڶ����ת�����ʱ䶯���ͽ�����ȵı䶯
             dfm.loc[i,'����������ʱ䶯']=(dfm.loc[i+1,'�������']-dfm.loc[i,'�������'])/dfm.loc[i,'�������']
        if (dfm.loc[i+1,'1���´浥����'] !='') and (dfm.loc[i,'1���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             dfm.loc[i,'1���´浥���ʱ䶯']=(dfm.loc[i+1,'1���´浥����']-dfm.loc[i,'1���´浥����'])/dfm.loc[i,'1���´浥����']
        if (dfm.loc[i+1,'3���´浥����'] !='') and (dfm.loc[i,'3���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             dfm.loc[i,'3���´浥���ʱ䶯']=(dfm.loc[i+1,'3���´浥����']-dfm.loc[i,'3���´浥����'])/dfm.loc[i,'3���´浥����']
        if (dfm.loc[i+1,'6���´浥����'] !='') and (dfm.loc[i,'6���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             dfm.loc[i,'6���´浥���ʱ䶯']=(dfm.loc[i+1,'6���´浥����']-dfm.loc[i,'6���´浥����'])/dfm.loc[i,'6���´浥����']
        if (dfm.loc[i+1,'1��浥����'] !='') and (dfm.loc[i,'1��浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             dfm.loc[i,'1��浥���ʱ䶯']=(dfm.loc[i+1,'1��浥����']-dfm.loc[i,'1��浥����'])/dfm.loc[i,'1��浥����']
         

    dfm=dfm.reset_index(drop = True)
    dfm=dfm.dropna(how='any')
    dfm.to_csv('xiaomoxing.csv',header=True)





#��ͼ
    mpl.rcParams['font.sans-serif'] = ['SimHei']  #������ʾ���ģ���������
    mpl.rcParams['axes.unicode_minus']=False #����������ʾ���ţ������plt��ͼ����mlp����plt
    model_guogu_df2=dfm[['����','1���´浥����','3���´浥����','6���´浥����','1��浥����','�������']]

    model_guogu_df2['����'] = pd.to_datetime(model_guogu_df2['����']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ

    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    model_guogu_df2=model_guogu_df2.set_index(['����'])

    model_guogu_df2.plot(kind='line', alpha=0.8)
    plt.xlabel('')
    plt.ylabel('���ʣ�%��',fontproperties=font_set2)
    plt.title('2018��������ɼ۸����ƣ�%s��'%shijian, fontproperties=font_set2) 
    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��
  
    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('images/guogupiaojia.png')   #images/
    fig.show()




    #2.1����ģ��
    X=dfm.loc[:,('1���´浥���ʱ䶯','3���´浥���ʱ䶯','6���´浥���ʱ䶯','1��浥���ʱ䶯','��Ʊ/��Ʊ')]
    y=dfm.loc[:,'����������ʱ䶯']
    print('�����������')
    print(len(dfm))





    #2.2����ѵ�����Ͳ��Լ�
    X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.01,random_state=1)
    print ('X_train.shape={}\n y_train.shape ={}\n X_test.shape={}\n,  y_test.shape={}'.format(X_train.shape,y_train.shape, X_test.shape,y_test.shape))

    #2.3�ع�ģ��
    linreg = LinearRegression()
    model=linreg.fit(X_train, y_train)
    congidence=linreg.score(X_test, y_test)  #�鿴����ģ�͵�׼ȷ��
    print('���ģ��:')
    print (model)
    print('���׼ȷ�ʣ�')
    print(congidence)
    # ѵ����ģ�ͽؾ�
    print('����ؾࣺ')
    print (linreg.intercept_)
    # ѵ����ģ��Ȩ�أ����������ޱ仯��
    print('���Ȩ�أ�')
    print (linreg.coef_)
    
    print('�������һ������������������Ԥ�⣺')
    print(zunianshijian)
    print(zunian)

    print('�����������Ĵ浥����Ԥ�⣺')
    dfcun=df00[['����','1���´浥����','3���´浥����','6���´浥����','1��浥����']]
    print(dfcun)
    dfcun=dfcun.fillna(method='ffill')  #��ȱʧֵǰ����������ȱʧֵ
    dfcun=dfcun.dropna(how='any')
    dfcun=dfcun.reset_index(drop = True)
    
    xcun1=(dfcun.loc[(len(dfcun)-1),'1���´浥����']-dfcun.loc[(len(dfcun)-2),'1���´浥����'])/dfcun.loc[(len(dfcun)-2),'1���´浥����']
    xcun3=(dfcun.loc[(len(dfcun)-1),'3���´浥����']-dfcun.loc[(len(dfcun)-2),'3���´浥����'])/dfcun.loc[(len(dfcun)-2),'3���´浥����']
    xcun6=(dfcun.loc[(len(dfcun)-1),'6���´浥����']-dfcun.loc[(len(dfcun)-2),'6���´浥����'])/dfcun.loc[(len(dfcun)-2),'6���´浥����']
    xcun12=(dfcun.loc[(len(dfcun)-1),'1��浥����']-dfcun.loc[(len(dfcun)-2),'1��浥����'])/dfcun.loc[(len(dfcun)-2),'1��浥����']


    print('�������ʱ�̵���Ʊ/��ƱԤ�⣺')
    dfshouchu=df00[['����','��Ʊ','��Ʊ']]
    dfshouchu=dfshouchu.dropna(how='any')
    dfshouchu=dfshouchu.reset_index(drop = True)
    dfshouchu['��Ʊ/��Ʊ']=dfshouchu['��Ʊ']/dfshouchu['��Ʊ']
    print(len(dfshouchu))
    print(dfshouchu[(len(dfshouchu)-1):])   #������һ��
    xshouchu=dfshouchu.loc[(len(dfshouchu)-1),'��Ʊ/��Ʊ']

    y_pred = linreg.predict([[xcun1,xcun3,xcun6,xcun12,xshouchu]])
    print('ģ��Ԥ�⣬����������Ƚ���������')
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
    ming=input('    ������Ҫͳ���������ڣ��������ڼ��գ�,�����ʽΪ��2017-11-01���������Զ���Ϊ����:')
    if ming!='':
       shijianm=ming
    print(yzunian) 


    collection16.remove({ "$and":[{'�۸�����':str(shijianm)},{'����':'Ԥ��'}] })
    guogu_df=pd.DataFrame({'ͳ������': [shijian0],
                   '�������': [float(yzunian)],
                           '����':'Ԥ��',
                           '�۸�����':[shijianm]
                  })
    records = json.loads(guogu_df.T.to_json()).values()
    collection16.insert(records)    
    print('    �Ѿ����¡�')






    #��ͼ
    y_pred = linreg.predict(X_test)
    sum_mean=0
    for i in range(len(y_pred)):
        sum_mean+=(y_pred[i]-y_test.values[i])**2
    sum_erro=np.sqrt(sum_mean/20)  #���10������Լ�������
    # calculate RMSE by hand
    print ("RMSE by hand:",sum_erro)
    #��ROC����
   # plt.figure()
   # plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
   # plt.plot(range(len(y_pred)),y_test,'r',label="test")
   # plt.legend(loc="upper right") #��ʾͼ�еı�ǩ
   # plt.xlabel("the number of sales")
   # plt.ylabel('value of sales')
   # plt.show()














#һ���ڵļ۸�����ͼ
def yizhouguogu():
    print('��ʼ14���������ɼ۸����պ�Ԥ����򡭡�')
    zhiling=input('    ������ָ�1����ȷ��ִ�У�')
    if zhiling!='1':
       print('    ��ֹ��')
       return

    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    import datetime
    shijian=datetime.datetime.strptime(shijian , "%Y-%m-%d")#תΪ���ڸ�ʽ
    shijian=str(shijian.strftime("%Y-%m-%d"))

    
    cursor = collection16.find()
    guogu_df= pd.DataFrame(list(cursor))
    guogu_df['�۸�����'] = pd.to_datetime(guogu_df['�۸�����']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    guogu_df = guogu_df.sort_values(by='�۸�����', ascending=True)
    guogu_df=guogu_df.iloc[len(guogu_df)-14:,:]   #ȡ���14��

    print(guogu_df)
    model_guogu_df=guogu_df[['�۸�����','����','�������']]
    model_guogu_df['�۸�����'] = pd.to_datetime(model_guogu_df['�۸�����']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ
    model_guogu_df=model_guogu_df.set_index(['�۸�����'])
    model_guogu_df['�������'] = model_guogu_df['�������'].astype('float')     


    model_guogu_df1=model_guogu_df[model_guogu_df['����']=='����']
    model_guogu_df1.rename(columns={'�������':'����'}, inplace=True)
    model_guogu_df1=model_guogu_df1[['����']]
    print(model_guogu_df1)
    model_guogu_df2=model_guogu_df[model_guogu_df['����']=='Ԥ��']
    model_guogu_df2.rename(columns={'�������':'Ԥ��'}, inplace=True)
    model_guogu_df2=model_guogu_df2[['Ԥ��']]

    print(model_guogu_df2)

    model_guogu_df= pd.concat([model_guogu_df1,model_guogu_df2], axis=1)



    
   #model_guogu_df['Ԥ���ڶ���۸�'] = model_guogu_df['Ԥ���ڶ���۸�'].astype('float') 
    print(model_guogu_df)
    mpl.rcParams['font.sans-serif'] = ['SimHei']  #������ʾ���ģ���������
    mpl.rcParams['axes.unicode_minus']=False #����������ʾ���ţ������plt��ͼ����mlp����plt

    model_guogu_df.plot(kind='line', alpha=0.8)
    plt.xlabel('')
    plt.ylabel('���ʣ�%��',fontproperties=font_set2)
    plt.title('��14��������ɼ۸����ƣ�%s��'%shijian, fontproperties=font_set2) 
    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��

    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('images/guogupiaojia2.png')   #images/

    fig.show()

guogu()
yizhouguogu()
