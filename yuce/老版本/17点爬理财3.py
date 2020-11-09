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
collection.remove({'��ȡ����':{'$lt':shijian}})  #ɾ�����ڸ�ʱ��������

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






cursor = collection.find({ "$and":[{'��ȡ����':shijian} ] })
licai_df= pd.DataFrame(list(cursor)) 
if licai_df.empty:
    yemian=0
else:
    yemian=max(licai_df['ҳ��'].tolist())


maxtry=30
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}    
url0="http://data.bank.hexun.com/lccp/AllLccp.aspx?col=fld_type&tag=desc&orderMarks=&page="







#�ӵڶ�ҳ��ʼѭ��
for i in range(yemian+1,90):
  url2=url0+str(i)
  print(url2)
  for tries in range(maxtry):
    try:
  
        req = urllib.request.Request(url2,headers = headers)
        menuCode=urllib.request.urlopen(req,timeout=20).read()  # ����ҳԴ���븳��menuCode
    except:
       if tries<(maxtry-1):
          print(tries)
          continue
       else:
          print("Has tried %d times to access  %s, all failed!"%( maxtry, url2))
          print(tries)
          stop 
        
  soup=BeautifulSoup(menuCode,'html.parser')  # ʹ��html���������н���
  pattern = '[0-9][0-9][0-9][0-9][0-9][0-9].shtml'
  trSoup = soup.find("table", id="Table1")

  if trSoup is None:
          print('����')
          break
  foundAllTr1 = trSoup.findAll("tr")


 #��ȡ���� 
  mingzi1= foundAllTr1[0].findAll("th")
#��ȡ��һ�������Ϣ
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
                                '����':lian,
                                '��ȡ����':shijian,
                                'ҳ��':i
                      })
 # print(zong0)

#ѭ����ȡ���漸����Ϣ
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
                                '����':lian,
                                '��ȡ����':shijian,
                                'ҳ��':i
                      })


   
     zong0=pd.concat([zong0,zong1])
  #zong00=pd.concat([zong00,zong0])
  zong0= zong0.reset_index(drop=True)    #���¶�������
  records = json.loads(zong0.T.to_json()).values() 
  collection.insert(records)


  
#print(zong00)
#zong00.to_csv('dd.csv')







font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15) #������ɢ��ͼ���������



cursor = collection2.find({ "$and":[{'date':shijian} ] })
hexunlicai_zong= pd.DataFrame(list(cursor)) 
if hexunlicai_zong.empty:
    yemian=0
    cursor = collection.find({ "$and":[{'��ȡ����':shijian} ] })
    result= pd.DataFrame(list(cursor)) 


        
    result['ͣ����'] = pd.to_datetime(result['ͣ����'])   #ת��Ϊ���ڸ�ʽ

    result=result[(result['ͣ����']>shijian )&(result['������(��)']!='--')&(result['Ԥ������(%)']!='--')]

#�ѹ����µ���λС���ĳ�0λС��
    result['������(��)2'] =result['������(��)'].astype('float') 
    result=result.round({'������(��)2':0})
    result['������(��)2'] =result['������(��)2'].astype('int')
    result['Ԥ������(%)'] =result['Ԥ������(%)'].astype('float') 




    result= result.reset_index(drop=True)    #���¶�������
    for i in range(0,len(result)):
        result.loc[i,'����']='����'
        for j in range(0,len(cundanbank_df)):
          if cundanbank_df.astype(str).loc[j,'����'].strip() in result.loc[i,'����']:
            result.loc[i,'����']=cundanbank_df.astype(str).loc[j,'����2'].strip()
            break



#�������ݱ�
        
    resultz=result[(result['����']!='������')&((result['������(��)2']==3)|(result['������(��)2']==6)|(result['������(��)2']==12))]
