# -*- coding: cp936 -*-
import pandas as pd
from bs4 import BeautifulSoup
import urllib
import requests
from pymongo import MongoClient
import cgi,time
import re,datetime,json
from math import  floor
from matplotlib.font_manager import FontProperties  
import matplotlib.pyplot as plt

shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
print(shijian)
client=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')
db = client.hexunlicai
collection = db.hexunlicai
collection.remove({'爬取日期':{'$lt':shijian}})  #删除早于该时间点的数据

db2 = client.hexunlicai_zong
collection2 = db2.hexunlicai_zong

db3 = client.cundanbank
collection3 = db3.cundanbank
cursor = collection3.find()
cundanbank_df= pd.DataFrame(list(cursor))

db4 = client.hexunlicai_qi
collection4= db4.hexunlicai_qi



db5= client.hexunlicai_lilv
collection5= db5.hexunlicai_lilv






cursor = collection.find({ "$and":[{'爬取日期':shijian} ] })
licai_df= pd.DataFrame(list(cursor)) 
if licai_df.empty:
    yemian=0
else:
    yemian=max(licai_df['页面'].tolist())


maxtry=30
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}    
url0="http://data.bank.hexun.com/lccp/AllLccp.aspx?col=fld_type&tag=desc&orderMarks=&page="







#从第二页开始循环
for i in range(yemian+1,90):
  url2=url0+str(i)
  print(url2)
  for tries in range(maxtry):
    try:
  
        req = urllib.request.Request(url2,headers = headers)
        menuCode=urllib.request.urlopen(req,timeout=20).read()  # 将网页源代码赋予menuCode
    except:
       if tries<(maxtry-1):
          print(tries)
          continue
       else:
          print("Has tried %d times to access  %s, all failed!"%( maxtry, url2))
          print(tries)
          stop 
        
  soup=BeautifulSoup(menuCode,'html.parser')  # 使用html解析器进行解析
  pattern = '[0-9][0-9][0-9][0-9][0-9][0-9].shtml'
  trSoup = soup.find("table", id="Table1")

  if trSoup is None:
          print('结束')
          break
  foundAllTr1 = trSoup.findAll("tr")


 #获取标题 
  mingzi1= foundAllTr1[0].findAll("th")
#获取第一条理财信息
  for url in foundAllTr1[1].find_all("a"):
                url_search = re.search(pattern,str(url.get('href')))
                if url_search:         
                    url='http://data.bank.hexun.com/lccp/'+str(url.get('href'))
                    lian=url
                    
  Td1=foundAllTr1[1].findAll("td")
  zong0=pd.DataFrame({mingzi1[0].get_text(): [Td1[0].get_text()],
                                mingzi1[1].get_text(): [Td1[1].get_text()],
                                mingzi1[2].get_text(): [Td1[2].get_text()],
                                mingzi1[3].get_text(): [Td1[3].get_text()],
                                mingzi1[4].get_text(): [Td1[4].get_text()],
                                mingzi1[5].get_text(): [Td1[5].get_text()],
                                mingzi1[6].get_text(): [Td1[6].get_text()],
                                mingzi1[7].get_text(): [Td1[7].get_text()],
                                mingzi1[8].get_text(): [Td1[8].get_text()],
                                '链接':lian,
                                '爬取日期':shijian,
                                '页面':i
                      })
 # print(zong0)

#循环获取后面几条信息
  for j in range(2,len(foundAllTr1)):
     for url in foundAllTr1[j].find_all("a"):
                url_search = re.search(pattern,str(url.get('href')))
                if url_search:         
                    url='http://data.bank.hexun.com/lccp/'+str(url.get('href'))
                    lian=url
     Td1=foundAllTr1[j].findAll("td")

  #   if lian not in licail:
     zong1=pd.DataFrame({mingzi1[0].get_text(): [Td1[0].get_text()],
                                mingzi1[1].get_text(): [Td1[1].get_text()],
                                mingzi1[2].get_text(): [Td1[2].get_text()],
                                mingzi1[3].get_text(): [Td1[3].get_text()],
                                mingzi1[4].get_text(): [Td1[4].get_text()],
                                mingzi1[5].get_text(): [Td1[5].get_text()],
                                mingzi1[6].get_text(): [Td1[6].get_text()],
                                mingzi1[7].get_text(): [Td1[7].get_text()],
                                mingzi1[8].get_text(): [Td1[8].get_text()],
                                '链接':lian,
                                '爬取日期':shijian,
                                '页面':i
                      })


   
     zong0=pd.concat([zong0,zong1])
  #zong00=pd.concat([zong00,zong0])
  zong0= zong0.reset_index(drop=True)    #重新定义索引
  records = json.loads(zong0.T.to_json()).values() 
  collection.insert(records)


  
