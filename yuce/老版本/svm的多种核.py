# -*- coding: cp936 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame,Series
import matplotlib as mpl   #显示中文
from sklearn import metrics
from sklearn import preprocessing, cross_validation, svm
from sklearn.model_selection import train_test_split   #这里是引用了交叉验证 
from sklearn.linear_model import LinearRegression
import numpy as np
import  math
from sklearn import preprocessing, cross_validation, svm



#一、读取数据，并且标准化
url='zong.csv'
df = pd.read_table(url,sep=',',encoding='GB18030')   #用dictreader根据行内容查找
df=df[['3个月同业存单利率','3个月后一天','后一天利率','收票/出票','足年国股']]
df=df.dropna(axis=0,how='any')
df['后一天增长率']=(df['后一天利率']-df['足年国股'])/df['足年国股']
df['3个月后一天增长率']=(df['3个月后一天']-df['3个月同业存单利率'])/df['3个月同业存单利率']


#df['后一天增长率z'] = (df['后一天增长率']-df['后一天增长率'].mean())/df['后一天增长率'].std()    #转化为标准分数
df['足年国股z'] = (df['足年国股']-df['足年国股'].mean())/df['足年国股'].std()    #转化为标准分数
#df['质押式回购7天z'] = (df['质押式回购7天']-df['质押式回购7天'].mean())/df['质押式回购7天'].std()    #转化为标准分数
#df['隔夜拆借z'] = (df['隔夜拆借']-df['隔夜拆借'].mean())/df['隔夜拆借'].std()    #转化为标准分数
df['3个月后一天增长率z'] = (df['3个月后一天增长率']-df['3个月后一天增长率'].mean())/df['3个月后一天增长率'].std()    #转化为标准分数
#df['贴现量/成交金额z'] = (df['贴现量/成交金额']-df['贴现量/成交金额'].mean())/df['贴现量/成交金额'].std()    #转化为标准分数
df['收票/出票z'] = (df['收票/出票']-df['收票/出票'].mean())/df['收票/出票'].std()    #转化为标准分数
print(df)


#二、画散点图
sns.pairplot(df, x_vars=['3个月后一天增长率z','收票/出票z','足年国股z'], y_vars='后一天增长率',kind="reg", size=5, aspect=0.7)
mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号，如果是plt画图，则将mlp换成plt
plt.show()#注意必须加上这一句，否则无法显示。



#三、构建模型

X=df.loc[:,('3个月后一天增长率z','收票/出票z','足年国股z')]
y=df.loc[:,'后一天增长率']
print(len(df))










#四、构建训练集和测试集
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state=1)
print ('X_train.shape={}\n y_train.shape ={}\n X_test.shape={}\n,  y_test.shape={}'.format(X_train.shape,y_train.shape, X_test.shape,y_test.shape))

#4.1回归模型
linreg = LinearRegression()
model=linreg.fit(X_train, y_train)
congidence=linreg.score(X_test, y_test)  #查看测试模型的准确率
print (model)
print(congidence)
    # 训练后模型截距
print (linreg.intercept_)
    # 训练后模型权重（特征个数无变化）
print (linreg.coef_)

#4.2 分类器模型
#2.2.1看是那个模型最符合
#for k in ['linear','poly','rbf','sigmoid']:
 #   clf = svm.SVR(kernel=k)
  #  clf.fit(X_train, y_train)
   # confidence = clf.score(X_test, y_test)
    #print(k,confidence)

#2.2.2直接计算最符合的模型数值
#clf = svm.SVR()
#clf.fit(X_train, y_train)
#confidence = clf.score(X_test, y_test)

#print(confidence)








#五、变量预测

y_pred = linreg.predict([[0.1,0,0]])
print(y_pred) #10个变量的预测结果




#六、画图
y_pred = linreg.predict(X_test)
sum_mean=0
for i in range(len(y_pred)):
        sum_mean+=(y_pred[i]-y_test.values[i])**2
sum_erro=np.sqrt(sum_mean/23)  #这个10是你测试级的数量
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
