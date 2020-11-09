# -*- coding: cp936 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl   #��ʾ����
import json,csv
import pandas as pd
import statsmodels.api as sm
from pymongo import MongoClient
import numpy as np
import seaborn as sns



url='dd.csv'
df = pd.read_table(url,sep=',',encoding='GB18030')   #��dictreader���������ݲ���

df=df[['����','���׽��/��Ԫ','�жҽ��/��Ԫ','���ֽ��/��Ԫ','��Ʊ','��Ʊ','3���´浥����','�������']]
df=df.dropna(how='any')
df=df.reset_index(drop = True)


df['��Ʊ/��Ʊ']=df['��Ʊ']/df['��Ʊ']
df['�ж�/����']=df['�жҽ��/��Ԫ']/df['���ֽ��/��Ԫ']
df['����/����']=df['���ֽ��/��Ԫ']/df['���׽��/��Ԫ']

for i in range(0,len(df)-1):
        if (df.loc[i+1,'�������'] !='') and (df.loc[i,'�������'] !=''):   #�ڶ����ת�����ʱ䶯���ͽ�����ȵı䶯
             df.loc[i,'����������ʱ䶯']=(df.loc[i+1,'�������']-df.loc[i,'�������'])/df.loc[i,'�������']
        if (df.loc[i+1,'3���´浥����'] !='') and (df.loc[i,'3���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
             df.loc[i,'3���´浥���ʱ䶯']=(df.loc[i+1,'3���´浥����']-df.loc[i,'3���´浥����'])/df.loc[i,'3���´浥����']
         
         
    
for i in range(1,len(df)):
 #   if (df.loc[i-1,'�������'] !='') and (df.loc[i,'�������'] !=''):   #�ڶ����ת�����ʱ䶯���ͽ�����ȵı䶯
  #       df.loc[i,'����������ʱ䶯']=(df.loc[i,'�������']-df.loc[i-1,'�������'])/df.loc[i-1,'�������']
         
    if (df.loc[i-1,'�жҽ��/��Ԫ'] !='') and (df.loc[i,'�жҽ��/��Ԫ'] !=''):   
         df.loc[i,'�жҽ��䶯']=(df.loc[i,'�жҽ��/��Ԫ']-df.loc[i-1,'�жҽ��/��Ԫ'])/df.loc[i-1,'�жҽ��/��Ԫ']

    if (df.loc[i-1,'���ֽ��/��Ԫ'] !='') and (df.loc[i,'���ֽ��/��Ԫ'] !=''):   
         df.loc[i,'���ֽ��䶯']=(df.loc[i,'���ֽ��/��Ԫ']-df.loc[i-1,'���ֽ��/��Ԫ'])/df.loc[i-1,'���ֽ��/��Ԫ']         

    if (df.loc[i-1,'���׽��/��Ԫ'] !='') and (df.loc[i,'���׽��/��Ԫ'] !=''):   
         df.loc[i,'���׽��䶯']=(df.loc[i,'���׽��/��Ԫ']-df.loc[i-1,'���׽��/��Ԫ'])/df.loc[i-1,'���׽��/��Ԫ']

    if (df.loc[i-1,'��Ʊ/��Ʊ'] !='') and (df.loc[i,'��Ʊ/��Ʊ'] !=''):   
         df.loc[i,'��Ʊ/��Ʊ�䶯']=(df.loc[i,'��Ʊ/��Ʊ']-df.loc[i-1,'��Ʊ/��Ʊ'])/df.loc[i-1,'��Ʊ/��Ʊ']


    if (df.loc[i-1,'�ж�/����'] !='') and (df.loc[i,'�ж�/����'] !=''):   
         df.loc[i,'�ж�/���ֱ䶯']=(df.loc[i,'�ж�/����']-df.loc[i-1,'�ж�/����'])/df.loc[i-1,'�ж�/����']
         
    if (df.loc[i-1,'����/����'] !='') and (df.loc[i,'����/����'] !=''):   
         df.loc[i,'����/���ױ䶯']=(df.loc[i,'����/����']-df.loc[i-1,'����/����'])/df.loc[i-1,'����/����']
                  
df=df.dropna(how='any')

df=df.reset_index(drop = True)


df['����������ʱ䶯z'] = (df['����������ʱ䶯']-df['����������ʱ䶯'].mean())/df['����������ʱ䶯'].std()    #ת��Ϊ��׼����
df['�жҽ��䶯z'] = (df['�жҽ��䶯']-df['�жҽ��䶯'].mean())/df['�жҽ��䶯'].std()    #ת��Ϊ��׼����
df['���ֽ��䶯z'] = (df['���ֽ��䶯']-df['���ֽ��䶯'].mean())/df['���ֽ��䶯'].std()    #ת��Ϊ��׼����

df['���׽��䶯z'] = (df['���׽��䶯']-df['���׽��䶯'].mean())/df['���׽��䶯'].std()    #ת��Ϊ��׼����
df['��Ʊ/��Ʊ�䶯z'] = (df['��Ʊ/��Ʊ�䶯']-df['��Ʊ/��Ʊ�䶯'].mean())/df['��Ʊ/��Ʊ�䶯'].std()    #ת��Ϊ��׼����
df['�ж�/���ֱ䶯z'] = (df['�ж�/���ֱ䶯']-df['�ж�/���ֱ䶯'].mean())/df['�ж�/���ֱ䶯'].std()    #ת��Ϊ��׼����

df['����/���ױ䶯z'] = (df['����/���ױ䶯']-df['����/���ױ䶯'].mean())/df['����/���ױ䶯'].std()    #ת��Ϊ��׼����
df['����������ʱ䶯z'] = (df['����������ʱ䶯']-df['����������ʱ䶯'].mean())/df['����������ʱ䶯'].std()    #ת��Ϊ��׼����
df['3���´浥���ʱ䶯z'] = (df['3���´浥���ʱ䶯']-df['3���´浥���ʱ䶯'].mean())/df['3���´浥���ʱ䶯'].std()    #ת��Ϊ��׼����

df.to_csv('ffa.csv')


mpl.rcParams['font.sans-serif'] = ['SimHei']  #������ʾ���ģ���������
mpl.rcParams['axes.unicode_minus']=False #����������ʾ���ţ������plt��ͼ����mlp����plt
sns.pairplot(df, x_vars=['�жҽ��䶯z','���ֽ��䶯z','���׽��䶯z','�ж�/���ֱ䶯z','����/���ױ䶯z'], y_vars='����������ʱ䶯z',kind="reg", size=5, aspect=0.7)
plt.show()  #ע����������һ�䣬�����޷���ʾ��






#nsample = 100
x=df[['�жҽ��䶯z','���ֽ��䶯z','���׽��䶯z','�ж�/���ֱ䶯z','����/���ױ䶯z']]
#x = np.linspace(0, 10, nsample)

X = sm.add_constant(x)
beta=np.array([1,10])
e = np.random.normal(size=len(df))
#y = np.dot(X, beta) + e

y=df['����������ʱ䶯z']



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