#print(zong00)
#zong00.to_csv('dd.csv')







font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15) #用于在散点图中输出中文



cursor = collection2.find({ "$and":[{'date':shijian} ] })
hexunlicai_zong= pd.DataFrame(list(cursor)) 
if hexunlicai_zong.empty:
    yemian=0
    cursor = collection.find({ "$and":[{'爬取日期':shijian} ] })
    result= pd.DataFrame(list(cursor)) 


        
    result['停售日'] = pd.to_datetime(result['停售日'])   #转换为日期格式

    result=result[(result['停售日']>shijian )&(result['管理期(月)']!='--')&(result['预期收益(%)']!='--')]

#把管理月的两位小数改成0位小数
    result['管理期(月)2'] =result['管理期(月)'].astype('float') 
    result=result.round({'管理期(月)2':0})
    result['管理期(月)2'] =result['管理期(月)2'].astype('int')
    result['预期收益(%)'] =result['预期收益(%)'].astype('float') 




    result= result.reset_index(drop=True)    #重新定义索引
    for i in range(0,len(result)):
        result.loc[i,'行类']='城商'
        for j in range(0,len(cundanbank_df)):
          if cundanbank_df.astype(str).loc[j,'银行'].strip() in result.loc[i,'银行']:
            result.loc[i,'行类']=cundanbank_df.astype(str).loc[j,'分类2'].strip()
            break



#制作数据表
        
    resultz=result[(result['行类']!='外资行')&((result['管理期(月)2']==3)|(result['管理期(月)2']==6)|(result['管理期(月)2']==12))]
