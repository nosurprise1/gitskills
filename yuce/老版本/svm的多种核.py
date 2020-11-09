# -*- coding: cp936 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame,Series
import matplotlib as mpl   #��ʾ����
from sklearn import metrics
from sklearn import preprocessing, cross_validation, svm
from sklearn.model_selection import train_test_split   #�����������˽�����֤ 
from sklearn.linear_model import LinearRegression
import numpy as np
import  math
from sklearn import preprocessing, cross_validation, svm



#һ����ȡ���ݣ����ұ�׼��
url='zong.csv'
df = pd.read_table(url,sep=',',encoding='GB18030')   #��dictreader���������ݲ���
df=df[['3����ͬҵ�浥����','3���º�һ��','��һ������','��Ʊ/��Ʊ','�������']]
df=df.dropna(axis=0,how='any')
df['��һ��������']=(df['��һ������']-df['�������'])/df['�������']
df['3���º�һ��������']=(df['3���º�һ��']-df['3����ͬҵ�浥����'])/df['3����ͬҵ�浥����']


#df['��һ��������z'] = (df['��һ��������']-df['��һ��������'].mean())/df['��һ��������'].std()    #ת��Ϊ��׼����
df['�������z'] = (df['�������']-df['�������'].mean())/df['�������'].std()    #ת��Ϊ��׼����
#df['��Ѻʽ�ع�7��z'] = (df['��Ѻʽ�ع�7��']-df['��Ѻʽ�ع�7��'].mean())/df['��Ѻʽ�ع�7��'].std()    #ת��Ϊ��׼����
#df['��ҹ���z'] = (df['��ҹ���']-df['��ҹ���'].mean())/df['��ҹ���'].std()    #ת��Ϊ��׼����
df['3���º�һ��������z'] = (df['3���º�һ��������']-df['3���º�һ��������'].mean())/df['3���º�һ��������'].std()    #ת��Ϊ��׼����
#df['������/�ɽ����z'] = (df['������/�ɽ����']-df['������/�ɽ����'].mean())/df['������/�ɽ����'].std()    #ת��Ϊ��׼����
df['��Ʊ/��Ʊz'] = (df['��Ʊ/��Ʊ']-df['��Ʊ/��Ʊ'].mean())/df['��Ʊ/��Ʊ'].std()    #ת��Ϊ��׼����
print(df)


#������ɢ��ͼ
sns.pairplot(df, x_vars=['3���º�һ��������z','��Ʊ/��Ʊz','�������z'], y_vars='��һ��������',kind="reg", size=5, aspect=0.7)
mpl.rcParams['font.sans-serif'] = ['SimHei']  #������ʾ���ģ���������
mpl.rcParams['axes.unicode_minus']=False #����������ʾ���ţ������plt��ͼ����mlp����plt
plt.show()#ע����������һ�䣬�����޷���ʾ��



#��������ģ��

X=df.loc[:,('3���º�һ��������z','��Ʊ/��Ʊz','�������z')]
y=df.loc[:,'��һ��������']
print(len(df))










#�ġ�����ѵ�����Ͳ��Լ�
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state=1)
print ('X_train.shape={}\n y_train.shape ={}\n X_test.shape={}\n,  y_test.shape={}'.format(X_train.shape,y_train.shape, X_test.shape,y_test.shape))

#4.1�ع�ģ��
linreg = LinearRegression()
model=linreg.fit(X_train, y_train)
congidence=linreg.score(X_test, y_test)  #�鿴����ģ�͵�׼ȷ��
print (model)
print(congidence)
    # ѵ����ģ�ͽؾ�
print (linreg.intercept_)
    # ѵ����ģ��Ȩ�أ����������ޱ仯��
print (linreg.coef_)

#4.2 ������ģ��
#2.2.1�����Ǹ�ģ�������
#for k in ['linear','poly','rbf','sigmoid']:
 #   clf = svm.SVR(kernel=k)
  #  clf.fit(X_train, y_train)
   # confidence = clf.score(X_test, y_test)
    #print(k,confidence)

#2.2.2ֱ�Ӽ�������ϵ�ģ����ֵ
#clf = svm.SVR()
#clf.fit(X_train, y_train)
#confidence = clf.score(X_test, y_test)

#print(confidence)








#�塢����Ԥ��

y_pred = linreg.predict([[0.1,0,0]])
print(y_pred) #10��������Ԥ����




#������ͼ
y_pred = linreg.predict(X_test)
sum_mean=0
for i in range(len(y_pred)):
        sum_mean+=(y_pred[i]-y_test.values[i])**2
sum_erro=np.sqrt(sum_mean/23)  #���10������Լ�������
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
