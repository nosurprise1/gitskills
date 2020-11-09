# -*- coding: cp936 -*-
import datetime,time
maxTryNum=20
import json,csv
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12) #������ɢ��ͼ���������
font_set2 = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=9) #������ɢ��ͼ���������


username='18957170906'
password0 ='123'
url0='https://www.51tradecloud.com/'
password = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password.add_password(None,url0,username,password0)
handler=urllib.request.HTTPBasicAuthHandler(password)
opener = urllib.request.build_opener(handler)  
urllib.request.install_opener(opener)








def duqu2():
    global shijian,piaofen3
    url = url0+'31'
    for tries in range(maxTryNum):
            try:
                res_data = urllib.request.urlopen(url,timeout=35)
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    print("��������ϲ�޷�����")
                    break

    res = res_data.read()

    piaofen3=res.decode('utf-8')
    piaofen3= pd.read_json(piaofen3,typ='frame')  #������
    print(piaofen3)
    piaofen3=piaofen3[piaofen3['����']=='����']
    
    piaofen3['��ȡ����'] = pd.to_datetime(piaofen3['��ȡ����']).astype('str')     #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ

    piaofen3=piaofen3[piaofen3['��ȡ����']>='2018-08-01']
    piaofen3 = piaofen3.sort_values(by=['��ȡ����'], ascending=True)
    piaofen3= piaofen3.reset_index(drop=True)    #���¶�������

    shijian=piaofen3.loc[(len(piaofen3)-1),'��ȡ����']
    
    piaofen3=piaofen3.set_index(['��ȡ����'])
    piaofen3=piaofen3[['�жҽ��/��Ԫ','���ֽ��/��Ԫ','���׽��/��Ԫ']]
    
    piaofen4=piaofen3
    piaofen4['�ж�/����']=piaofen4['�жҽ��/��Ԫ']/piaofen4['���ֽ��/��Ԫ']
    piaofen4['�ж�/������']=piaofen4['�жҽ��/��Ԫ']/piaofen4['���׽��/��Ԫ']

    y1=piaofen4['�ж�/����'].tolist()
    y2=piaofen4['�ж�/������'].tolist()

    
    piaofen3=piaofen3[['�жҽ��/��Ԫ','���ֽ��/��Ԫ','���׽��/��Ԫ']]

    piaofen3.plot(kind='bar', alpha=0.4,stacked=False)
    plt.ylabel('������(��Ԫ)',fontproperties=font_set)
    plt.xlabel('')
    plt.legend(prop=font_set2,loc='upper left')  #��ʾlableλ��

    plt2=plt.twinx()
    plt2.plot(y1,alpha=0.7,label='�ж�/����')
    plt2.plot(y2,alpha=0.7,label='�ж�/������')

#�ڶ���������Ҫ��set
    plt2.set_ylabel('�ж�/����',fontproperties=font_set)

    plt2.legend(prop=font_set2,loc='upper center', bbox_to_anchor=(0.6,0.95))  #��ʾlable


    plt.title('%sƱ�ݽ��������ж�����������'%(shijian),fontproperties=font_set) 




    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��
    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('C:/Users/yangbing/wangye/wangye/static/images/piaojiaosuol.png') 
    fig.show()
    print('�ѵ���������')











def duqu():
    global shijian,piaofen2,df2
    url = url0+'11'
    for tries in range(maxTryNum):
            try:
                res_data = urllib.request.urlopen(url,timeout=35)
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    print("��������ϲ�޷�����")
                    break

    res = res_data.read()

    piaofen2=res.decode('utf-8')
    piaofen2= pd.read_json(piaofen2,typ='frame')  #������

    piaofen2['��ȡ����'] = pd.to_datetime(piaofen2['��ȡ����']).astype('str')   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ
    piaofen2 = piaofen2.sort_values(by=['��ȡ����'], ascending=True)
    piaofen2= piaofen2.reset_index(drop=True)    #���¶�������
    print(piaofen2)
    
    shijian=piaofen2.loc[(len(piaofen2)-1),'��ȡ����']
    
    piaofen3=piaofen2.set_index(['��ȡ����'])

    
    piaofen3=piaofen3[(piaofen3['Ʊ������']=='����')& (piaofen3['ҵ������']=='���ʽ')]

    print(piaofen3)
  #  piaofen3['��ȡ����'] = pd.to_datetime(piaofen3['��ȡ����'])   #,format='%Y%m%d'  ��yyyy-m-d ת��Ϊyyyy-mm-dd��ʱ���ʽ


    piaofen3=piaofen3[['1-3���£�����','3-6���£�����','9-12���£�����']]
    piaofen3.plot()
    plt.xlabel('')


    plt.ylabel('����(%)',fontproperties=font_set)
    plt.legend(prop=font_set)  #��ʾlable
    plt.title('%s�����޵�Ʊ����'%(shijian), fontproperties=font_set) 
    piaofen2.to_csv('piaoj.csv',mode='w',header=True)

    print('�ѵ�����Ȩ����')




    plt.gcf().autofmt_xdate()  # �Զ���ת���ڱ��
  #  plt.savefig('C:/Users/yangbing/wangye/wangye/static/images/piaojiaosuoli.png')
    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('C:/Users/Administrator/wangye/static/images/piaojiaosuoli.png')

    fig.show()