#一、三个月
    result3y=resultz[resultz['管理期(月)2']==3]
    mean=result3y['预期收益(%)'].mean()
    std=result3y['预期收益(%)'].std()
    result3y=result3y[(result3y['预期收益(%)']<(mean+std))&(result3y['预期收益(%)']>(mean-std))]

    result3y = result3y.reset_index(drop=False)    #重新定义索引




    #1.算标准差、平均数
    result3y1=result3y['预期收益(%)'].groupby([result3y['行类']]).size().fillna(0)
    result3y1 = result3y1.reset_index(drop=False)    #重新定义索引
    result3y1.rename(columns={'预期收益(%)': '发行数'}, inplace=True)
    result3y1 = result3y1.set_index('行类')    #重新定义索引

    result3y2=result3y['预期收益(%)'].groupby([result3y['行类']]).std().fillna(0)
    result3y2 = result3y2.reset_index(drop=False)    #重新定义索引
    result3y2.rename(columns={'预期收益(%)': '标准差'}, inplace=True)
    result3y2 = result3y2.set_index('行类')    #重新定义索引

    result3y3=result3y['预期收益(%)'].groupby([result3y['行类']]).mean().fillna(0)
    result3y3 = result3y3.reset_index(drop=False)    #重新定义索引
    result3y3.rename(columns={'预期收益(%)': '平均数'}, inplace=True)
    result3y3 = result3y3.set_index('行类')    #重新定义索引

    result3y3= pd.concat([result3y1, result3y2,result3y3], axis=1)
    result3y3 = result3y3.reset_index(drop=False)    #重新定义索引

    #2.清洗数据
    for i in range(0,len(result3y)):
       for j in range(0,len(result3y3)):
           if result3y.loc[i,'行类']==result3y3.loc[j,'行类']:
               result3y.loc[i,'筛选1'] = (result3y3.loc[j,'平均数']-result3y3.loc[j,'标准差'])
               result3y.loc[i,'筛选2'] = (result3y3.loc[j,'平均数']+result3y3.loc[j,'标准差'])
               break

    result3y=result3y[(result3y['预期收益(%)']<result3y['筛选2'])&(result3y['预期收益(%)']>result3y['筛选1'])]
    result3y3x=result3y['预期收益(%)'].groupby([result3y['行类']]).mean().fillna(0)
    result3y3x = result3y3x.reset_index(drop=False)    #重新定义索引


    #二、六个月
    result6y=resultz[resultz['管理期(月)2']==6]
    mean=result6y['预期收益(%)'].mean()
    std=result6y['预期收益(%)'].std()
    result6y=result6y[(result6y['预期收益(%)']<(mean+std))&(result6y['预期收益(%)']>(mean-std))]

    result6y = result6y.reset_index(drop=False)    #重新定义索引

    #1.算标准差、平均数
    result6y1=result6y['预期收益(%)'].groupby([result6y['行类']]).size().fillna(0)
    result6y1 = result6y1.reset_index(drop=False)    #重新定义索引
    result6y1.rename(columns={'预期收益(%)': '发行数'}, inplace=True)
    result6y1 = result6y1.set_index('行类')    #重新定义索引

    result6y2=result6y['预期收益(%)'].groupby([result6y['行类']]).std().fillna(0)
    result6y2 = result6y2.reset_index(drop=False)    #重新定义索引
    result6y2.rename(columns={'预期收益(%)': '标准差'}, inplace=True)
    result6y2 = result6y2.set_index('行类')    #重新定义索引

    result6y3=result6y['预期收益(%)'].groupby([result6y['行类']]).mean().fillna(0)
    result6y3 = result6y3.reset_index(drop=False)    #重新定义索引
    result6y3.rename(columns={'预期收益(%)': '平均数'}, inplace=True)
    result6y3 = result6y3.set_index('行类')    #重新定义索引

    result6y3= pd.concat([result6y1, result6y2,result6y3], axis=1)
    result6y3 = result6y3.reset_index(drop=False)    #重新定义索引

    #2.清洗数据
    for i in range(0,len(result6y)):
       for j in range(0,len(result6y3)):
           if result6y.loc[i,'行类']==result6y3.loc[j,'行类']:
               result6y.loc[i,'筛选1'] = (result6y3.loc[j,'平均数']-result6y3.loc[j,'标准差'])
               result6y.loc[i,'筛选2'] = (result6y3.loc[j,'平均数']+result6y3.loc[j,'标准差'])
               break

    result6y=result6y[(result6y['预期收益(%)']<result6y['筛选2'])&(result6y['预期收益(%)']>result6y['筛选1'])]
    result6y3x=result6y['预期收益(%)'].groupby([result6y['行类']]).mean().fillna(0)
    result6y3x = result6y3x.reset_index(drop=False)    #重新定义索引




    #三、12个月
    result12y=resultz[resultz['管理期(月)2']==12]
    mean=result12y['预期收益(%)'].mean()
    std=result12y['预期收益(%)'].std()
    result12y=result12y[(result12y['预期收益(%)']<(mean+std))&(result12y['预期收益(%)']>(mean-std))]

    result12y = result12y.reset_index(drop=False)    #重新定义索引

    #1.算标准差、平均数
    result12y1=result12y['预期收益(%)'].groupby([result12y['行类']]).size().fillna(0)
    result12y1 = result12y1.reset_index(drop=False)    #重新定义索引
    result12y1.rename(columns={'预期收益(%)': '发行数'}, inplace=True)
    result12y1 = result12y1.set_index('行类')    #重新定义索引

    result12y2=result12y['预期收益(%)'].groupby([result12y['行类']]).std().fillna(0)
    result12y2 = result12y2.reset_index(drop=False)    #重新定义索引
    result12y2.rename(columns={'预期收益(%)': '标准差'}, inplace=True)
    result12y2 = result12y2.set_index('行类')    #重新定义索引

    result12y3=result12y['预期收益(%)'].groupby([result12y['行类']]).mean().fillna(0)
    result12y3 = result12y3.reset_index(drop=False)    #重新定义索引
    result12y3.rename(columns={'预期收益(%)': '平均数'}, inplace=True)
    result12y3 = result12y3.set_index('行类')    #重新定义索引

    result12y3= pd.concat([result12y1, result12y2,result12y3], axis=1)
    result12y3 = result12y3.reset_index(drop=False)    #重新定义索引
    print('12月发行数表')

    print(result12y3)
    #2.清洗数据
    for i in range(0,len(result12y)):
       for j in range(0,len(result12y3)):
           if result12y.loc[i,'行类']==result12y3.loc[j,'行类']:
               result12y.loc[i,'筛选1'] = (result12y3.loc[j,'平均数']-result12y3.loc[j,'标准差'])
               result12y.loc[i,'筛选2'] = (result12y3.loc[j,'平均数']+result12y3.loc[j,'标准差'])
               break

    result12y=result12y[(result12y['预期收益(%)']<result12y['筛选2'])&(result12y['预期收益(%)']>result12y['筛选1'])]
    result12y3x=result12y['预期收益(%)'].groupby([result12y['行类']]).mean().fillna(0)
    result12y3x = result12y3x.reset_index(drop=False)    #重新定义索引
    print('12月利率表')
    print(result12y3x)

    #3.合表
    result12y3x=result12y3x.set_index('行类')
    result12y3=result12y3.set_index('行类')
    result12z= pd.concat([result12y3x,result12y3], axis=1)
    result12z['期限']='12个月'


    result6y3x=result6y3x.set_index('行类')
    result6y3=result6y3.set_index('行类')
    result6z= pd.concat([result6y3x,result6y3], axis=1)
    result6z['期限']='6个月'


    result3y3x=result3y3x.set_index('行类')
    result3y3=result3y3.set_index('行类')
    result3z= pd.concat([result3y3x,result3y3], axis=1)
    result3z['期限']='3个月'


    print(result3z)

    resultz= pd.concat([result3z,result6z,result12z], axis=0)
    print(resultz)

    resultz['日期']=shijian
    resultz =resultz.reset_index(drop=False)    #重新定义索引

    resultz=resultz.set_index('日期')
    print(resultz)
    #resultz=resultz[['行类','预期收益(%)','发行数','期限']]

    resultz= resultz.reset_index(drop=False)    #重新定义索引
    records = json.loads(resultz.T.to_json()).values() 
    collection5.insert(records)













