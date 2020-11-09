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

df=df[['����','���ֽ��/��Ԫ','���׽��/��Ԫ','�жҽ��/��Ԫ','3���´浥����','�������','��Ʊ','��Ʊ']]
df=df.dropna(how='any')
df=df.reset_index(drop = True)

for i in range(1,len(df)):
    df.loc[i,'���ֽ��/��Ԫq']=df.loc[i-1,'���ֽ��/��Ԫ']
    df.loc[i,'���׽��/��Ԫq']=df.loc[i-1,'���׽��/��Ԫ']
    df.loc[i,'�жҽ��/��Ԫq']=df.loc[i-1,'�жҽ��/��Ԫ']
df['��Ʊ/��Ʊ']=df['��Ʊ']/df['��Ʊ']



df['���ֽ��/���׽��']=df['���ֽ��/��Ԫq']/df['���׽��/��Ԫq']
df['�жҽ��/���ֽ��']=df['�жҽ��/��Ԫq']/df['���ֽ��/��Ԫq']

print(df)



    
for i in range(0,len(df)-1):
    if (df.loc[i+1,'�������'] !='') and (df.loc[i,'�������'] !=''):   #�ڶ����ת�����ʱ䶯���ͽ�����ȵı䶯
         df.loc[i,'����������ʱ䶯']=(df.loc[i+1,'�������']-df.loc[i,'�������'])/df.loc[i,'�������']
         
    if (df.loc[i+1,'3���´浥����'] !='') and (df.loc[i,'3���´浥����'] !=''):        #�ڶ�������������ʣ��ͽ�����ȵı䶯
         df.loc[i,'3���´浥���ʱ䶯']=(df.loc[i+1,'3���´浥����']-df.loc[i,'3���´浥����'])/df.loc[i,'3���´浥����']
         
for i in range(1,len(df)):                                        #ǰһ������������ʣ���������ȵı䶯
    if (df.loc[i-1,'���ֽ��/���׽��'] !='') and (df.loc[i,'���ֽ��/���׽��'] !=''):  
         df.loc[i,'���ֽ��/���׽��䶯']=(df.loc[i,'���ֽ��/���׽��']-df.loc[i-1,'���ֽ��/���׽��'] )/df.loc[i-1,'���ֽ��/���׽��']

    if (df.loc[i-1,'�жҽ��/���ֽ��'] !='') and (df.loc[i,'�жҽ��/���ֽ��'] !=''):
         df.loc[i,'�жҽ��/���ֽ��䶯']=(df.loc[i,'�жҽ��/���ֽ��']-df.loc[i-1,'�жҽ��/���ֽ��'] )/df.loc[i-1,'�жҽ��/���ֽ��']




#df=df.dropna(how='any')
print(df)


df=df.reset_index(drop = True)

df.to_csv('4yinsu.csv',header=True)



df=df.dropna(how='any')


#df['���ֽ��/���׽��z'] = (df['���ֽ��/���׽��']-df['���ֽ��/���׽��'].mean())/df['���ֽ��/���׽��'].std()    #ת��Ϊ��׼����
#df['�жҽ��/���ֽ��z'] = (df['�жҽ��/���ֽ��']-df['�жҽ��/���ֽ��'].mean())/df['�жҽ��/���ֽ��'].std()    #ת��Ϊ��׼����
#df['3���´浥���ʱ䶯z'] = (df['3���´浥���ʱ䶯']-df['3���´浥���ʱ䶯'].mean())/df['3���´浥���ʱ䶯'].std()    #ת��Ϊ��׼����
#df['��Ʊ/��Ʊz'] = (df['��Ʊ/��Ʊ']-df['��Ʊ/��Ʊ'].mean())/df['��Ʊ/��Ʊ'].std()    #ת��Ϊ��׼����
#df['����������ʱ䶯z'] = (df['����������ʱ䶯']-df['����������ʱ䶯'].mean())/df['����������ʱ䶯'].std()    #ת��Ϊ��׼����




mpl.rcParams['font.sans-serif'] = ['SimHei']  #������ʾ���ģ���������
mpl.rcParams['axes.unicode_minus']=False #����������ʾ���ţ������plt��ͼ����mlp����plt
sns.pairplot(df, x_vars=['3���´浥���ʱ䶯','��Ʊ/��Ʊ','���ֽ��/���׽��','�жҽ��/���ֽ��'], y_vars='����������ʱ䶯',kind="reg", size=5, aspect=0.7)
plt.show()  #ע����������һ�䣬�����޷���ʾ��






#nsample = 100
x=df[['3���´浥���ʱ䶯','��Ʊ/��Ʊ','���ֽ��/���׽��','�жҽ��/���ֽ��']]
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


