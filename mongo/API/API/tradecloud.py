#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from PIL import Image, ImageTk  
import flask
import http.client
import hashlib,csv,datetime,time
import urllib,json
import random
import urllib.request
import requests
from flask_httpauth import HTTPBasicAuth
import tkinter as tk
from tkinter import ttk
from tkinter import *
import urllib.parse
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15) #用于在散点图中输出中文
maxTryNum=20


global huifu,guanggaoshu,len0,piaofen2

username='miguel'
password0 ='python'
url0='http://139.196.79.93:90/'
password = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password.add_password(None,url0,username,password0)
handler=urllib.request.HTTPBasicAuthHandler(password)
opener = urllib.request.build_opener(handler)  
urllib.request.install_opener(opener)
huifu=''
ggg='67312'
def fasong():

    global guanggaoshu,len0,piaofen2,shijian2
    shijian2=time.strftime('%H:%M',time.localtime(time.time()))
    caozuo='发送广告'
    url = url0+'2?jigou='+urllib.parse.quote(str(jigou.get()))+'&lianxi='+urllib.parse.quote(str(lianxi.get()))+'&beizhu='+urllib.parse.quote(str(beizhu.get()))+'&qixian='+urllib.parse.quote(str(qixian.get()))+'&leixing='+urllib.parse.quote(str(leixing.get()))+'&ggg='+urllib.parse.quote(ggg)+'&caozuo='+urllib.parse.quote(caozuo)
    print(url)
    guanggaoshu=20
    if jigou.get()=='':
        bbb0=("%s  请输入所在银行~"%shijian2)
        leb_yewu1.config(text=bbb0)
        return
    else:
            if lianxi.get()=='':
              bbb0=('%s  请输入联系方式~'%shijian2)
              leb_yewu1.config(text=bbb0)
              return
    for tries in range(maxTryNum):
            try:
                res_data = urllib.request.urlopen(url,timeout=15)
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    bbb0=("%s  您的网络较差，无法连接"%shijian2)
                    leb_yewu1.config(text=bbb0)
                    break

    res = res_data.read()
    piaofen2=res.decode('utf-8')
    if piaofen2=='999':
            bbb0='%s  暂无对应广告，请稍后再试。'%shijian2
            leb_yewu1.config(text=bbb0)
            return
    piaofen2= pd.read_json(piaofen2,typ='frame')  #方法二
    a=len(piaofen2)
    len0=min(a,guanggaoshu)
    piaofen2= piaofen2.sort_index(ascending=False)

    piaofen2=piaofen2[['time','time2','content']][:len0]
    piaofen2 = piaofen2.reset_index(drop=True)    #重新定义索引
    for i in range(0,len0):
          piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\r','；')

    clickMe2()

def liulan():

    global guanggaoshu,len0,piaofen2,shijian2
    shijian2=time.strftime('%H:%M',time.localtime(time.time()))
    guanggaoshu=10
    caozuo='浏览广告'
    url = url0+'2?jigou='+urllib.parse.quote(str(jigou.get()))+'&lianxi='+urllib.parse.quote(str(lianxi.get()))+'&beizhu='+urllib.parse.quote(str(beizhu.get()))+'&qixian='+urllib.parse.quote(str(qixian.get()))+'&leixing='+urllib.parse.quote(str(leixing.get()))+'&ggg='+urllib.parse.quote(ggg)+'&caozuo='+urllib.parse.quote(caozuo)
    print(url)
    for tries in range(maxTryNum):
            try:
                res_data = urllib.request.urlopen(url,timeout=15)
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    bbb0=("%s  您的网络较差，无法连接"%shijian2)
                    leb_yewu1.config(text=bbb0)
                    break
    res = res_data.read()
    piaofen2=res.decode('utf-8')
    if piaofen2=='999':
            bbb0='%s  暂无对应广告，请稍后再试。'%shijian2
            leb_yewu1.config(text=bbb0)
            return
    piaofen2= pd.read_json(piaofen2,typ='frame')  #方法二
    a=len(piaofen2)
    len0=min(a,guanggaoshu)
    print(len0)
    piaofen2= piaofen2.sort_index(ascending=False)

    piaofen2=piaofen2[['time','time2','content']][:len0]
    piaofen2 = piaofen2.reset_index(drop=True)    #重新定义索引
    for i in range(0,len0):
          piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\r','；')

    clickMe2()
    
