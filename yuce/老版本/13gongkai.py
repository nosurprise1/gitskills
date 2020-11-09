from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import re,datetime,json,time
from pymongo import MongoClient

client=MongoClient('mongodb://root:' + '5768116' + '@121.196.220.14')
shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))






#lianjiez=''
chrome_options = Options()
# 无头模式启动
chrome_options.add_argument('--headless')
# 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--disable-gpu')


def gongkai():
    print('开始执行公开操作爬取程序……')
    zhiling=input('    请输入指令“1”来确认执行：')
    if zhiling!='1':
       print('    终止。')
       return



    db = client.zixun
    collection = db.zixun
    cursor = collection.find({'权重':'央行政策'})
    zixun_df= pd.DataFrame(list(cursor))
    lianjiez=(zixun_df['链接'].tolist())

# 初始化实例
    driver= webdriver.Chrome(chrome_options=chrome_options)
    time.sleep(2) 
# 请求百度

    es=driver.get("http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/index.html")
    d=driver.find_elements_by_xpath('//td[@class="unline"]/a')
    e=driver.find_elements_by_xpath('//td[@class="unline"]')
    shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))


    for i in range(0,len(e)):
        cont=''
        biaotou=''
        biaonei=''
        lianjie=d[i].get_attribute('href')
        if lianjie  not in lianjiez:
           title=d[i].get_attribute('title')
           date=e[i].find_elements_by_xpath('.//following-sibling::span')[0].text
           time.sleep(2) 

           es2=driver.get(lianjie)
           t=driver.find_elements_by_xpath('.//div[@id="zoom"]')
           for i in t:
             string=re.split('\n',i.text)
             for i in range (1,len(string)):
               zhaop2=re.search('^((?!(MLF|二〇一八|。|，)).)*([\u4e00-\u9fa5]{0,4})(?:期限|名称|利率|量|日)',string[i])  #如11-12月
               if zhaop2:

                 biaotou=biaotou+'    '+string[i]

             
               zhaop2=re.search('([\d]{1,5}(?:天|年|亿元|%|日))',string[i])  #如11-12月
               if zhaop2:
                   biaonei=biaonei+'    '+string[i]

           time.sleep(2)
           driver.back()  # 从百度新闻后退到百度首页
           es=driver.get("http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/index.html")
           d=driver.find_elements_by_xpath('//td[@class="unline"]/a')
           e=driver.find_elements_by_xpath('//td[@class="unline"]')



           cont='    '+string[0]+'<br>'+biaotou+'<br>'+biaonei       
        
           gongkai=pd.DataFrame({'时间': [date],
                          '标题': [title],
                          '链接': [lianjie],
                          '内容':[cont],
                          '爬取日期':[shijian],
                          '权重':['央行政策'],
                          '序号':[''],
                          '网站':['人民银行'],
                          '国外':['']
                         })
           records = json.loads(gongkai.T.to_json()).values()
           collection.insert(records)


        else:
            print('已更新')
    print("Clean...")
    driver.close()
    driver.quit()


def waihui():
    print('开始执行外汇爬取程序……')
    zhiling=input('    请输入指令“1”来确认执行：')
    if zhiling!='1':
       print('    终止。')
       return


    
    driver= webdriver.Chrome(chrome_options=chrome_options)

    driver.get('https://finance.sina.com.cn/money/forex/hq/USDCNH.shtml')
    time.sleep(2)

    price_0 = driver.find_element_by_xpath("//div[@id='quoteWrap']")
    string=re.split('\n',price_0.text)
    
    print(string[2][:10])
    db2 = client.waihui
    collection2 = db2.waihui
    cursor = collection2.find({'日期':string[2][:10]})
    df3= pd.DataFrame(list(cursor))
    if df3.empty:
        waihui=pd.DataFrame({'日期': [string[2][:10]],
                          '现价': [string[0]],
                          '开盘': [string[4]],
                          '昨收':[string[6]],
                          '振幅':[string[8]],
                          '波幅':[string[10]],
                          '最低':[string[12]],
                          '最高':[string[14]]
                          })


        records = json.loads(waihui.T.to_json()).values()
        collection2.insert(records)

    else:
        print(df3)
        print('已经爬过')
    #baojia = '当前美元人民币离岸价为：'+price_0.text
    #print(baojia)
    driver.quit()
gongkai()
waihui()