#把总表输入到数据库
        
    test5 = result['链接'].groupby([result['管理期(月)2'],result['行类']]).size().unstack('行类').fillna(0)

    test5['date']=shijian
    test5= test5.reset_index(drop=False)    #重新定义索引
    records = json.loads(test5.T.to_json()).values() 
    collection2.insert(records)


#总表画图
    test5.plot(kind='bar', alpha=1,stacked=True)
    plt.legend(prop=font_set)  #显示lable
    plt.xlabel('发行期限（月）',fontproperties=font_set)
    plt.ylabel('发行理财数',fontproperties=font_set)
    plt.title('%s 理财发行'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.savefig('licai/image/licaihuatu.png')
    plt.show()


#把三个月的总数据输入数据库
    licai3=result[(result['管理期(月)2']==3)]
    licai3['预期收益(%)'] =licai3['预期收益(%)'].astype('float')
    licai3=licai3.round({'预期收益(%)':1})
    licai3=licai3['链接'].groupby([licai3['预期收益(%)'],licai3['行类']]).size().unstack('行类').fillna(0)
    licai3['date']=shijian
    licai3['期限']='3个月'

    licai3= licai3.reset_index(drop=False)    #重新定义索引

    records = json.loads(licai3.T.to_json()).values() 
    collection4.insert(records)

    licai3.plot(kind='bar', alpha=1,stacked=True)
    plt.legend(prop=font_set)  #显示lable
    plt.xlabel('预期收益(%)',fontproperties=font_set)
    plt.ylabel('发行理财数',fontproperties=font_set)
    plt.title('%s 3个月理财发行利率'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.savefig('licai/image/licaili3.png')
    plt.show()

#六个月的画利率银行类别图
    licai3=result[(result['管理期(月)2']==6)]
    licai3['预期收益(%)'] =licai3['预期收益(%)'].astype('float') 
    licai3=licai3.round({'预期收益(%)':1})

    licai3=licai3['链接'].groupby([licai3['预期收益(%)'],licai3['行类']]).size().unstack('行类').fillna(0)
    licai3['date']=shijian
    licai3['期限']='6个月'

    licai3= licai3.reset_index(drop=False)    #重新定义索引

    records = json.loads(licai3.T.to_json()).values() 
    collection4.insert(records)
    
    licai3.plot(kind='bar', alpha=1,stacked=True)
    plt.legend(prop=font_set)  #显示lable
    plt.xlabel('预期收益(%)',fontproperties=font_set)
    plt.ylabel('发行理财数',fontproperties=font_set)
    plt.title('%s 6个月理财发行利率'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.savefig('licai/image/licaili6.png')
    plt.show()

#1年的画利率银行类别图
    licai3=result[(result['管理期(月)2']==12)]
    licai3['预期收益(%)'] =licai3['预期收益(%)'].astype('float') 
    licai3=licai3.round({'预期收益(%)':1})

    licai3=licai3['链接'].groupby([licai3['预期收益(%)'],licai3['行类']]).size().unstack('行类').fillna(0)
    licai3['date']=shijian
    licai3['期限']='12个月'

    licai3= licai3.reset_index(drop=False)    #重新定义索引

    records = json.loads(licai3.T.to_json()).values() 
    collection4.insert(records)
    
    licai3.plot(kind='bar', alpha=1,stacked=True)
    plt.legend(prop=font_set)  #显示lable
    plt.xlabel('预期收益(%)',fontproperties=font_set)
    plt.ylabel('发行理财数',fontproperties=font_set)
    plt.title('%s 1年理财发行利率'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.savefig('licai/image/licaili12.png')
    plt.show()






    
else:
    print('已经更新!')
















