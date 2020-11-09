# -*- coding: cp936 -*-
import datetime,time
maxTryNum=20
import json,csv
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12) #用于在散点图中输出中文
font_set2 = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=9) #用于在散点图中输出中文


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
                    print("您的网络较差，无法连接")
                    break

    res = res_data.read()

    piaofen3=res.decode('utf-8')
    piaofen3= pd.read_json(piaofen3,typ='frame')  #方法二
    print(piaofen3)
    piaofen3=piaofen3[piaofen3['数据']=='当日']
    
    piaofen3['提取日期'] = pd.to_datetime(piaofen3['提取日期']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式

    piaofen3=piaofen3[piaofen3['提取日期']>='2018-08-01']
    piaofen3 = piaofen3.sort_values(by=['提取日期'], ascending=True)
    piaofen3= piaofen3.reset_index(drop=True)    #重新定义索引

    shijian=piaofen3.loc[(len(piaofen3)-1),'提取日期']
    
    piaofen3=piaofen3.set_index(['提取日期'])
    piaofen3=piaofen3[['承兑金额/亿元','贴现金额/亿元','交易金额/亿元']]
    
    piaofen4=piaofen3
    piaofen4['承兑/贴现']=piaofen4['承兑金额/亿元']/piaofen4['贴现金额/亿元']
    piaofen4['承兑/交易量']=piaofen4['承兑金额/亿元']/piaofen4['交易金额/亿元']

    y1=piaofen4['承兑/贴现'].tolist()
    y2=piaofen4['承兑/交易量'].tolist()

    
    piaofen3=piaofen3[['承兑金额/亿元','贴现金额/亿元','交易金额/亿元']]

    piaofen3.plot(kind='bar', alpha=0.4,stacked=False)
    plt.ylabel('发行量(亿元)',fontproperties=font_set)
    plt.xlabel('')
    plt.legend(prop=font_set2,loc='upper left')  #显示lable位置

    plt2=plt.twinx()
    plt2.plot(y1,alpha=0.7,label='承兑/贴现')
    plt2.plot(y2,alpha=0.7,label='承兑/交易量')

#第二纵坐标需要用set
    plt2.set_ylabel('承兑/贴现',fontproperties=font_set)

    plt2.legend(prop=font_set2,loc='upper center', bbox_to_anchor=(0.6,0.95))  #显示lable


    plt.title('%s票据交易量、承兑量、贴现量'%(shijian),fontproperties=font_set) 




    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('C:/Users/yangbing/wangye/wangye/static/images/piaojiaosuol.png') 
    fig.show()
    print('已导出交易量')











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
                    print("您的网络较差，无法连接")
                    break

    res = res_data.read()

    piaofen2=res.decode('utf-8')
    piaofen2= pd.read_json(piaofen2,typ='frame')  #方法二

    piaofen2['提取日期'] = pd.to_datetime(piaofen2['提取日期']).astype('str')   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    piaofen2 = piaofen2.sort_values(by=['提取日期'], ascending=True)
    piaofen2= piaofen2.reset_index(drop=True)    #重新定义索引
    print(piaofen2)
    
    shijian=piaofen2.loc[(len(piaofen2)-1),'提取日期']
    
    piaofen3=piaofen2.set_index(['提取日期'])

    
    piaofen3=piaofen3[(piaofen3['票据类型']=='电银')& (piaofen3['业务类型']=='买断式')]

    print(piaofen3)
  #  piaofen3['提取日期'] = pd.to_datetime(piaofen3['提取日期'])   #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式


    piaofen3=piaofen3[['1-3个月（含）','3-6个月（含）','9-12个月（含）']]
    piaofen3.plot()
    plt.xlabel('')


    plt.ylabel('利率(%)',fontproperties=font_set)
    plt.legend(prop=font_set)  #显示lable
    plt.title('%s各期限电票利率'%(shijian), fontproperties=font_set) 
    piaofen2.to_csv('piaoj.csv',mode='w',header=True)

    print('已导出加权利率')




    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
  #  plt.savefig('C:/Users/yangbing/wangye/wangye/static/images/piaojiaosuoli.png')
    fig =plt.gcf()
    fig.set_size_inches(9, 4)
    fig.savefig('C:/Users/Administrator/wangye/static/images/piaojiaosuoli.png')

    fig.show()



def charu():
    url='ee.csv'

    shuru1=input('请输入所提取的csv文件名（请确保在同一文件夹下，不输入则默认为“ee”）:')
    if shuru1!='':
        url=shuru1
    
    df = pd.read_table(url,sep=',',encoding='GB18030')   #用dictreader根据行内容查找


   # global shijian
    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))

    shijian = datetime.datetime.strptime(shijian, "%Y-%m-%d")
    shijian=shijian-datetime.timedelta(days=1)

    shijian=str(shijian.strftime("%Y-%m-%d"))

    shuru=input('请输入所提取数据的日期,格式为“2017-11-01”，不输入则默认为昨天:')
    if shuru!='':
        shijian=shuru