#һ��������
    result3y=resultz[resultz['������(��)2']==3]
    mean=result3y['Ԥ������(%)'].mean()
    std=result3y['Ԥ������(%)'].std()
    result3y=result3y[(result3y['Ԥ������(%)']<(mean+std))&(result3y['Ԥ������(%)']>(mean-std))]

    result3y = result3y.reset_index(drop=False)    #���¶�������




    #1.���׼�ƽ����
    result3y1=result3y['Ԥ������(%)'].groupby([result3y['����']]).size().fillna(0)
    result3y1 = result3y1.reset_index(drop=False)    #���¶�������
    result3y1.rename(columns={'Ԥ������(%)': '������'}, inplace=True)
    result3y1 = result3y1.set_index('����')    #���¶�������

    result3y2=result3y['Ԥ������(%)'].groupby([result3y['����']]).std().fillna(0)
    result3y2 = result3y2.reset_index(drop=False)    #���¶�������
    result3y2.rename(columns={'Ԥ������(%)': '��׼��'}, inplace=True)
    result3y2 = result3y2.set_index('����')    #���¶�������

    result3y3=result3y['Ԥ������(%)'].groupby([result3y['����']]).mean().fillna(0)
    result3y3 = result3y3.reset_index(drop=False)    #���¶�������
    result3y3.rename(columns={'Ԥ������(%)': 'ƽ����'}, inplace=True)
    result3y3 = result3y3.set_index('����')    #���¶�������

    result3y3= pd.concat([result3y1, result3y2,result3y3], axis=1)
    result3y3 = result3y3.reset_index(drop=False)    #���¶�������

    #2.��ϴ����
    for i in range(0,len(result3y)):
       for j in range(0,len(result3y3)):
           if result3y.loc[i,'����']==result3y3.loc[j,'����']:
               result3y.loc[i,'ɸѡ1'] = (result3y3.loc[j,'ƽ����']-result3y3.loc[j,'��׼��'])
               result3y.loc[i,'ɸѡ2'] = (result3y3.loc[j,'ƽ����']+result3y3.loc[j,'��׼��'])
               break

    result3y=result3y[(result3y['Ԥ������(%)']<result3y['ɸѡ2'])&(result3y['Ԥ������(%)']>result3y['ɸѡ1'])]
    result3y3x=result3y['Ԥ������(%)'].groupby([result3y['����']]).mean().fillna(0)
    result3y3x = result3y3x.reset_index(drop=False)    #���¶�������


    #����������
    result6y=resultz[resultz['������(��)2']==6]
    mean=result6y['Ԥ������(%)'].mean()
    std=result6y['Ԥ������(%)'].std()
    result6y=result6y[(result6y['Ԥ������(%)']<(mean+std))&(result6y['Ԥ������(%)']>(mean-std))]

    result6y = result6y.reset_index(drop=False)    #���¶�������

    #1.���׼�ƽ����
    result6y1=result6y['Ԥ������(%)'].groupby([result6y['����']]).size().fillna(0)
    result6y1 = result6y1.reset_index(drop=False)    #���¶�������
    result6y1.rename(columns={'Ԥ������(%)': '������'}, inplace=True)
    result6y1 = result6y1.set_index('����')    #���¶�������

    result6y2=result6y['Ԥ������(%)'].groupby([result6y['����']]).std().fillna(0)
    result6y2 = result6y2.reset_index(drop=False)    #���¶�������
    result6y2.rename(columns={'Ԥ������(%)': '��׼��'}, inplace=True)
    result6y2 = result6y2.set_index('����')    #���¶�������

    result6y3=result6y['Ԥ������(%)'].groupby([result6y['����']]).mean().fillna(0)
    result6y3 = result6y3.reset_index(drop=False)    #���¶�������
    result6y3.rename(columns={'Ԥ������(%)': 'ƽ����'}, inplace=True)
    result6y3 = result6y3.set_index('����')    #���¶�������

    result6y3= pd.concat([result6y1, result6y2,result6y3], axis=1)
    result6y3 = result6y3.reset_index(drop=False)    #���¶�������

    #2.��ϴ����
    for i in range(0,len(result6y)):
       for j in range(0,len(result6y3)):
           if result6y.loc[i,'����']==result6y3.loc[j,'����']:
               result6y.loc[i,'ɸѡ1'] = (result6y3.loc[j,'ƽ����']-result6y3.loc[j,'��׼��'])
               result6y.loc[i,'ɸѡ2'] = (result6y3.loc[j,'ƽ����']+result6y3.loc[j,'��׼��'])
               break

    result6y=result6y[(result6y['Ԥ������(%)']<result6y['ɸѡ2'])&(result6y['Ԥ������(%)']>result6y['ɸѡ1'])]
    result6y3x=result6y['Ԥ������(%)'].groupby([result6y['����']]).mean().fillna(0)
    result6y3x = result6y3x.reset_index(drop=False)    #���¶�������




    #����12����
    result12y=resultz[resultz['������(��)2']==12]
    mean=result12y['Ԥ������(%)'].mean()
    std=result12y['Ԥ������(%)'].std()
    result12y=result12y[(result12y['Ԥ������(%)']<(mean+std))&(result12y['Ԥ������(%)']>(mean-std))]

    result12y = result12y.reset_index(drop=False)    #���¶�������

    #1.���׼�ƽ����
    result12y1=result12y['Ԥ������(%)'].groupby([result12y['����']]).size().fillna(0)
    result12y1 = result12y1.reset_index(drop=False)    #���¶�������
    result12y1.rename(columns={'Ԥ������(%)': '������'}, inplace=True)
    result12y1 = result12y1.set_index('����')    #���¶�������

    result12y2=result12y['Ԥ������(%)'].groupby([result12y['����']]).std().fillna(0)
    result12y2 = result12y2.reset_index(drop=False)    #���¶�������
    result12y2.rename(columns={'Ԥ������(%)': '��׼��'}, inplace=True)
    result12y2 = result12y2.set_index('����')    #���¶�������

    result12y3=result12y['Ԥ������(%)'].groupby([result12y['����']]).mean().fillna(0)
    result12y3 = result12y3.reset_index(drop=False)    #���¶�������
    result12y3.rename(columns={'Ԥ������(%)': 'ƽ����'}, inplace=True)
    result12y3 = result12y3.set_index('����')    #���¶�������

    result12y3= pd.concat([result12y1, result12y2,result12y3], axis=1)
    result12y3 = result12y3.reset_index(drop=False)    #���¶�������
    print('12�·�������')

    print(result12y3)
    #2.��ϴ����
    for i in range(0,len(result12y)):
       for j in range(0,len(result12y3)):
           if result12y.loc[i,'����']==result12y3.loc[j,'����']:
               result12y.loc[i,'ɸѡ1'] = (result12y3.loc[j,'ƽ����']-result12y3.loc[j,'��׼��'])
               result12y.loc[i,'ɸѡ2'] = (result12y3.loc[j,'ƽ����']+result12y3.loc[j,'��׼��'])
               break

    result12y=result12y[(result12y['Ԥ������(%)']<result12y['ɸѡ2'])&(result12y['Ԥ������(%)']>result12y['ɸѡ1'])]
    result12y3x=result12y['Ԥ������(%)'].groupby([result12y['����']]).mean().fillna(0)
    result12y3x = result12y3x.reset_index(drop=False)    #���¶�������
    print('12�����ʱ�')
    print(result12y3x)

    #3.�ϱ�
    result12y3x=result12y3x.set_index('����')
    result12y3=result12y3.set_index('����')
    result12z= pd.concat([result12y3x,result12y3], axis=1)
    result12z['����']='12����'


    result6y3x=result6y3x.set_index('����')
    result6y3=result6y3.set_index('����')
    result6z= pd.concat([result6y3x,result6y3], axis=1)
    result6z['����']='6����'


    result3y3x=result3y3x.set_index('����')
    result3y3=result3y3.set_index('����')
    result3z= pd.concat([result3y3x,result3y3], axis=1)
    result3z['����']='3����'


    print(result3z)

    resultz= pd.concat([result3z,result6z,result12z], axis=0)
    print(resultz)

    resultz['����']=shijian
    resultz =resultz.reset_index(drop=False)    #���¶�������

    resultz=resultz.set_index('����')
    print(resultz)
    #resultz=resultz[['����','Ԥ������(%)','������','����']]

    resultz= resultz.reset_index(drop=False)    #���¶�������
    records = json.loads(resultz.T.to_json()).values() 
    collection5.insert(records)













