# -*- coding: cp936 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl   #��ʾ����
from sklearn import metrics
from sklearn import preprocessing, cross_validation, svm
from sklearn.model_selection import train_test_split   #�����������˽�����֤ 
from sklearn.linear_model import LinearRegression
import json,csv
import pandas as pd
import statsmodels.api as sm
from pymongo import MongoClient
#client = MongoClient()
client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')
import numpy as np
import seaborn as sns
db16=client.guogu
collection16 = db16.guogu



#һ��ȡ��
#1.jishi
def jishi():
    global jishi
    db = client.jishi
    collection = db.jishi
    cursor = collection.find()
    jishi = pd.DataFrame(list(cursor))
    jishi.rename(columns={'��¼����':'ͳ������'}, inplace=True)
    jishi['ͳ������']=jishi['ͳ������'].astype(str)
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


#2.piaofenxi
def piaofenxi():
    global piaofenxi
    db = client.piaofenxi         #�õ����ݿ�
    collection = db.piaofenxi      #�õ����ݼ���
    cursor = collection.find()
    piaofenxi = pd.DataFrame(list(cursor))
    piaofenxi['ͳ������'] = pd.to_datetime(piaofenxi['ͳ������']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ

    piaofenxi=piaofenxi[piaofenxi['����']!='�н�']
    piaofenxi1=piaofenxi['��Ʊ'].groupby([piaofenxi['ͳ������']]).sum()
    piaofenxi2=piaofenxi['��Ʊ'].groupby([piaofenxi['ͳ������']]).sum()
    piaofenxi2=piaofenxi2.reset_index(drop = False)
    piaofenxi1=piaofenxi1.reset_index(drop = False)
    piaofenxi1=piaofenxi1.set_index('ͳ������')
    piaofenxi2=piaofenxi2.set_index('ͳ������')

    piaofenxi=pd.concat([piaofenxi1,piaofenxi2], axis=1)
    piaofenxi.to_csv('dd5666.csv',header=True)



#3.piaojiaosuo2
def piaojiaosuo2():
    global piaojiaosuo2
    db = client.piaojiaosuo2         #�õ����ݿ�
    collection = db.piaojiaosuo2      #�õ����ݼ���
    cursor = collection.find()
    piaojiaosuo2 = pd.DataFrame(list(cursor))
    piaojiaosuo2['��ȡ����'] = pd.to_datetime(piaojiaosuo2['��ȡ����']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ

    piaojiaosuo2 = piaojiaosuo2.sort_values(by=['��ȡ����'], ascending=True)

    piaojiaosuo2=piaojiaosuo2[piaojiaosuo2['����']=='����']
    piaojiaosuo2=piaojiaosuo2[['��ȡ����','�жҽ��/��Ԫ','���ֽ��/��Ԫ','���׽��/��Ԫ']]
    piaojiaosuo2=piaojiaosuo2.drop_duplicates('��ȡ����', keep='last')  #ɾ���ظ�ֵ

    piaojiaosuo2=piaojiaosuo2.set_index('��ȡ����')



#4.cundan
def cundan():
    global cundan
    url='7/cu/fen.csv'
    cundan=pd.read_table(url, sep=',',encoding='GB18030')
    cundan=cundan[cundan['���з���2']=='�ɷ���']
    cundan=cundan[['������','����','ԭ�ƻ���Ȩ����2(%)AAA']]
    cundan=cundan.set_index(['������'],drop=True)

    cundan1=cundan[cundan['����']=='1��']
    cundan2=cundan[cundan['����']=='3��']
    cundan3=cundan[cundan['����']=='6��']
    cundan4=cundan[cundan['����']=='1��']
    cundan=pd.concat([cundan1,cundan2,cundan3,cundan4], axis=1,join='outer') #Ĭ����outer
    cundan['1���´浥����']=cundan.iloc[:,1]
    cundan['3���´浥����']=cundan.iloc[:,3]
    cundan['6���´浥����']=cundan.iloc[:,5]
    cundan['1��浥����']=cundan.iloc[:,7]
    cundan=cundan[['1���´浥����','3���´浥����','6���´浥����','1��浥����']]


#4.1 ͬҵ�浥������
def cundanshouyi():
    global cundanshou
    url='cundanshou.csv'
    cundanshou=pd.read_table(url, sep=',',encoding='GB18030')
    cundanshou=cundanshou[['����','������(%)','��������']]
        #dfm=dfm.reset_index(drop = True)
    cundanshou['����'] = pd.to_datetime(cundanshou['����']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ

    cundanshou1=cundanshou[cundanshou['��������']=='1M']
    cundanshou1=cundanshou1.drop_duplicates('����', keep='last')  #ɾ���ظ�ֵ
    cundanshou1=cundanshou1.set_index(['����'],drop=True)

    cundanshou2=cundanshou[cundanshou['��������']=='3M']
    cundanshou2=cundanshou2.drop_duplicates('����', keep='last')  #ɾ���ظ�ֵ
    cundanshou2=cundanshou2.set_index(['����'],drop=True)

    cundanshou3=cundanshou[cundanshou['��������']=='6M']
    cundanshou3=cundanshou3.drop_duplicates('����', keep='last')  #ɾ���ظ�ֵ
    cundanshou3=cundanshou3.set_index(['����'],drop=True)

    cundanshou4=cundanshou[cundanshou['��������']=='1Y']
    cundanshou4=cundanshou4.drop_duplicates('����', keep='last')  #ɾ���ظ�ֵ
    cundanshou4=cundanshou4.set_index(['����'],drop=True)

    
    cundanshou=pd.concat([cundanshou1,cundanshou2,cundanshou3,cundanshou4], axis=1,join='outer') #Ĭ����outer
    cundanshou['1���´浥����������']=cundanshou.iloc[:,0]
    cundanshou['3���´浥����������']=cundanshou.iloc[:,2]
    cundanshou['6���´浥����������']=cundanshou.iloc[:,4]
    cundanshou['1��浥����������']=cundanshou.iloc[:,6]
    cundanshou=cundanshou[['1���´浥����������','3���´浥����������','6���´浥����������','1��浥����������']]
    print(cundanshou)







#5.zhiya
def zhiya():
    global zhiya
    url='7/zhiya/zhiyamingxi.csv'
    zhiya=pd.read_table(url, sep=',',encoding='GB18030')
    zhiya=zhiya[['date','kind','��Ȩ����(%)','��������(%)']]
    zhiya['date'] = pd.to_datetime(zhiya['date']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ

    zhiya1=zhiya[zhiya['kind']=='R001']
    zhiya1=zhiya1.drop_duplicates('date', keep='last')  #ɾ���ظ�ֵ
    zhiya1=zhiya1.set_index('date')

    zhiya2=zhiya[zhiya['kind']=='R007']
    zhiya2=zhiya2.drop_duplicates('date', keep='last')  #ɾ���ظ�ֵ
    zhiya2=zhiya2.set_index('date')
    zhiya=pd.concat([zhiya1,zhiya2], axis=1,join='outer') #Ĭ����outer

    zhiya['��ҹ��Ѻ��Ȩ����']=zhiya.iloc[:,1]
    zhiya['��ҹ��Ѻ��������']=zhiya.iloc[:,2]
    zhiya['7����Ѻ��Ȩ����']=zhiya.iloc[:,4]
    zhiya['7����Ѻ��������']=zhiya.iloc[:,5]
    zhiya=zhiya[['��ҹ��Ѻ��Ȩ����','��ҹ��Ѻ��������','7����Ѻ��Ȩ����','7����Ѻ��������']]

    
#6.������ɼ۸�
def guogu():
    global guogu_df

    cursor = collection16.find()
    guogu_df= pd.DataFrame(list(cursor))
    guogu_df['ͳ������'] = pd.to_datetime(guogu_df['ͳ������']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ ע��Ҫ����string��ʽ
    guogu_df=guogu_df.set_index('ͳ������')
  #  print(guogu_df)
    guogu_df['�������']=guogu_df['�������'].astype(float)

    

#��������ģ��
def moxing():
    print('��ʼʹ��3���´浥����Ʊ/��Ʊģ�͡���')
    global df00
    dfm=df00[['����','1���´浥����','3���´浥����','6���´浥����','1��浥����','�������','��Ʊ','��Ʊ']]
    dfm=dfm[dfm['����']>='2018-01-08']

    dfm=dfm.fillna(method='ffill')  #��ȱʧֵǰ����������ȱʧֵ
    dfm=dfm.reset_index(drop = True)


    dfm['��Ʊ/��Ʊ']=dfm['��Ʊ']/dfm['��Ʊ']

 
#    dfm['�жҽ��/��Ԫ']=dfm['�жҽ��/��Ԫ'].astype(float)
#    dfm['���ֽ��/��Ԫ']=dfm['���ֽ��/��Ԫ'].astype(float)
 #   dfm['���׽��/��Ԫ']=dfm['���׽��/��Ԫ'].astype(float)

#    dfm['�ж�/����']=dfm['�жҽ��/��Ԫ']/dfm['���ֽ��/��Ԫ']
#    dfm['����/����']=dfm['���ֽ��/��Ԫ']/dfm['���׽��/��Ԫ']


#    for i in range(2,len(dfm)):
#
 #       if (dfm.loc[i-2,'�жҽ��/��Ԫ'] !=''):   
  #           dfm.loc[i,'�жҽ��/��Ԫ2']=dfm.loc[i-2,'�жҽ��/��Ԫ']
             
   #     if (dfm.loc[i-2,'���ֽ��/��Ԫ'] !=''):   
    #         dfm.loc[i,'���ֽ��/��Ԫ2']=dfm.loc[i-2,'���ֽ��/��Ԫ']
             
     #   if (dfm.loc[i-2,'���׽��/��Ԫ'] !=''):   
      #       dfm.loc[i,'���׽��/��Ԫ2']=dfm.loc[i-2,'���׽��/��Ԫ']
             
      #  if (dfm.loc[i-2,'����/����'] !=''):   
      #       dfm.loc[i,'����/����2']=dfm.loc[i-2,'����/����']
             
      #  if (dfm.loc[i-2,'�ж�/����'] !=''):   
      #       dfm.loc[i,'�ж�/����2']=dfm.loc[i-2,'�ж�/����']   

    
    for i in range(0,len(dfm)-1):
        if (dfm.loc[i+1,'�������'] !='') and (dfm.loc[i,'�������'] !=''):   #�ڶ����ת�����ʱ䶯���ͽ�����ȵı䶯
            # dfm.loc[i,'����������ʱ䶯']=(dfm.loc[i+1,'�������']-dfm.loc[i,'�������'])/dfm.loc[i,'�������']
             if abs(dfm.loc[i+1,'�������']-dfm.loc[i,'�������'])<0.05:
                 dfm.loc[i,'����������ʱ䶯']=0
             elif (dfm.loc[i+1,'�������']-dfm.loc[i,'�������'])>=0.05:
                 dfm.loc[i,'����������ʱ䶯']=1
             elif (dfm.loc[i+1,'�������']-dfm.loc[i,'�������'])>=0.05:
                 dfm.loc[i,'����������ʱ䶯']=-1

             
        if (dfm.loc[i+1,'1���´浥����'] !='') and (dfm.loc[i,'1���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             dfm.loc[i,'1���´浥���ʱ䶯']=(dfm.loc[i+1,'1���´浥����']-dfm.loc[i,'1���´浥����'])/dfm.loc[i,'1���´浥����']
        if (dfm.loc[i+1,'3���´浥����'] !='') and (dfm.loc[i,'3���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             dfm.loc[i,'3���´浥���ʱ䶯']=(dfm.loc[i+1,'3���´浥����']-dfm.loc[i,'3���´浥����'])/dfm.loc[i,'3���´浥����']
        if (dfm.loc[i+1,'6���´浥����'] !='') and (dfm.loc[i,'6���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             dfm.loc[i,'6���´浥���ʱ䶯']=(dfm.loc[i+1,'6���´浥����']-dfm.loc[i,'6���´浥����'])/dfm.loc[i,'6���´浥����']
        if (dfm.loc[i+1,'1��浥����'] !='') and (dfm.loc[i,'1��浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             dfm.loc[i,'1��浥���ʱ䶯']=(dfm.loc[i+1,'1��浥����']-dfm.loc[i,'1��浥����'])/dfm.loc[i,'1��浥����']
         

    dfm=dfm.reset_index(drop = True)

    dfm.to_csv('xiaomoxing.csv',header=True)
    dfm=dfm.dropna(how='any')


    #2.1����ģ��
    X=dfm.loc[:,('1���´浥���ʱ䶯','3���´浥���ʱ䶯','6���´浥���ʱ䶯','1��浥���ʱ䶯','��Ʊ/��Ʊ')]
    y=dfm.loc[:,'����������ʱ䶯']
    print('�����������')

    print(len(dfm))





    #2.2����ѵ�����Ͳ��Լ�
    X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state=1)
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





    xzunian=df00.loc[(len(df00)-2),'�������']
    print('�������������ɣ�')

    print(xzunian)
    dfcun=df00[['����','1���´浥����','3���´浥����','6���´浥����','1��浥����']]
    dfcun=dfcun.dropna(how='any')
    dfcun=dfcun.reset_index(drop = True)

    print(dfcun[(len(dfcun)-2):])
    xcun1=(dfcun.loc[(len(dfcun)-1),'1���´浥����']-dfcun.loc[(len(dfcun)-2),'1���´浥����'])/dfcun.loc[(len(dfcun)-2),'1���´浥����']
    xcun3=(dfcun.loc[(len(dfcun)-1),'3���´浥����']-dfcun.loc[(len(dfcun)-2),'3���´浥����'])/dfcun.loc[(len(dfcun)-2),'3���´浥����']
    xcun6=(dfcun.loc[(len(dfcun)-1),'6���´浥����']-dfcun.loc[(len(dfcun)-2),'6���´浥����'])/dfcun.loc[(len(dfcun)-2),'6���´浥����']
    xcun12=(dfcun.loc[(len(dfcun)-1),'1��浥����']-dfcun.loc[(len(dfcun)-2),'1��浥����'])/dfcun.loc[(len(dfcun)-2),'1��浥����']



    dfshouchu=df00[['����','��Ʊ','��Ʊ']]
    dfshouchu=dfshouchu.dropna(how='any')
    dfshouchu=dfshouchu.reset_index(drop = True)
    dfshouchu['��Ʊ/��Ʊ']=dfshouchu['��Ʊ']/dfshouchu['��Ʊ']
    print(len(dfshouchu))
    print(dfshouchu[(len(dfshouchu)-1):])
    xshouchu=dfshouchu.loc[(len(dfshouchu)-1),'��Ʊ/��Ʊ']


#dfpiaojiao=df[['����','�жҽ��/��Ԫ','���׽��/��Ԫ','���ֽ��/��Ԫ']]
#dfpiaojiao=dfpiaojiao.dropna(how='any')
#dfpiaojiao=dfpiaojiao.reset_index(drop = True)
#dfpiaojiao['���ֽ��/���׽��']=dfpiaojiao['���ֽ��/��Ԫ']/dfpiaojiao['���׽��/��Ԫ']
#dfpiaojiao['�жҽ��/���ֽ��']=dfpiaojiao['�жҽ��/��Ԫ']/dfpiaojiao['���ֽ��/��Ԫ']
#print(len(dfpiaojiao))
#print(dfpiaojiao[(len(dfpiaojiao)-2):])
#xtie=(dfpiaojiao.loc[(len(dfpiaojiao)-1),'���ֽ��/���׽��']-dfpiaojiao.loc[(len(dfpiaojiao)-2),'���ֽ��/���׽��'])/dfpiaojiao.loc[(len(dfpiaojiao)-2),'���ֽ��/���׽��']
#xcheng=(dfpiaojiao.loc[(len(dfpiaojiao)-1),'�жҽ��/���ֽ��']-dfpiaojiao.loc[(len(dfpiaojiao)-2),'�жҽ��/���ֽ��'])/dfpiaojiao.loc[(len(dfpiaojiao)-2),'�жҽ��/���ֽ��']



    y_pred = linreg.predict([[xcun1,xcun3,xcun6,xcun12,xshouchu]])
    print('ģ��Ԥ�⣬����������Ƚ���������')
    print(y_pred[0]) 
    yzunian=xzunian+y_pred*xzunian

    print(yzunian) 


    #��ͼ
    y_pred = linreg.predict(X_test)
    sum_mean=0
    for i in range(len(y_pred)):
        sum_mean+=(y_pred[i]-y_test.values[i])**2
    sum_erro=np.sqrt(sum_mean/20)  #���10������Լ�������
    # calculate RMSE by hand
    print ("RMSE by hand:",sum_erro)
    #��ROC����
    plt.figure()
    plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
    plt.plot(range(len(y_pred)),y_test,'r',label="test")
    plt.legend(loc="upper right") #��ʾͼ�еı�ǩ
    plt.xlabel("the number of sales")
    plt.ylabel('value of sales')
    plt.show()







def cundanmoxing():
    print('��ʼʹ�ô浥���������ߺ���Ʊ/��Ʊģ�͡���')
    global df00

    df=df00[['����','��ҹ��Ѻ��Ȩ����','7����Ѻ��Ȩ����','1���´浥����','3���´浥����','6���´浥����','1��浥����','���׽��/��Ԫ','�жҽ��/��Ԫ','���ֽ��/��Ԫ','�������','��Ʊ','��Ʊ']]
    df=df[df['�������'].notnull()]  #���������Ϊ�յ���ֵɾ��

    df=df[df['����']>='2018-02-05']
    df=df.fillna(method='ffill')  #��ȱʧֵǰ����������ȱʧֵ
    #df=df.dropna(how='any')
    df=df.reset_index(drop = True)
    df['�жҽ��/��Ԫ']=df['�жҽ��/��Ԫ'].astype(float)
    df['���ֽ��/��Ԫ']=df['���ֽ��/��Ԫ'].astype(float)
    df['���׽��/��Ԫ']=df['���׽��/��Ԫ'].astype(float)

    df['��Ʊ/��Ʊ']=df['��Ʊ']/df['��Ʊ']
    df['�ж�/����']=df['�жҽ��/��Ԫ']/df['���ֽ��/��Ԫ']
    df['����/����']=df['���ֽ��/��Ԫ']/df['���׽��/��Ԫ']

    df['7����Ѻʽ����']=df['7����Ѻ��Ȩ����']-df['��ҹ��Ѻ��Ȩ����']
    df['1��浥��������']=df['1��浥����']-df['1���´浥����']

    for i in range(2,len(df)):
       # if (df.loc[i-1,'��Ʊ/��Ʊ'] !='') and (df.loc[i,'��Ʊ/��Ʊ'] !=''):   
        #     df.loc[i,'��Ʊ/��Ʊ�䶯']=(df.loc[i,'��Ʊ/��Ʊ']-df.loc[i-1,'��Ʊ/��Ʊ'])/df.loc[i-1,'��Ʊ/��Ʊ']

        if (df.loc[i-2,'�жҽ��/��Ԫ'] !=''):   
             df.loc[i,'�жҽ��/��Ԫ2']=df.loc[i-2,'�жҽ��/��Ԫ']
             
        if (df.loc[i-2,'���ֽ��/��Ԫ'] !=''):   
             df.loc[i,'���ֽ��/��Ԫ2']=df.loc[i-2,'���ֽ��/��Ԫ']
             
        if (df.loc[i-2,'���׽��/��Ԫ'] !=''):   
             df.loc[i,'���׽��/��Ԫ2']=df.loc[i-2,'���׽��/��Ԫ']
             
        if (df.loc[i-2,'����/����'] !=''):   
             df.loc[i,'����/����2']=df.loc[i-2,'����/����']
             
        if (df.loc[i-2,'�ж�/����'] !=''):   
             df.loc[i,'�ж�/����2']=df.loc[i-2,'�ж�/����']             
  #      if (df.loc[i-1,'���ֽ��/��Ԫ'] !='') and (df.loc[i,'���ֽ��/��Ԫ'] !=''):   
   #          df.loc[i,'���ֽ��䶯']=(df.loc[i,'���ֽ��/��Ԫ']-df.loc[i-1,'���ֽ��/��Ԫ'])/df.loc[i-1,'���ֽ��/��Ԫ']         

    #    if (df.loc[i-1,'���׽��/��Ԫ'] !='') and (df.loc[i,'���׽��/��Ԫ'] !=''):   
     #        df.loc[i,'���׽��䶯']=(df.loc[i,'���׽��/��Ԫ']-df.loc[i-1,'���׽��/��Ԫ'])/df.loc[i-1,'���׽��/��Ԫ']

      #  if (df.loc[i-1,'��Ʊ/��Ʊ'] !='') and (df.loc[i,'��Ʊ/��Ʊ'] !=''):   
       #      df.loc[i,'��Ʊ/��Ʊ�䶯']=(df.loc[i,'��Ʊ/��Ʊ']-df.loc[i-1,'��Ʊ/��Ʊ'])/df.loc[i-1,'��Ʊ/��Ʊ']


        #if (df.loc[i-1,'�ж�/����'] !='') and (df.loc[i,'�ж�/����'] !=''):   
         #    df.loc[i,'�ж�/���ֱ䶯']=(df.loc[i,'�ж�/����']-df.loc[i-1,'�ж�/����'])/df.loc[i-1,'�ж�/����']
         
      #  if (df.loc[i-1,'����/����'] !='') and (df.loc[i,'����/����'] !=''):   
       #      df.loc[i,'����/���ױ䶯']=(df.loc[i,'����/����']-df.loc[i-1,'����/����'])/df.loc[i-1,'����/����']
                  
        if (df.loc[i-1,'��ҹ��Ѻ��Ȩ����'] !='') and (df.loc[i,'��ҹ��Ѻ��Ȩ����'] !=''):   
             df.loc[i,'��ҹ��Ѻ��Ȩ���ʱ䶯']=np.log(df.loc[i,'��ҹ��Ѻ��Ȩ����']/df.loc[i-1,'��ҹ��Ѻ��Ȩ����'])

        if (df.loc[i-1,'7����Ѻ��Ȩ����'] !='') and (df.loc[i,'7����Ѻ��Ȩ����'] !=''):   
             df.loc[i,'7����Ѻ��Ȩ���ʱ䶯']=np.log(df.loc[i,'7����Ѻ��Ȩ����']/df.loc[i-1,'7����Ѻ��Ȩ����'])
        if (df.loc[i-1,'��Ʊ/��Ʊ'] !='') and (df.loc[i,'��Ʊ/��Ʊ'] !=''):   
             df.loc[i,'��Ʊ/��Ʊ2']=np.log(df.loc[i,'��Ʊ/��Ʊ']/df.loc[i-1,'��Ʊ/��Ʊ'])



  #  for i in range(0,len(df)-1):
   #     if (df.loc[i+1,'�������'] !='') and (df.loc[i,'�������'] !=''):   #�ڶ����ת�����ʱ䶯���ͽ�����ȵı䶯
    #         df.loc[i,'����������ʱ䶯']=(df.loc[i+1,'�������']-df.loc[i,'�������'])/df.loc[i,'�������']
     #   if (df.loc[i+1,'6���´浥����'] !='') and (df.loc[i,'6���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
      #       df.loc[i,'6���´浥���ʱ䶯']=(df.loc[i+1,'6���´浥����']-df.loc[i,'6���´浥����'])/df.loc[i,'6���´浥����']
       # if (df.loc[i+1,'3���´浥����'] !='') and (df.loc[i,'3���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
        #     df.loc[i,'3���´浥���ʱ䶯']=(df.loc[i+1,'3���´浥����']-df.loc[i,'3���´浥����'])/df.loc[i,'3���´浥����']
  #      if (df.loc[i+1,'1���´浥����'] !='') and (df.loc[i,'1���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
   #          df.loc[i,'1���´浥���ʱ䶯']=(df.loc[i+1,'1���´浥����']-df.loc[i,'1���´浥����'])/df.loc[i,'1���´浥����']
    #    if (df.loc[i+1,'1��浥����'] !='') and (df.loc[i,'1��浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
     #        df.loc[i,'1��浥���ʱ䶯']=(df.loc[i+1,'1��浥����']-df.loc[i,'1��浥����'])/df.loc[i,'1��浥����']
#�ö���
    for i in range(0,len(df)-1):
        if (df.loc[i+1,'�������'] !='') and (df.loc[i,'�������'] !=''):   
             df.loc[i,'����������ʱ䶯']=np.log(df.loc[i+1,'�������']/df.loc[i,'�������'])
        if (df.loc[i+1,'6���´浥����'] !='') and (df.loc[i,'6���´浥����'] !=''):      
             df.loc[i,'6���´浥���ʱ䶯']=np.log(df.loc[i+1,'6���´浥����']/df.loc[i,'6���´浥����'])
        if (df.loc[i+1,'3���´浥����'] !='') and (df.loc[i,'3���´浥����'] !=''):       
             df.loc[i,'3���´浥���ʱ䶯']=np.log(df.loc[i+1,'3���´浥����']/df.loc[i,'3���´浥����'])
        if (df.loc[i+1,'1���´浥����'] !='') and (df.loc[i,'1���´浥����'] !=''):        
             df.loc[i,'1���´浥���ʱ䶯']=np.log(df.loc[i+1,'1���´浥����']/df.loc[i,'1���´浥����'])
        if (df.loc[i+1,'1��浥����'] !='') and (df.loc[i,'1��浥����'] !=''):       
             df.loc[i,'1��浥���ʱ䶯']=np.log(df.loc[i+1,'1��浥����']/df.loc[i,'1��浥����'])
                  
                  


    df=df.reset_index(drop = True)
    df.to_csv('xiaomoxing.csv',header=True)

    df=df.dropna(how='any')




    mpl.rcParams['font.sans-serif'] = ['SimHei']  #������ʾ���ģ���������
    mpl.rcParams['axes.unicode_minus']=False #����������ʾ���ţ������plt��ͼ����mlp����plt
    sns.pairplot(df, x_vars=['��ҹ��Ѻ��Ȩ���ʱ䶯','1��浥��������','7����Ѻ��Ȩ���ʱ䶯','�жҽ��/��Ԫ2','���ֽ��/��Ԫ2','���׽��/��Ԫ2','�ж�/����2','����/����2'], y_vars='����������ʱ䶯',kind="reg", size=5, aspect=0.7)
    plt.show()  #ע����������һ�䣬�����޷���ʾ��

    sns.pairplot(df, x_vars=['6���´浥���ʱ䶯','3���´浥���ʱ䶯','1���´浥���ʱ䶯','1��浥���ʱ䶯','��Ʊ/��Ʊ'], y_vars='����������ʱ䶯',kind="reg", size=5, aspect=0.7)
    plt.show()  #ע����������һ�䣬�����޷���ʾ��



#��ģ��
    #nsample = 100
    x=df[['6���´浥���ʱ䶯','3���´浥���ʱ䶯','1���´浥���ʱ䶯','1��浥���ʱ䶯','�жҽ��/��Ԫ2','���ֽ��/��Ԫ2','���׽��/��Ԫ2','��Ʊ/��Ʊ']]
    #x = np.linspace(0, 10, nsample)
    X = sm.add_constant(x)
    beta=np.array([1,10])
    e = np.random.normal(size=len(df))
    #y = np.dot(X, beta) + e
    y=df['����������ʱ䶯']
    model=sm.OLS(y,X.astype(float))
    model1=model.fit()
    print(model1.params)
    print(model1.summary())

    y_fitted = model1.fittedvalues
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(x, y, 'o', label='data')
    ax.plot(x, y_fitted, 'r--.',label='OLS')
    ax.legend(loc='best')
    fig.show()


#Сģ��

    #nsample = 100
    x=df[['3���´浥���ʱ䶯','1��浥���ʱ䶯','���ֽ��/��Ԫ2','���׽��/��Ԫ2','��Ʊ/��Ʊ']]
    #x = np.linspace(0, 10, nsample)
    X = sm.add_constant(x)
    beta=np.array([1,10])
    e = np.random.normal(size=len(df))
    #y = np.dot(X, beta) + e
    y=df['����������ʱ䶯']
    model=sm.OLS(y,X.astype(float))
    model1=model.fit()
    print(model1.params)
    print(model1.summary())

    y_fitted = model1.fittedvalues
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(x, y, 'o', label='data')
    ax.plot(x, y_fitted, 'r--.',label='OLS')
    ax.legend(loc='best')
    fig.show()














cundanshouyi()
cundan()
guogu()

zhiya()
piaojiaosuo2()
jishi()    
piaofenxi()
df00=pd.concat([cundan,piaofenxi,zhiya,jishi,piaojiaosuo2,guogu_df], axis=1,join='outer')
#df.fillna(value=-99999, inplace=True)
df00=df00.reset_index(drop = False)
df00.rename(columns={'index':'����'}, inplace=True)
df00.to_csv('ģ��ԭʼ����.csv',header=True)
cundanmoxing()

moxing()