#提取买断式
    print(shijian)

    mai_yin=pd.DataFrame({'提取日期': [shijian],
                      '票据类型':['电银'],
                      '业务类型':['买断式'],
                    df.loc[0,'期限']: [df.loc[0,'银票加权利率%']],
                    df.loc[1,'期限']: [df.loc[1,'银票加权利率%']],
                    df.loc[2,'期限']: [df.loc[2,'银票加权利率%']],
                    df.loc[3,'期限']: [df.loc[3,'银票加权利率%']],
                    df.loc[4,'期限']: [df.loc[4,'银票加权利率%']],
                    df.loc[5,'期限']: [df.loc[5,'银票加权利率%']]

                         })
    mai_shang=pd.DataFrame({'提取日期': [shijian],
                      '票据类型':['电商'],
                      '业务类型':['买断式'],

                    df.loc[0,'期限']: [df.loc[0,'商票加权利率%']],
                    df.loc[1,'期限']: [df.loc[1,'商票加权利率%']],
                    df.loc[2,'期限']: [df.loc[2,'商票加权利率%']],
                    df.loc[3,'期限']: [df.loc[3,'商票加权利率%']],
                    df.loc[4,'期限']: [df.loc[4,'商票加权利率%']],
                    df.loc[5,'期限']: [df.loc[5,'商票加权利率%']]
                         })

#提取质押式
    hui_yin=pd.DataFrame({'提取日期': [shijian],
                      '票据类型':['电银'],
                      '业务类型':['回购式'],

                    df.loc[0,'期限.1']: [df.loc[0,'银票加权利率%.1']],
                    df.loc[1,'期限.1']: [df.loc[1,'银票加权利率%.1']],
                    df.loc[2,'期限.1']: [df.loc[2,'银票加权利率%.1']],
                    df.loc[3,'期限.1']: [df.loc[3,'银票加权利率%.1']],
                    df.loc[4,'期限.1']: [df.loc[4,'银票加权利率%.1']],
                    df.loc[5,'期限.1']: [df.loc[5,'银票加权利率%.1']]
                         })
    hui_shang=pd.DataFrame({'提取日期': [shijian],
                      '票据类型':['电商'],
                      '业务类型':['回购式'],

                    df.loc[0,'期限.1']: [df.loc[0,'商票加权利率%.1']],
                    df.loc[1,'期限.1']: [df.loc[1,'商票加权利率%.1']],
                    df.loc[2,'期限.1']: [df.loc[2,'商票加权利率%.1']],
                    df.loc[3,'期限.1']: [df.loc[3,'商票加权利率%.1']],
                    df.loc[4,'期限.1']: [df.loc[4,'商票加权利率%.1']],
                    df.loc[5,'期限.1']: [df.loc[5,'商票加权利率%.1']]
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
                    print("您的网络较差，无法连接")
                    break

    
    res = res_data.read()
    huifu=res.decode('utf-8')
    print(huifu)


    

zhiling=input('请输入指令:“1”——仅更新数据图；“2”——上传数据，并更新数据和画图:')
if zhiling=='1':
     duqu2()


if zhiling=='2':
     charu()
     duqu()
     duqu2()