#���ܱ����뵽���ݿ�
        
    test5 = result['����'].groupby([result['������(��)2'],result['����']]).size().unstack('����').fillna(0)

    test5['date']=shijian
    test5= test5.reset_index(drop=False)    #���¶�������
    records = json.loads(test5.T.to_json()).values() 
    collection2.insert(records)


#�ܱ�ͼ
    test5.plot(kind='bar', alpha=1,stacked=True)
    plt.legend(prop=font_set)  #��ʾlable
    plt.xlabel('�������ޣ��£�',fontproperties=font_set)
    plt.ylabel('���������',fontproperties=font_set)
    plt.title('%s ��Ʒ���'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��
    plt.savefig('licai/image/licaihuatu.png')
    plt.show()


#�������µ��������������ݿ�
    licai3=result[(result['������(��)2']==3)]
    licai3['Ԥ������(%)'] =licai3['Ԥ������(%)'].astype('float')
    licai3=licai3.round({'Ԥ������(%)':1})
    licai3=licai3['����'].groupby([licai3['Ԥ������(%)'],licai3['����']]).size().unstack('����').fillna(0)
    licai3['date']=shijian
    licai3['����']='3����'

    licai3= licai3.reset_index(drop=False)    #���¶�������

    records = json.loads(licai3.T.to_json()).values() 
    collection4.insert(records)

    licai3.plot(kind='bar', alpha=1,stacked=True)
    plt.legend(prop=font_set)  #��ʾlable
    plt.xlabel('Ԥ������(%)',fontproperties=font_set)
    plt.ylabel('���������',fontproperties=font_set)
    plt.title('%s 3������Ʒ�������'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��
    plt.savefig('licai/image/licaili3.png')
    plt.show()

#�����µĻ������������ͼ
    licai3=result[(result['������(��)2']==6)]
    licai3['Ԥ������(%)'] =licai3['Ԥ������(%)'].astype('float') 
    licai3=licai3.round({'Ԥ������(%)':1})

    licai3=licai3['����'].groupby([licai3['Ԥ������(%)'],licai3['����']]).size().unstack('����').fillna(0)
    licai3['date']=shijian
    licai3['����']='6����'

    licai3= licai3.reset_index(drop=False)    #���¶�������

    records = json.loads(licai3.T.to_json()).values() 
    collection4.insert(records)
    
    licai3.plot(kind='bar', alpha=1,stacked=True)
    plt.legend(prop=font_set)  #��ʾlable
    plt.xlabel('Ԥ������(%)',fontproperties=font_set)
    plt.ylabel('���������',fontproperties=font_set)
    plt.title('%s 6������Ʒ�������'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��
    plt.savefig('licai/image/licaili6.png')
    plt.show()

#1��Ļ������������ͼ
    licai3=result[(result['������(��)2']==12)]
    licai3['Ԥ������(%)'] =licai3['Ԥ������(%)'].astype('float') 
    licai3=licai3.round({'Ԥ������(%)':1})

    licai3=licai3['����'].groupby([licai3['Ԥ������(%)'],licai3['����']]).size().unstack('����').fillna(0)
    licai3['date']=shijian
    licai3['����']='12����'

    licai3= licai3.reset_index(drop=False)    #���¶�������

    records = json.loads(licai3.T.to_json()).values() 
    collection4.insert(records)
    
    licai3.plot(kind='bar', alpha=1,stacked=True)
    plt.legend(prop=font_set)  #��ʾlable
    plt.xlabel('Ԥ������(%)',fontproperties=font_set)
    plt.ylabel('���������',fontproperties=font_set)
    plt.title('%s 1����Ʒ�������'%shijian, fontproperties=font_set) 
    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��
    plt.savefig('licai/image/licaili12.png')
    plt.show()






    
else:
    print('�Ѿ�����!')
















