# -*- coding: cp936 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl   #显示中文
from sklearn import metrics
from sklearn import preprocessing, cross_validation, svm
from sklearn.model_selection import train_test_split   #这里是引用了交叉验证 
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



#一、取数
#1.jishi
def jishi():
    global jishi
    db = client.jishi
    collection = db.jishi
    cursor = collection.find()
    jishi = pd.DataFrame(list(cursor))
    jishi.rename(columns={'登录日期':'统计日期'}, inplace=True)
    jishi['统计日期']=jishi['统计日期'].astype(str)
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


#2.piaofenxi
def piaofenxi():
    global piaofenxi
    db = client.piaofenxi         #得到数据库
    collection = db.piaofenxi      #得到数据集合
    cursor = collection.find()
    piaofenxi = pd.DataFrame(list(cursor))
    piaofenxi['统计日期'] = pd.to_datetime(piaofenxi['统计日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式

    piaofenxi=piaofenxi[piaofenxi['机构']!='中介']
    piaofenxi1=piaofenxi['收票'].groupby([piaofenxi['统计日期']]).sum()
    piaofenxi2=piaofenxi['出票'].groupby([piaofenxi['统计日期']]).sum()
    piaofenxi2=piaofenxi2.reset_index(drop = False)
    piaofenxi1=piaofenxi1.reset_index(drop = False)
    piaofenxi1=piaofenxi1.set_index('统计日期')
    piaofenxi2=piaofenxi2.set_index('统计日期')

    piaofenxi=pd.concat([piaofenxi1,piaofenxi2], axis=1)
    piaofenxi.to_csv('dd5666.csv',header=True)



#3.piaojiaosuo2
def piaojiaosuo2():
    global piaojiaosuo2
    db = client.piaojiaosuo2         #得到数据库
    collection = db.piaojiaosuo2      #得到数据集合
    cursor = collection.find()
    piaojiaosuo2 = pd.DataFrame(list(cursor))
    piaojiaosuo2['提取日期'] = pd.to_datetime(piaojiaosuo2['提取日期']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式

    piaojiaosuo2 = piaojiaosuo2.sort_values(by=['提取日期'], ascending=True)

    piaojiaosuo2=piaojiaosuo2[piaojiaosuo2['数据']=='当日']
    piaojiaosuo2=piaojiaosuo2[['提取日期','承兑金额/亿元','贴现金额/亿元','交易金额/亿元']]
    piaojiaosuo2=piaojiaosuo2.drop_duplicates('提取日期', keep='last')  #删除重复值

    piaojiaosuo2=piaojiaosuo2.set_index('提取日期')



#4.cundan
def cundan():
    global cundan
    url='7/cu/fen.csv'
    cundan=pd.read_table(url, sep=',',encoding='GB18030')
    cundan=cundan[cundan['银行分类2']=='股份行']
    cundan=cundan[['发行日','期限','原计划加权利率2(%)AAA']]
    cundan=cundan.set_index(['发行日'],drop=True)

    cundan1=cundan[cundan['期限']=='1月']
    cundan2=cundan[cundan['期限']=='3月']
    cundan3=cundan[cundan['期限']=='6月']
    cundan4=cundan[cundan['期限']=='1年']
    cundan=pd.concat([cundan1,cundan2,cundan3,cundan4], axis=1,join='outer') #默认是outer
    cundan['1个月存单利率']=cundan.iloc[:,1]
    cundan['3个月存单利率']=cundan.iloc[:,3]
    cundan['6个月存单利率']=cundan.iloc[:,5]
    cundan['1年存单利率']=cundan.iloc[:,7]
    cundan=cundan[['1个月存单利率','3个月存单利率','6个月存单利率','1年存单利率']]


#4.1 同业存单收益率
def cundanshouyi():
    global cundanshou
    url='cundanshou.csv'
    cundanshou=pd.read_table(url, sep=',',encoding='GB18030')
    cundanshou=cundanshou[['日期','收益率(%)','期限描述']]
        #dfm=dfm.reset_index(drop = True)
    cundanshou['日期'] = pd.to_datetime(cundanshou['日期']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式

    cundanshou1=cundanshou[cundanshou['期限描述']=='1M']
    cundanshou1=cundanshou1.drop_duplicates('日期', keep='last')  #删除重复值
    cundanshou1=cundanshou1.set_index(['日期'],drop=True)

    cundanshou2=cundanshou[cundanshou['期限描述']=='3M']
    cundanshou2=cundanshou2.drop_duplicates('日期', keep='last')  #删除重复值
    cundanshou2=cundanshou2.set_index(['日期'],drop=True)

    cundanshou3=cundanshou[cundanshou['期限描述']=='6M']
    cundanshou3=cundanshou3.drop_duplicates('日期', keep='last')  #删除重复值
    cundanshou3=cundanshou3.set_index(['日期'],drop=True)

    cundanshou4=cundanshou[cundanshou['期限描述']=='1Y']
    cundanshou4=cundanshou4.drop_duplicates('日期', keep='last')  #删除重复值
    cundanshou4=cundanshou4.set_index(['日期'],drop=True)

    
    cundanshou=pd.concat([cundanshou1,cundanshou2,cundanshou3,cundanshou4], axis=1,join='outer') #默认是outer
    cundanshou['1个月存单收益率曲线']=cundanshou.iloc[:,0]
    cundanshou['3个月存单收益率曲线']=cundanshou.iloc[:,2]
    cundanshou['6个月存单收益率曲线']=cundanshou.iloc[:,4]
    cundanshou['1年存单收益率曲线']=cundanshou.iloc[:,6]
    cundanshou=cundanshou[['1个月存单收益率曲线','3个月存单收益率曲线','6个月存单收益率曲线','1年存单收益率曲线']]
    print(cundanshou)







#5.zhiya
def zhiya():
    global zhiya
    url='7/zhiya/zhiyamingxi.csv'
    zhiya=pd.read_table(url, sep=',',encoding='GB18030')
    zhiya=zhiya[['date','kind','加权利率(%)','收盘利率(%)']]
    zhiya['date'] = pd.to_datetime(zhiya['date']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式

    zhiya1=zhiya[zhiya['kind']=='R001']
    zhiya1=zhiya1.drop_duplicates('date', keep='last')  #删除重复值
    zhiya1=zhiya1.set_index('date')

    zhiya2=zhiya[zhiya['kind']=='R007']
    zhiya2=zhiya2.drop_duplicates('date', keep='last')  #删除重复值
    zhiya2=zhiya2.set_index('date')
    zhiya=pd.concat([zhiya1,zhiya2], axis=1,join='outer') #默认是outer

    zhiya['隔夜质押加权利率']=zhiya.iloc[:,1]
    zhiya['隔夜质押收盘利率']=zhiya.iloc[:,2]
    zhiya['7天质押加权利率']=zhiya.iloc[:,4]
    zhiya['7天质押收盘利率']=zhiya.iloc[:,5]
    zhiya=zhiya[['隔夜质押加权利率','隔夜质押收盘利率','7天质押加权利率','7天质押收盘利率']]

    
#6.足年国股价格
def guogu():
    global guogu_df

    cursor = collection16.find()
    guogu_df= pd.DataFrame(list(cursor))
    guogu_df['统计日期'] = pd.to_datetime(guogu_df['统计日期']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式 注意要换成string格式
    guogu_df=guogu_df.set_index('统计日期')
  #  print(guogu_df)
    guogu_df['足年国股']=guogu_df['足年国股'].astype(float)

    

#二、构建模型
def moxing():
    print('开始使用3个月存单和收票/出票模型……')
    global df00
    dfm=df00[['日期','1个月存单利率','3个月存单利率','6个月存单利率','1年存单利率','足年国股','收票','出票']]
    dfm=dfm[dfm['日期']>='2018-01-08']

    dfm=dfm.fillna(method='ffill')  #用缺失值前面的数字填充缺失值
    dfm=dfm.reset_index(drop = True)


    dfm['收票/出票']=dfm['收票']/dfm['出票']

 
#    dfm['承兑金额/亿元']=dfm['承兑金额/亿元'].astype(float)
#    dfm['贴现金额/亿元']=dfm['贴现金额/亿元'].astype(float)
 #   dfm['交易金额/亿元']=dfm['交易金额/亿元'].astype(float)

#    dfm['承兑/贴现']=dfm['承兑金额/亿元']/dfm['贴现金额/亿元']
#    dfm['贴现/交易']=dfm['贴现金额/亿元']/dfm['交易金额/亿元']


#    for i in range(2,len(dfm)):
#
 #       if (dfm.loc[i-2,'承兑金额/亿元'] !=''):   
  #           dfm.loc[i,'承兑金额/亿元2']=dfm.loc[i-2,'承兑金额/亿元']
             
   #     if (dfm.loc[i-2,'贴现金额/亿元'] !=''):   
    #         dfm.loc[i,'贴现金额/亿元2']=dfm.loc[i-2,'贴现金额/亿元']
             
     #   if (dfm.loc[i-2,'交易金额/亿元'] !=''):   
      #       dfm.loc[i,'交易金额/亿元2']=dfm.loc[i-2,'交易金额/亿元']
             
      #  if (dfm.loc[i-2,'贴现/交易'] !=''):   
      #       dfm.loc[i,'贴现/交易2']=dfm.loc[i-2,'贴现/交易']
             
      #  if (dfm.loc[i-2,'承兑/贴现'] !=''):   
      #       dfm.loc[i,'承兑/贴现2']=dfm.loc[i-2,'承兑/贴现']   

    
    for i in range(0,len(dfm)-1):
        if (dfm.loc[i+1,'足年国股'] !='') and (dfm.loc[i,'足年国股'] !=''):   #第二天的转贴利率变动，和今天相比的变动
            # dfm.loc[i,'足年国股利率变动']=(dfm.loc[i+1,'足年国股']-dfm.loc[i,'足年国股'])/dfm.loc[i,'足年国股']
             if abs(dfm.loc[i+1,'足年国股']-dfm.loc[i,'足年国股'])<0.05:
                 dfm.loc[i,'足年国股利率变动']=0
             elif (dfm.loc[i+1,'足年国股']-dfm.loc[i,'足年国股'])>=0.05:
                 dfm.loc[i,'足年国股利率变动']=1
             elif (dfm.loc[i+1,'足年国股']-dfm.loc[i,'足年国股'])>=0.05:
                 dfm.loc[i,'足年国股利率变动']=-1

             
        if (dfm.loc[i+1,'1个月存单利率'] !='') and (dfm.loc[i,'1个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
             dfm.loc[i,'1个月存单利率变动']=(dfm.loc[i+1,'1个月存单利率']-dfm.loc[i,'1个月存单利率'])/dfm.loc[i,'1个月存单利率']
        if (dfm.loc[i+1,'3个月存单利率'] !='') and (dfm.loc[i,'3个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
             dfm.loc[i,'3个月存单利率变动']=(dfm.loc[i+1,'3个月存单利率']-dfm.loc[i,'3个月存单利率'])/dfm.loc[i,'3个月存单利率']
        if (dfm.loc[i+1,'6个月存单利率'] !='') and (dfm.loc[i,'6个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
             dfm.loc[i,'6个月存单利率变动']=(dfm.loc[i+1,'6个月存单利率']-dfm.loc[i,'6个月存单利率'])/dfm.loc[i,'6个月存单利率']
        if (dfm.loc[i+1,'1年存单利率'] !='') and (dfm.loc[i,'1年存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
             dfm.loc[i,'1年存单利率变动']=(dfm.loc[i+1,'1年存单利率']-dfm.loc[i,'1年存单利率'])/dfm.loc[i,'1年存单利率']
         

    dfm=dfm.reset_index(drop = True)

    dfm.to_csv('xiaomoxing.csv',header=True)
    dfm=dfm.dropna(how='any')


    #2.1构建模型
    X=dfm.loc[:,('1个月存单利率变动','3个月存单利率变动','6个月存单利率变动','1年存单利率变动','收票/出票')]
    y=dfm.loc[:,'足年国股利率变动']
    print('输出样本量：')

    print(len(dfm))





    #2.2构建训练集和测试集
    X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state=1)
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





    xzunian=df00.loc[(len(df00)-2),'足年国股']
    print('输出今日足年国股：')

    print(xzunian)
    dfcun=df00[['日期','1个月存单利率','3个月存单利率','6个月存单利率','1年存单利率']]
    dfcun=dfcun.dropna(how='any')
    dfcun=dfcun.reset_index(drop = True)

    print(dfcun[(len(dfcun)-2):])
    xcun1=(dfcun.loc[(len(dfcun)-1),'1个月存单利率']-dfcun.loc[(len(dfcun)-2),'1个月存单利率'])/dfcun.loc[(len(dfcun)-2),'1个月存单利率']
    xcun3=(dfcun.loc[(len(dfcun)-1),'3个月存单利率']-dfcun.loc[(len(dfcun)-2),'3个月存单利率'])/dfcun.loc[(len(dfcun)-2),'3个月存单利率']
    xcun6=(dfcun.loc[(len(dfcun)-1),'6个月存单利率']-dfcun.loc[(len(dfcun)-2),'6个月存单利率'])/dfcun.loc[(len(dfcun)-2),'6个月存单利率']
    xcun12=(dfcun.loc[(len(dfcun)-1),'1年存单利率']-dfcun.loc[(len(dfcun)-2),'1年存单利率'])/dfcun.loc[(len(dfcun)-2),'1年存单利率']



    dfshouchu=df00[['日期','收票','出票']]
    dfshouchu=dfshouchu.dropna(how='any')
    dfshouchu=dfshouchu.reset_index(drop = True)
    dfshouchu['收票/出票']=dfshouchu['收票']/dfshouchu['出票']
    print(len(dfshouchu))
    print(dfshouchu[(len(dfshouchu)-1):])
    xshouchu=dfshouchu.loc[(len(dfshouchu)-1),'收票/出票']


#dfpiaojiao=df[['日期','承兑金额/亿元','交易金额/亿元','贴现金额/亿元']]
#dfpiaojiao=dfpiaojiao.dropna(how='any')
#dfpiaojiao=dfpiaojiao.reset_index(drop = True)
#dfpiaojiao['贴现金额/交易金额']=dfpiaojiao['贴现金额/亿元']/dfpiaojiao['交易金额/亿元']
#dfpiaojiao['承兑金额/贴现金额']=dfpiaojiao['承兑金额/亿元']/dfpiaojiao['贴现金额/亿元']
#print(len(dfpiaojiao))
#print(dfpiaojiao[(len(dfpiaojiao)-2):])
#xtie=(dfpiaojiao.loc[(len(dfpiaojiao)-1),'贴现金额/交易金额']-dfpiaojiao.loc[(len(dfpiaojiao)-2),'贴现金额/交易金额'])/dfpiaojiao.loc[(len(dfpiaojiao)-2),'贴现金额/交易金额']
#xcheng=(dfpiaojiao.loc[(len(dfpiaojiao)-1),'承兑金额/贴现金额']-dfpiaojiao.loc[(len(dfpiaojiao)-2),'承兑金额/贴现金额'])/dfpiaojiao.loc[(len(dfpiaojiao)-2),'承兑金额/贴现金额']



    y_pred = linreg.predict([[xcun1,xcun3,xcun6,xcun12,xshouchu]])
    print('模型预测，明天利率相比今天增长：')
    print(y_pred[0]) 
    yzunian=xzunian+y_pred*xzunian

    print(yzunian) 


    #画图
    y_pred = linreg.predict(X_test)
    sum_mean=0
    for i in range(len(y_pred)):
        sum_mean+=(y_pred[i]-y_test.values[i])**2
    sum_erro=np.sqrt(sum_mean/20)  #这个10是你测试级的数量
    # calculate RMSE by hand
    print ("RMSE by hand:",sum_erro)
    #做ROC曲线
    plt.figure()
    plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
    plt.plot(range(len(y_pred)),y_test,'r',label="test")
    plt.legend(loc="upper right") #显示图中的标签
    plt.xlabel("the number of sales")
    plt.ylabel('value of sales')
    plt.show()







def cundanmoxing():
    print('开始使用存单收益率曲线和收票/卖票模型……')
    global df00

    df=df00[['日期','隔夜质押加权利率','7天质押加权利率','1个月存单利率','3个月存单利率','6个月存单利率','1年存单利率','交易金额/亿元','承兑金额/亿元','贴现金额/亿元','足年国股','收票','出票']]
    df=df[df['足年国股'].notnull()]  #把足年国股为空的数值删除

    df=df[df['日期']>='2018-02-05']
    df=df.fillna(method='ffill')  #用缺失值前面的数字填充缺失值
    #df=df.dropna(how='any')
    df=df.reset_index(drop = True)
    df['承兑金额/亿元']=df['承兑金额/亿元'].astype(float)
    df['贴现金额/亿元']=df['贴现金额/亿元'].astype(float)
    df['交易金额/亿元']=df['交易金额/亿元'].astype(float)

    df['收票/出票']=df['收票']/df['出票']
    df['承兑/贴现']=df['承兑金额/亿元']/df['贴现金额/亿元']
    df['贴现/交易']=df['贴现金额/亿元']/df['交易金额/亿元']

    df['7天质押式趋势']=df['7天质押加权利率']-df['隔夜质押加权利率']
    df['1年存单利率趋势']=df['1年存单利率']-df['1个月存单利率']

    for i in range(2,len(df)):
       # if (df.loc[i-1,'收票/出票'] !='') and (df.loc[i,'收票/出票'] !=''):   
        #     df.loc[i,'收票/出票变动']=(df.loc[i,'收票/出票']-df.loc[i-1,'收票/出票'])/df.loc[i-1,'收票/出票']

        if (df.loc[i-2,'承兑金额/亿元'] !=''):   
             df.loc[i,'承兑金额/亿元2']=df.loc[i-2,'承兑金额/亿元']
             
        if (df.loc[i-2,'贴现金额/亿元'] !=''):   
             df.loc[i,'贴现金额/亿元2']=df.loc[i-2,'贴现金额/亿元']
             
        if (df.loc[i-2,'交易金额/亿元'] !=''):   
             df.loc[i,'交易金额/亿元2']=df.loc[i-2,'交易金额/亿元']
             
        if (df.loc[i-2,'贴现/交易'] !=''):   
             df.loc[i,'贴现/交易2']=df.loc[i-2,'贴现/交易']
             
        if (df.loc[i-2,'承兑/贴现'] !=''):   
             df.loc[i,'承兑/贴现2']=df.loc[i-2,'承兑/贴现']             
  #      if (df.loc[i-1,'贴现金额/亿元'] !='') and (df.loc[i,'贴现金额/亿元'] !=''):   
   #          df.loc[i,'贴现金额变动']=(df.loc[i,'贴现金额/亿元']-df.loc[i-1,'贴现金额/亿元'])/df.loc[i-1,'贴现金额/亿元']         

    #    if (df.loc[i-1,'交易金额/亿元'] !='') and (df.loc[i,'交易金额/亿元'] !=''):   
     #        df.loc[i,'交易金额变动']=(df.loc[i,'交易金额/亿元']-df.loc[i-1,'交易金额/亿元'])/df.loc[i-1,'交易金额/亿元']

      #  if (df.loc[i-1,'收票/出票'] !='') and (df.loc[i,'收票/出票'] !=''):   
       #      df.loc[i,'收票/出票变动']=(df.loc[i,'收票/出票']-df.loc[i-1,'收票/出票'])/df.loc[i-1,'收票/出票']


        #if (df.loc[i-1,'承兑/贴现'] !='') and (df.loc[i,'承兑/贴现'] !=''):   
         #    df.loc[i,'承兑/贴现变动']=(df.loc[i,'承兑/贴现']-df.loc[i-1,'承兑/贴现'])/df.loc[i-1,'承兑/贴现']
         
      #  if (df.loc[i-1,'贴现/交易'] !='') and (df.loc[i,'贴现/交易'] !=''):   
       #      df.loc[i,'贴现/交易变动']=(df.loc[i,'贴现/交易']-df.loc[i-1,'贴现/交易'])/df.loc[i-1,'贴现/交易']
                  
        if (df.loc[i-1,'隔夜质押加权利率'] !='') and (df.loc[i,'隔夜质押加权利率'] !=''):   
             df.loc[i,'隔夜质押加权利率变动']=np.log(df.loc[i,'隔夜质押加权利率']/df.loc[i-1,'隔夜质押加权利率'])

        if (df.loc[i-1,'7天质押加权利率'] !='') and (df.loc[i,'7天质押加权利率'] !=''):   
             df.loc[i,'7天质押加权利率变动']=np.log(df.loc[i,'7天质押加权利率']/df.loc[i-1,'7天质押加权利率'])
        if (df.loc[i-1,'收票/出票'] !='') and (df.loc[i,'收票/出票'] !=''):   
             df.loc[i,'收票/出票2']=np.log(df.loc[i,'收票/出票']/df.loc[i-1,'收票/出票'])



  #  for i in range(0,len(df)-1):
   #     if (df.loc[i+1,'足年国股'] !='') and (df.loc[i,'足年国股'] !=''):   #第二天的转贴利率变动，和今天相比的变动
    #         df.loc[i,'足年国股利率变动']=(df.loc[i+1,'足年国股']-df.loc[i,'足年国股'])/df.loc[i,'足年国股']
     #   if (df.loc[i+1,'6个月存单利率'] !='') and (df.loc[i,'6个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
      #       df.loc[i,'6个月存单利率变动']=(df.loc[i+1,'6个月存单利率']-df.loc[i,'6个月存单利率'])/df.loc[i,'6个月存单利率']
       # if (df.loc[i+1,'3个月存单利率'] !='') and (df.loc[i,'3个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
        #     df.loc[i,'3个月存单利率变动']=(df.loc[i+1,'3个月存单利率']-df.loc[i,'3个月存单利率'])/df.loc[i,'3个月存单利率']
  #      if (df.loc[i+1,'1个月存单利率'] !='') and (df.loc[i,'1个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
   #          df.loc[i,'1个月存单利率变动']=(df.loc[i+1,'1个月存单利率']-df.loc[i,'1个月存单利率'])/df.loc[i,'1个月存单利率']
    #    if (df.loc[i+1,'1年存单利率'] !='') and (df.loc[i,'1年存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
     #        df.loc[i,'1年存单利率变动']=(df.loc[i+1,'1年存单利率']-df.loc[i,'1年存单利率'])/df.loc[i,'1年存单利率']
#用对数
    for i in range(0,len(df)-1):
        if (df.loc[i+1,'足年国股'] !='') and (df.loc[i,'足年国股'] !=''):   
             df.loc[i,'足年国股利率变动']=np.log(df.loc[i+1,'足年国股']/df.loc[i,'足年国股'])
        if (df.loc[i+1,'6个月存单利率'] !='') and (df.loc[i,'6个月存单利率'] !=''):      
             df.loc[i,'6个月存单利率变动']=np.log(df.loc[i+1,'6个月存单利率']/df.loc[i,'6个月存单利率'])
        if (df.loc[i+1,'3个月存单利率'] !='') and (df.loc[i,'3个月存单利率'] !=''):       
             df.loc[i,'3个月存单利率变动']=np.log(df.loc[i+1,'3个月存单利率']/df.loc[i,'3个月存单利率'])
        if (df.loc[i+1,'1个月存单利率'] !='') and (df.loc[i,'1个月存单利率'] !=''):        
             df.loc[i,'1个月存单利率变动']=np.log(df.loc[i+1,'1个月存单利率']/df.loc[i,'1个月存单利率'])
        if (df.loc[i+1,'1年存单利率'] !='') and (df.loc[i,'1年存单利率'] !=''):       
             df.loc[i,'1年存单利率变动']=np.log(df.loc[i+1,'1年存单利率']/df.loc[i,'1年存单利率'])
                  
                  


    df=df.reset_index(drop = True)
    df.to_csv('xiaomoxing.csv',header=True)

    df=df.dropna(how='any')




    mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
    mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号，如果是plt画图，则将mlp换成plt
    sns.pairplot(df, x_vars=['隔夜质押加权利率变动','1年存单利率趋势','7天质押加权利率变动','承兑金额/亿元2','贴现金额/亿元2','交易金额/亿元2','承兑/贴现2','贴现/交易2'], y_vars='足年国股利率变动',kind="reg", size=5, aspect=0.7)
    plt.show()  #注意必须加上这一句，否则无法显示。

    sns.pairplot(df, x_vars=['6个月存单利率变动','3个月存单利率变动','1个月存单利率变动','1年存单利率变动','收票/出票'], y_vars='足年国股利率变动',kind="reg", size=5, aspect=0.7)
    plt.show()  #注意必须加上这一句，否则无法显示。



#总模型
    #nsample = 100
    x=df[['6个月存单利率变动','3个月存单利率变动','1个月存单利率变动','1年存单利率变动','承兑金额/亿元2','贴现金额/亿元2','交易金额/亿元2','收票/出票']]
    #x = np.linspace(0, 10, nsample)
    X = sm.add_constant(x)
    beta=np.array([1,10])
    e = np.random.normal(size=len(df))
    #y = np.dot(X, beta) + e
    y=df['足年国股利率变动']
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


#小模型

    #nsample = 100
    x=df[['3个月存单利率变动','1年存单利率变动','贴现金额/亿元2','交易金额/亿元2','收票/出票']]
    #x = np.linspace(0, 10, nsample)
    X = sm.add_constant(x)
    beta=np.array([1,10])
    e = np.random.normal(size=len(df))
    #y = np.dot(X, beta) + e
    y=df['足年国股利率变动']
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
df00.rename(columns={'index':'日期'}, inplace=True)
df00.to_csv('模型原始数据.csv',header=True)
cundanmoxing()

moxing()