def charu():
    url='ee.csv'

    shuru1=input('����������ȡ��csv�ļ�������ȷ����ͬһ�ļ����£���������Ĭ��Ϊ��ee����:')
    if shuru1!='':
        url=shuru1
    
    df = pd.read_table(url,sep=',',encoding='GB18030')   #��dictreader���������ݲ���


   # global shijian
    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))

    shijian = datetime.datetime.strptime(shijian, "%Y-%m-%d")
    shijian=shijian-datetime.timedelta(days=1)

    shijian=str(shijian.strftime("%Y-%m-%d"))

    shuru=input('����������ȡ���ݵ�����,��ʽΪ��2017-11-01������������Ĭ��Ϊ����:')
    if shuru!='':
        shijian=shuru
#��ȡ���ʽ
    print(shijian)

    mai_yin=pd.DataFrame({'��ȡ����': [shijian],
                      'Ʊ������':['����'],
                      'ҵ������':['���ʽ'],
                    df.loc[0,'����']: [df.loc[0,'��Ʊ��Ȩ����%']],
                    df.loc[1,'����']: [df.loc[1,'��Ʊ��Ȩ����%']],
                    df.loc[2,'����']: [df.loc[2,'��Ʊ��Ȩ����%']],
                    df.loc[3,'����']: [df.loc[3,'��Ʊ��Ȩ����%']],
                    df.loc[4,'����']: [df.loc[4,'��Ʊ��Ȩ����%']],
                    df.loc[5,'����']: [df.loc[5,'��Ʊ��Ȩ����%']]

                         })
    mai_shang=pd.DataFrame({'��ȡ����': [shijian],
                      'Ʊ������':['����'],
                      'ҵ������':['���ʽ'],

                    df.loc[0,'����']: [df.loc[0,'��Ʊ��Ȩ����%']],
                    df.loc[1,'����']: [df.loc[1,'��Ʊ��Ȩ����%']],
                    df.loc[2,'����']: [df.loc[2,'��Ʊ��Ȩ����%']],
                    df.loc[3,'����']: [df.loc[3,'��Ʊ��Ȩ����%']],
                    df.loc[4,'����']: [df.loc[4,'��Ʊ��Ȩ����%']],
                    df.loc[5,'����']: [df.loc[5,'��Ʊ��Ȩ����%']]
                         })

#��ȡ��Ѻʽ
    hui_yin=pd.DataFrame({'��ȡ����': [shijian],
                      'Ʊ������':['����'],
                      'ҵ������':['�ع�ʽ'],

                    df.loc[0,'����.1']: [df.loc[0,'��Ʊ��Ȩ����%.1']],
                    df.loc[1,'����.1']: [df.loc[1,'��Ʊ��Ȩ����%.1']],
                    df.loc[2,'����.1']: [df.loc[2,'��Ʊ��Ȩ����%.1']],
                    df.loc[3,'����.1']: [df.loc[3,'��Ʊ��Ȩ����%.1']],
                    df.loc[4,'����.1']: [df.loc[4,'��Ʊ��Ȩ����%.1']],
                    df.loc[5,'����.1']: [df.loc[5,'��Ʊ��Ȩ����%.1']]
                         })
    hui_shang=pd.DataFrame({'��ȡ����': [shijian],
                      'Ʊ������':['����'],
                      'ҵ������':['�ع�ʽ'],

                    df.loc[0,'����.1']: [df.loc[0,'��Ʊ��Ȩ����%.1']],
                    df.loc[1,'����.1']: [df.loc[1,'��Ʊ��Ȩ����%.1']],
                    df.loc[2,'����.1']: [df.loc[2,'��Ʊ��Ȩ����%.1']],
                    df.loc[3,'����.1']: [df.loc[3,'��Ʊ��Ȩ����%.1']],
                    df.loc[4,'����.1']: [df.loc[4,'��Ʊ��Ȩ����%.1']],
                    df.loc[5,'����.1']: [df.loc[5,'��Ʊ��Ȩ����%.1']]
                         })



    maiyin = json.loads(mai_yin.T.to_json()).values()
    maishang = json.loads(mai_shang.T.to_json()).values()

    huishang = json.loads(hui_shang.T.to_json()).values()
    print(hui_shang)
    print(huishang)
    huishang=str(huishang).replace('dict_values([','')
    huishang=huishang.replace('])','')
    huishang = eval(huishang)
    huishang_df=pd.DataFrame(huishang, index=[0])
    

    print(huishang_df)

    
    stop

    url = url0+'2?maiyin='+urllib.parse.quote(str(maiyin))+'&maishang='+urllib.parse.quote(str(maishang))+'&huiyin='+urllib.parse.quote(str(huiyin))+'&huishang='+urllib.parse.quote(str(huishang))+'&shijian='+urllib.parse.quote(str(shijian))

    for tries in range(maxTryNum):
            try:
                res_data = urllib.request.urlopen(url,timeout=35)
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    print("��������ϲ�޷�����")
                    break

    
    res = res_data.read()
    huifu=res.decode('utf-8')
    print(huifu)


    

zhiling=input('������ָ��:��1����������������ͼ����2�������ϴ����ݣ����������ݺͻ�ͼ:')
if zhiling=='1':
     duqu2()


if zhiling=='2':
     charu()
     duqu()
     duqu2()