def clickMe2():   # 业务撮合
    global huifu,guanggaoshu,len0,piaofen2,shijian2
    if leixing.get()=='票据买断':
          piaofen2.to_csv('票据卖断广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))

    if leixing.get()=='票据卖断':
          
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('票据买断广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))
    elif leixing.get()=='票据收买返':
          
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('票据出回购广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))
    elif leixing.get()=='票据出回购':
          
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('票据收回购广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))

    elif leixing.get()=='票据收代持':
          
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('票据出代持广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))

    elif leixing.get()=='票据出代持':
          
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('票据收代持广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))

    elif leixing.get()=='收证':
         
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('出证广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))
    elif leixing.get()=='出证':
          
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('收证广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))
    elif leixing.get()=='收理财':
         
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('出理财广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))
    elif leixing.get()=='出理财':
         
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('收理财广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))
    elif leixing.get()=='收存单':
          
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('出存单广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))

    elif leixing.get()=='出存单':
          
          for i in range(0,len0):
              piaofen2.ix[i,'content']=piaofen2.ix[i,'content'].replace('\n','；')
          piaofen2.to_csv('收存单广告.csv',encoding='GB18030',mode='w',header=True)
          bbb0=('%s  已导出%s条广告~，请在文件夹中查看'%(shijian2,len0))


    leb_yewu1.config(text=bbb0)



def clickMe1():   # 当acction被点击时,该函数则生效
    global piaofen_df
    piaofen_df.to_csv('原始数据.csv',encoding='GB18030',mode='w',header=True)



def go(*args):   #处理事件，*args表示可变参数  
    print(numberChosen.get()) #打印选中的值

#以不同的颜色区别各个frame  

def clickMe3():
  caozuo='检索资讯'
  shijian2=time.strftime('%H:%M',time.localtime(time.time()))
  if guanjianci.get()=='':
    ccc0='%s  请输入要检索的关键词'%shijian2
    leb_zixun1.config(text=ccc0)
    return
  uget=urllib.parse.quote(str(guanjianci.get()))
  print(uget)
  url = url0+'14?jiansuoci='+uget+'&mubiao='+urllib.parse.quote(str(mubiao.get()))+'&ggg='+urllib.parse.quote(ggg)+'&caozuo='+urllib.parse.quote(caozuo)
  print(url)
  for tries in range(maxTryNum):
            try:
                res_data = urllib.request.urlopen(url,timeout=15)
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    ccc0=("%s  您的网络较差，无法连接"%shijian2)
                    leb_zixun1.config(text=ccc0)
                    break
  res = res_data.read()
  piaofen_df=res.decode('utf-8')

  if mubiao.get()=='标题':
         if piaofen_df=='999':
            ccc0=('%s  未在“标题”中检索到资讯。'%shijian2)
            leb_zixun1.config(text=ccc0)
            return          
         piaofen_df= pd.read_json(piaofen_df,typ='frame')  #方法二
         piaofen_df.to_csv('资讯-标题.csv',encoding='GB18030',mode='w',header=True)
         ccc0='%s  已找到%s条资讯~，请在文件夹中查看'%(shijian2,len(piaofen_df))
    
  elif mubiao.get()=='内容':         
         if piaofen_df=='999':
            ccc0=('%s  未在“内容”中检索到资讯。'%shijian2)
            leb_zixun1.config(text=ccc0)
            return          
         piaofen_df= pd.read_json(piaofen_df,typ='frame')  #方法二
         piaofen_df.to_csv('资讯-全文.csv',encoding='GB18030',mode='w',header=True)
         ccc0='%s  已找到%s条资讯~，请在文件夹中查看'%(shijian2,len(piaofen_df))
  leb_zixun1.config(text=ccc0)

    

# button被点击之后会被执行
def clickMe():   # 当acction被点击时,该函数则生效
  caozuo='市场分析'
  shijian2=time.strftime('%H:%M',time.localtime(time.time()))

  action1.configure()      # 将按钮设置为灰色状态，不可使用状态
  global img,piaofen_df
  shijian=time.strftime('%Y-%m-%d',time.localtime(time.time()))
  url = url0+'1?yewu='+urllib.parse.quote(str(yewu.get()))+'&ggg='+urllib.parse.quote(ggg)+'&caozuo='+urllib.parse.quote(caozuo)

  print(url)
  for tries in range(maxTryNum):
            try:
                res_data = urllib.request.urlopen(url,timeout=15)
                break
            except:
                if tries < (maxTryNum - 1):
                    print(tries)
                    continue
                else:
                    aaa=("%s 您的网络较差，无法连接"%shijian2)
                    leb2.config(text=aaa,justify = 'left')  #左对齐

                    break
  res = res_data.read()
  piaofen_df=res.decode('utf-8')

          
  if piaofen_df=='999'  :
            aaa=('%s暂无当日数据，请稍后再试。'%shijian2)
            leb2.config(text=aaa,justify = 'left')  #左对齐
            return
          
  piaofen_df= pd.read_json(piaofen_df,typ='frame')  #方法二
  if(len(piaofen_df[piaofen_df['hanglei2']==1])==0):
       aaa=('%s暂无当日数据，请稍后再试。'%shijian2)
       leb2.config(text=aaa,justify = 'left')  #左对齐
       return
#1.制作表格


#一、票据  
  if yewu.get()=='票据':
          huatudata3=piaofen_df[['hanglei1','hanglei2','shou','chu','shoudai','chudai']]
          huatudata5=huatudata3.groupby(['hanglei2']).sum()
          shouchubi=round(huatudata5.ix[1,'shou']/(huatudata5.ix[1,'chu']+0.0001),2)            
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shou': '收', 'chu': '出', 'shoudai': '收代持', 'chudai': '出代持'})         
          huatuhui=('    %s银行收票数为%s，出票数为%s，\n收票/出票为%s。\n以下为具体广告计数（已排除重复广告）。\n\n机构  收票  出票  收代持  出代持'%(shijian2,huatudata5.ix[1,'shou'],huatudata5.ix[1,'chu'],shouchubi)     )
          for i in range(0,len(huatudata4)):
                huatuhui0=('%s      %s      %s      %s      %s'%(huatudata4.ix[i,'机构'],huatudata4.ix[i,'收'],huatudata4.ix[i,'出'],huatudata4.ix[i,'收代持'],huatudata4.ix[i,'出代持']))
                huatuhui=('%s\n%s'%(huatuhui,huatuhui0))               
          aaa=huatuhui

         
#2.画图
          l2 = [-0.5,0.5,1.5]
          huatudata2=piaofen_df.groupby(['hanglei2']).cumsum(0)
          huatudata=piaofen_df[['hanglei2']]
          result = pd.concat([huatudata2, huatudata], axis=1)
          plt.scatter(y=result['shou'],x=result['chu'],c=result['hanglei2'],marker ='+',label='每个点代表当前时点的\n累积收票和卖票数\n黄色为银行，紫色为中介',edgecolors='face',s=20)  #制作散点图
          plt.legend(prop=font_set,fontsize=10)  #显示lable
          plt.xlabel(u'卖票计数',fontproperties=font_set)
          plt.ylabel(u'收票计数',fontproperties=font_set)
          plt.title('%s  微信群广告统计'%(shijian), fontproperties=font_set)
          plt.savefig('市场收票卖票比.png')
#3.显示导出按钮
          actiondao = ttk.Button(win, text="导出当日银行原始数据", command=clickMe1)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
          actiondao.grid(column=1, row=40)    # 设置其在界面中出现的位置  column代表列   row 代表行
          actiondao['state'] = 'disabled'





          

#二、福费廷  

  if yewu.get()=='福费廷':

#1.制作表格

          huatudata3=piaofen_df[['hanglei1','hanglei2','shoufu','chufu']]
          huatudata5=huatudata3.groupby(['hanglei2']).sum()
          shouchubi=round(huatudata5.ix[1,'shoufu']/(huatudata5.ix[1,'chufu']+0.0001),2)            
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shoufu': '收', 'chufu': '出'})         
          huatuhui=('    %s银行收福费廷数为%s，出福费廷数为%s，\n收福费廷/出福费廷为%s。\n以下为具体广告计数（已排除重复广告）。\n\n机构  收福费廷  出福费廷'%(shijian2,huatudata5.ix[1,'shoufu'],huatudata5.ix[1,'chufu'],shouchubi)     )
          for i in range(0,len(huatudata4)):
                huatuhui0=('%s      %s      %s '%(huatudata4.ix[i,'机构'],huatudata4.ix[i,'收'],huatudata4.ix[i,'出']))
                huatuhui=('%s\n%s'%(huatuhui,huatuhui0))               
          aaa=huatuhui


#三、存单  

  if yewu.get()=='存单':

#1.制作表格

          huatudata3=piaofen_df[['hanglei1','hanglei2','shoucun','chucun']]
          huatudata5=huatudata3.groupby(['hanglei2']).sum()
          shouchubi=round(huatudata5.ix[1,'shoucun']/(huatudata5.ix[1,'chucun']+0.0001),2)            
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shoucun': '收', 'chucun': '出'})         
          huatuhui=('    %s银行收存单数为%s，出存单数为%s，\n收存单/出存单为%s。\n以下为具体广告计数（已排除重复广告）。\n\n机构  收存单  出存单'%(shijian2,huatudata5.ix[1,'shoucun'],huatudata5.ix[1,'chucun'],shouchubi)     )
          for i in range(0,len(huatudata4)):
                huatuhui0=('%s      %s      %s '%(huatudata4.ix[i,'机构'],huatudata4.ix[i,'收'],huatudata4.ix[i,'出']))
                huatuhui=('%s\n%s'%(huatuhui,huatuhui0))               
          aaa=huatuhui

          

## 四、理财
  if yewu.get()=='理财':


#1.制作表格
          huatudata3=piaofen_df[['hanglei1','hanglei2','shouli','chuli']]
          huatudata5=huatudata3.groupby(['hanglei2']).sum()
          shouchubi=round(huatudata5.ix[1,'shouli']/(huatudata5.ix[1,'chuli']+0.0001),2)            
          huatudata4=huatudata3.groupby(['hanglei1']).sum()
          huatudata4=huatudata4.reset_index(drop = False)
          huatudata4=huatudata4.rename(columns={'hanglei1': '机构', 'shouli': '收', 'chuli': '出'})         
          huatuhui=('    %s银行收理财数为%s，出理财数为%s，\n收理财/出理财为%s。\n以下为具体广告计数（已排除重复广告）。\n\n机构  收理财  出理财'%(shijian2,huatudata5.ix[1,'shouli'],huatudata5.ix[1,'chuli'],shouchubi)     )
          for i in range(0,len(huatudata4)):
                huatuhui0=('%s      %s      %s '%(huatudata4.ix[i,'机构'],huatudata4.ix[i,'收'],huatudata4.ix[i,'出']))
                huatuhui=('%s\n%s'%(huatuhui,huatuhui0))               
          aaa=huatuhui


  leb2.config(text=aaa,justify = 'left')  #左对齐

 




win =Tk()


win.geometry("950x650")    # 设置窗口大小 注意：是x 不是*
win.resizable(width=True, height=True) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
win.title("交易云询价")    # 添加标题
win.top = win.winfo_toplevel()




#一、分析页面
Label(win, text="市场分析",font = ("黑体", 20, "bold"), fg='blue').grid(column=0, row=0,rowspan=2, columnspan=2)      # 设置其在界面中出现的位置  column代表列   row 代表行


Label(win, text="选择日期", fg='blue').grid(column=0, row=2)      # 设置其在界面中出现的位置  column代表列   row 代表行
Label(win, text="选择业务类型(*)", fg='blue').grid(column=1, row=2)      # 设置其在界面中出现的位置  column代表列   row 代表行
leb2=Label(win, text='')

leb2.grid(row=9, column = 0, columnspan=2) #,rowspan=66, columnspan=2
piaofen_df=[]       



# 按钮
action1 =ttk.Button(win, text="数据分析", command=clickMe)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
#action1['background']='green'
action1.grid(column=1, row=5)    # 设置其在界面中出现的位置  column代表列   row 代表行

lebfen=Label(win, text='|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|')
lebfen.grid(row=0, column = 3,rowspan=80, columnspan=1)

lebfen=Label(win, text='|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|')
lebfen.grid(row=0, column = 8,rowspan=80, columnspan=1)


# 创建一个日期下拉列表
date = tk.StringVar()
numberChosen = ttk.Combobox(win, width=12, textvariable=date)
numberChosen['values'] = ('今天')     # 设置下拉列表的值
numberChosen.grid(column=0, row=3)      # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

# 创建一个业务类型下拉列表
yewu = tk.StringVar()
numberChosen = ttk.Combobox(win, width=12, textvariable=yewu)
numberChosen['values'] = ('票据','福费廷','存单','理财')     # 设置下拉列表的值
numberChosen.grid(column=1, row=3)      # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
numberChosen.bind("<<ComboboxSelected>>",go)  #绑定事件,(下拉列表框被选中时，绑定go()函数)  




#二、业务页面
Label(win, text="业务撮合",font = ("黑体", 20, "bold"), fg='green').grid(column=4, row=0,rowspan=2, columnspan=4)      # 设置其在界面中出现的位置  column代表列   row 代表行


shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
shijian0=shijian11-datetime.timedelta(days=1)
shijian01=shijian11-datetime.timedelta(days=2)
shijian02=shijian11-datetime.timedelta(days=3)
shijian11=shijian11.strftime("%Y-%m-%d")  
shijian0=shijian0.strftime("%Y-%m-%d")
shijian01=shijian01.strftime("%Y-%m-%d")  
shijian02=shijian02.strftime("%Y-%m-%d")  
# 创建一个日期下拉列表
Label(win, text="业务类型(*)",fg='green').grid(column=4, row=2)   
leixing = tk.StringVar()
boxlist = ttk.Combobox(win, width=12, textvariable=leixing)
boxlist ['values'] = ('票据买断','票据卖断','票据收买返','票据出回购','票据收代持','票据出代持','收福费廷','出福费廷','收存单','出存单')     # 设置下拉列表的值
boxlist .grid(column=4, row=3)      # 设置其在界面中出现的位置  column代表列   row 代表行
boxlist .current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值




Label(win, text="机构(*)",fg='green') .grid(column=5, row=2)
jigou = StringVar()  
jigou_e = Entry(win, textvariable=jigou, width=12)  
jigou_e .grid(column=5, row=3)      # 设置其在界面中出现的位置  column代表列   row 代表行
lianxi= StringVar()  
Label(win, text="联系方式(*)",fg='green') .grid(column=6, row=2)  
lianxi_e = Entry(win, textvariable=lianxi, width=12)  
lianxi_e.grid(column=6, row=3)      # 设置其在界面中出现的位置  column代表列   row 代表行
Label(win, text="期限",fg='green').grid(column=7, row=2)   
qixian = tk.StringVar()
boxlist1 = ttk.Combobox(win, width=12, textvariable=qixian)
boxlist1 ['values'] = ('不限','1M以内','1-3M','3-6M','6-12M')     # 设置下拉列表的值
boxlist1 .grid(column=7, row=3)      # 设置其在界面中出现的位置  column代表列   row 代表行
boxlist1 .current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
beizhu= StringVar()  
Label(win, text="备注(可附加任何内容，如价格、承兑行等)",fg='green') .grid(column=4, row=4, columnspan=2)  
beizhu_e = Entry(win, textvariable=beizhu, width=28)  
beizhu_e.grid(column=4, row=5,rowspan=1, columnspan=2)      # 设置其在界面中出现的位置  column代表列   row 代表行

actiondao1 = ttk.Button(win, text="导出并发送广告", command=fasong)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
actiondao1.grid(column=6, row=5)    # 设置其在界面中出现的位置  column代表列   row 代表行
#actiondao1['state'] = 'disabled'

actiondao2 = ttk.Button(win, text="导出", command=liulan)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
actiondao2.grid(column=7, row=5)    # 设置其在界面中出现的位置  column代表列   row 代表行
leb_yewu1=Label(win, text='')
leb_yewu1.grid(row=9, column = 4,columnspan=4)



#三、资讯页面

Label(win, text="资讯搜索",font = ("黑体", 20, "bold"), fg='purple').grid(column=9, row=0,rowspan=2, columnspan=5)      # 设置其在界面中出现的位置  column代表列   row 代表行
Label(win, text="起始时间(*)", fg='purple').grid(column=9, row=2)   
sousuoshijian = tk.StringVar()
boxlist1 = ttk.Combobox(win, width=12, textvariable=sousuoshijian)
boxlist1 ['values'] = ('30天以内')     # 设置下拉列表的值
boxlist1 .current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
boxlist1 .grid(column=9, row=3)      # 设置其在界面中出现的位置  column代表列   row 代表行
Label(win, text="搜索目标(*)", fg='purple').grid(column=10, row=2)   
mubiao = tk.StringVar()
boxlist1 = ttk.Combobox(win, width=12, textvariable=mubiao)
boxlist1 ['values'] = ('标题','全文')     # 设置下拉列表的值
boxlist1 .grid(column=10, row=3)      # 设置其在界面中出现的位置  column代表列   row 代表行
boxlist1 .current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

actionsou = ttk.Button(win, text="搜索", command=clickMe3)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
actionsou.grid(column=10, row=5)    # 设置其在界面中出现的位置  column代表列   row 代表行
#leb_yewu1=Label(win, text='')
#leb_yewu1.grid(row=9, column = 4,columnspan=4)

guanjianci= StringVar()  
Label(win, text="检索词(*)", fg='purple') .grid(column=9, row=4)  
beizhu_e = Entry(win, textvariable=guanjianci)  
beizhu_e.grid(column=9, row=5,rowspan=1, columnspan=1)
leb_zixun1=Label(win, text='')
leb_zixun1.grid(row=9, column = 9,columnspan=4)





win.mainloop()      # 当调用mainloop()时,窗口才会显示出来


