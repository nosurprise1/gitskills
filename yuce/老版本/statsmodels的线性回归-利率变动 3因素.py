# -*- coding: cp936 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl   #显示中文
import json,csv
import pandas as pd
import statsmodels.api as sm
from pymongo import MongoClient
import numpy as np
import seaborn as sns



url='dd.csv'
df = pd.read_table(url,sep=',',encoding='GB18030')   #用dictreader根据行内容查找

df=df[['日期','3个月存单利率','6个月存单利率','足年国股','收票','出票']]
df=df.dropna(how='any')
df=df.reset_index(drop = True)


df['收票/出票']=df['收票']/df['出票']




    
for i in range(0,len(df)-1):
    if (df.loc[i+1,'足年国股'] !='') and (df.loc[i,'足年国股'] !=''):   #第二天的转贴利率变动，和今天相比的变动
         df.loc[i,'足年国股利率变动']=(df.loc[i+1,'足年国股']-df.loc[i,'足年国股'])/df.loc[i,'足年国股']
         
    if (df.loc[i+1,'3个月存单利率'] !='') and (df.loc[i,'3个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
         df.loc[i,'3个月存单利率变动']=(df.loc[i+1,'3个月存单利率']-df.loc[i,'3个月存单利率'])/df.loc[i,'3个月存单利率']

    if (df.loc[i+1,'6个月存单利率'] !='') and (df.loc[i,'6个月存单利率'] !=''):        #第二天的利率增长率，和今天相比的变动
         df.loc[i,'6个月存单利率变动']=(df.loc[i+1,'6个月存单利率']-df.loc[i,'6个月存单利率'])/df.loc[i,'6个月存单利率']
                  

df=df.reset_index(drop = True)

df.to_csv('3yinsu.csv',header=True)



df=df.dropna(how='any')




mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号，如果是plt画图，则将mlp换成plt
sns.pairplot(df, x_vars=['3个月存单利率变动','6个月存单利率变动','收票/出票'], y_vars='足年国股利率变动',kind="reg", size=5, aspect=0.7)
plt.show()  #注意必须加上这一句，否则无法显示。






#nsample = 100
x=df[['3个月存单利率变动','6个月存单利率变动','收票/出票']]
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


