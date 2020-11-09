import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl   #显示中文
import json,csv
import pandas as pd
import statsmodels.api as sm
from pymongo import MongoClient
import numpy as np
import seaborn as sns
url='yuanshimoxing.csv'
df = pd.read_table(url,sep=',')   #用dictreader根据行内容查找
df=df.reset_index(drop = True)
print(df.head())


#df.日期.value_counts()#查看每个值的计数。
#1.统一NAN值
df.to_csv('xiaomoxing19.csv',header=True)

df.fillna('9',inplace=True)  #把日期列的nan 数值用“NAN”填充，统一空值
#df=df.dropna(how='any')
df.to_csv('xiaomoxing20.csv',header=True)
df.fillna(0)
df.to_csv('xiaomoxing21.csv',header=True)
print(df.fillna(method='bfill',inplace=True))
