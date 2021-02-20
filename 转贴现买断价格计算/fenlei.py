import csv,xlrd,xlwt,datetime,time
import pandas as pd

shouxin=pd.read_excel('授信客户.xls')#,encoding='GB18030')
shouxin=shouxin[['客户名称','客户状态','额度到期日']]
#shouxin['客户名称']=shouxin['客户名称'].str.replace('股份有限公司','')
dict_shouxin = shouxin.set_index('客户名称').T.to_dict('list')


#四、导入价格表
jiage=pd.read_excel('jiage.xls')#,encoding='GB18030')
print(jiage)


#二、输入客户名单
fenlei=pd.read_excel('分类.xls')#,encoding='GB18030')
#for i in range(0,len(fenlei)):
#  for j in range(0,len(shouxin)):
#    if str(fenlei.loc[i,'银行类型']) in str(shouxin.loc[j,'客户名称']):
#               print(str(shouxin.loc[j,'客户名称']))
#               fenlei.loc[i,'授信表银行名字']=shouxin.loc[j,'客户名称']
#fenlei.to_excel('33.xls')





#三、匹配授信有效期限
for i in range(0,len(fenlei)):
  if fenlei.loc[i,'授信表银行名字'] in dict_shouxin:
              
               fenlei.loc[i,'授信有效']=dict_shouxin.get(fenlei.loc[i,'授信表银行名字'])[0]
               fenlei.loc[i,'到期日']=dict_shouxin.get(fenlei.loc[i,'授信表银行名字'])[1]
print(fenlei)





def suanqingdan():
    suanqingdan=0
    global url,qing,qing2,shijian0
    jin=input('请输入交易类型，1.买断；2.回购或卖断:')
    if jin=='1':
        
        jia_df=pd.read_excel('jiage.xls')#,encoding='GB18030')
        jia_df=jia_df.set_index('银行分类')
        columns=jia_df.columns.values.tolist()  #取表格中某一行作为columns的名字，千万不要用[1:1]的写法
        

        
    else:
        jia_df=pd.read_excel('转贴现买断价格计算/jia_hui.xls',encoding='GB18030')
     
    shijian0=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    shijian=datetime.datetime.strptime(shijian0 , "%Y-%m-%d")#转为日期格式

#2.1输入交易日
    jin=input('请输入要交易日,输入格式为“2017-11-01”，不输入默认为今天:')
    if jin!='':
        shijian=datetime.datetime.strptime(jin , "%Y-%m-%d")

#2.2确认列名，到时候可以删除
    qing=pd.read_excel(url)
#二、换列标题
    qingcolumn=qing.columns.values.tolist()  
    qingcolumn_df=pd.read_excel('转贴现买断价格计算/lieming.csv',encoding='GB18030')
    for i in range(0,len(qingcolumn)):
        for j in range(0,len(qingcolumn_df)):
            zhaop2= re.search(qingcolumn_df.loc[j,'原列名'] ,qingcolumn[i])
 

            if zhaop2:
                qing.rename(columns={qingcolumn[i]:qingcolumn_df.loc[j,'新列名']}, inplace=True)
                break

    if '贴现行' not in qing.columns.values.tolist():
        qing['贴现行']=''


#三、筛选列，计算清单
    qing=qing[['票号','票面金额','出票人','承兑行','贴现行','出票日','到期日']]
    qing= qing.reset_index(drop=True)    #重新定义索引
    for i in range(0,len(qing)):
        qing.loc[i,'承兑行号']=str(qing.loc[i,'票号'])[1:13]
        
        
    qing['到期日2'] = pd.to_datetime(qing['到期日'])   #把str转化为时间格式，format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式
    
    qing= qing.reset_index(drop=True)    #重新定义索引
    qing['承兑行号']=qing['承兑行号'].astype(str)
    
  #  qing['出票日']=qing['出票日'].astype(str)
    qing['出票日'] = pd.to_datetime(qing['出票日']).astype(str)   #把str转化为时间格式，format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式    
    qing['到期日'] = pd.to_datetime(qing['到期日']).astype(str)   #把str转化为时间格式，format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式    
    qing['到期日2'] = pd.to_datetime(qing['到期日'])   #把str转化为时间格式，format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式


    

    for i in range(0,len(qing)):
         for j in range(0,len(fenlei)):
              if fenlei.loc[j,'银行类型']  in qing.loc[i,'承兑行']:
                    qing.log[i,'银行分类']==fenlei.loc[j,'银行分类']
                    qing.loc[i,'银行分类2']==fenlei.loc[j,'银行类型']
                    qing.loc[i,'交易日']=str(shijian)
                    break
         for z in range (0,len(columns)):
              qixian=columns[z].split('至')
              qixian[0] = datetime.datetime.strptime(qixian1[0] , "%Y-%m-%d")
              qixian[1] = datetime.datetime.strptime(qixian1[1] , "%Y-%m-%d")
              if  (qing.loc[i,'到期日2']>=qixian2[0]) and (qing.loc[i,'到期日2']<=qixian2[1]) :
                    print(columns[z])
                    qing.loc[i,'邮储指导价']=jia.loc[qing.log[i,'银行分类'],columns[z]]
                    break
    print(qing)
    s

    for i in range (0,len(columns)):     
         if (qing.loc[i,'到期日2']>=qixian1[0]) and (qing.loc[i,'到期日2']<=qixian1[1]) :
           for j in range (0,len(jia_df)):
               if (jia_df.loc[j,'银行类型'] in qing.loc[i,'承兑行']) and (float(jia_df.loc[j,jia_df.columns[2]])>=1) :
                   if (qing.loc[i,'票面金额']<1000000) and (qing.loc[i,'票面金额']>=500000):
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[2]]+0.10
                       qing.loc[i,'小票票据']=1
                   elif qing.loc[i,'票面金额']<500000:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[2]]+0.15
                       qing.loc[i,'小票票据']=2
                   else:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[2]]
                       qing.loc[i,'小票票据']=0
                    

                   qing.loc[i,'指导期限']=jia_df.columns[2]
                   qing.loc[i,'银行分类']=jia_df.loc[j,'银行分类']
                   qing.loc[i,'银行分类2']=jia_df.loc[j,'银行类型']

                   qing.loc[i,'交易日']=str(shijian)
                   qing.loc[i,'交易日']=qing.loc[i,'交易日'].replace(' 00:00:00','')
                   qing.loc[i,'出票日']=qing.loc[i,'出票日'].replace(' 00:00:00','')
                   qing.loc[i,'到期日']=qing.loc[i,'到期日'].replace(' 00:00:00','')
                   qing.loc[i,'到期月']=qing.loc[i,'到期日'][:(len(qing.loc[i,'到期日'])-3)]

                   qing.loc[i,'承兑行号']=qing.loc[i,'承兑行号'].replace('.0','')

                   shijiancha=str(qing.loc[i,'到期日2']-shijian) #转化为str
                   shijiancha=int(shijiancha.replace(' days 00:00:00',''))  #转化为int
                   qing.loc[i,'期限']=shijiancha
                   qing.loc[i,'ji1']=shijiancha*qing.loc[i,'票面金额']
                   qing.loc[i,'ji2']=shijiancha*qing.loc[i,'票面金额']*qing.loc[i,'邮储指导价']
                   qing.loc[i,'可用额度']=jia_df.loc[j,'可用额度']
                   qing.loc[i,'生效截至日']=jia_df.loc[j,'生效截至日']
                   qing.loc[i,'授信有效']=jia_df.loc[j,'授信有效']
                   qing.loc[i,'我行评级']=jia_df.loc[j,'我行评级']
                   suanqingdan=suanqingdan+1

         elif (qing.loc[i,'到期日2']>=qixian2[0]) and (qing.loc[i,'到期日2']<=qixian2[1]) :

           for j in range (0,len(jia_df)):

               if jia_df.loc[j,'银行类型'] in qing.loc[i,'承兑行']    and (float(jia_df.loc[j,jia_df.columns[3]])>=1) :
                   if (qing.loc[i,'票面金额']<1000000) and (qing.loc[i,'票面金额']>=500000):
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[3]]+0.10
                       qing.loc[i,'小票票据']=1
                   elif qing.loc[i,'票面金额']<500000:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[3]]+0.15
                       qing.loc[i,'小票票据']=2
                   else:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[3]]
                       qing.loc[i,'小票票据']=0
                    
                   qing.loc[i,'指导期限']=jia_df.columns[3]
                   qing.loc[i,'银行分类']=jia_df.loc[j,'银行分类']
                   qing.loc[i,'银行分类2']=jia_df.loc[j,'银行类型']

                   qing.loc[i,'交易日']=str(shijian)
                   qing.loc[i,'交易日']=qing.loc[i,'交易日'].replace(' 00:00:00','')
                   qing.loc[i,'出票日']=qing.loc[i,'出票日'].replace(' 00:00:00','')
                   qing.loc[i,'到期日']=qing.loc[i,'到期日'].replace(' 00:00:00','')
                   qing.loc[i,'到期月']=qing.loc[i,'到期日'][:(len(qing.loc[i,'到期日'])-3)]
                   qing.loc[i,'承兑行号']=qing.loc[i,'承兑行号'].replace('.0','')
                   shijiancha=str(qing.loc[i,'到期日2']-shijian) #转化为str
                   shijiancha=int(shijiancha.replace(' days 00:00:00',''))  #转化为int
                   qing.loc[i,'期限']=shijiancha
                   qing.loc[i,'ji1']=shijiancha*qing.loc[i,'票面金额']
                   qing.loc[i,'ji2']=shijiancha*qing.loc[i,'票面金额']*qing.loc[i,'邮储指导价']
                   qing.loc[i,'可用额度']=jia_df.loc[j,'可用额度']
                   qing.loc[i,'生效截至日']=jia_df.loc[j,'生效截至日']
                   qing.loc[i,'授信有效']=jia_df.loc[j,'授信有效']
                   qing.loc[i,'我行评级']=jia_df.loc[j,'我行评级']
                   suanqingdan=suanqingdan+1

         elif (qing.loc[i,'到期日2']>=qixian3[0]) and (qing.loc[i,'到期日2']<=qixian3[1])  :  #

           for j in range (0,len(jia_df)):
               if jia_df.loc[j,'银行类型'] in qing.loc[i,'承兑行']  and (float(jia_df.loc[j,jia_df.columns[4]])>=1):
                   if (qing.loc[i,'票面金额']<1000000) and (qing.loc[i,'票面金额']>=500000):
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[4]]+0.10
                       qing.loc[i,'小票票据']=1
                   elif qing.loc[i,'票面金额']<500000:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[4]]+0.15
                       qing.loc[i,'小票票据']=2
                   else:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[4]]
                       qing.loc[i,'小票票据']=0

                   qing.loc[i,'指导期限']=jia_df.columns[4]
                   qing.loc[i,'银行分类']=jia_df.loc[j,'银行分类']
                   qing.loc[i,'银行分类2']=jia_df.loc[j,'银行类型']

                   qing.loc[i,'交易日']=str(shijian)
                   qing.loc[i,'交易日']=qing.loc[i,'交易日'].replace(' 00:00:00','')
                   qing.loc[i,'出票日']=qing.loc[i,'出票日'].replace(' 00:00:00','')
                   qing.loc[i,'到期日']=qing.loc[i,'到期日'].replace(' 00:00:00','')
                   qing.loc[i,'到期月']=qing.loc[i,'到期日'][:(len(qing.loc[i,'到期日'])-3)]

                   qing.loc[i,'承兑行号']=qing.loc[i,'承兑行号'].replace('.0','')
               
                   shijiancha=str(qing.loc[i,'到期日2']-shijian) #转化为str
                   shijiancha=int(shijiancha.replace(' days 00:00:00',''))  #转化为int
                   qing.loc[i,'期限']=shijiancha
                   qing.loc[i,'ji1']=shijiancha*qing.loc[i,'票面金额']
                   qing.loc[i,'ji2']=shijiancha*qing.loc[i,'票面金额']*qing.loc[i,'邮储指导价']
                   qing.loc[i,'可用额度']=jia_df.loc[j,'可用额度']
                   qing.loc[i,'生效截至日']=jia_df.loc[j,'生效截至日']
                   qing.loc[i,'授信有效']=jia_df.loc[j,'授信有效']
                   qing.loc[i,'我行评级']=jia_df.loc[j,'我行评级']
                   suanqingdan=suanqingdan+1

         elif (qing.loc[i,'到期日2']>=qixian4[0]) and (qing.loc[i,'到期日2']<=qixian4[1])  :

           for j in range (0,len(jia_df)) :
               if jia_df.loc[j,'银行类型'] in qing.loc[i,'承兑行'] and (float(jia_df.loc[j,jia_df.columns[5]])>=1):
                   if (qing.loc[i,'票面金额']<1000000) and (qing.loc[i,'票面金额']>=500000):
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[5]]+0.10
                       qing.loc[i,'小票票据']=1
                   elif qing.loc[i,'票面金额']<500000:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[5]]+0.15
                       qing.loc[i,'小票票据']=2
                   else:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[5]]
                       qing.loc[i,'小票票据']=0
                   qing.loc[i,'指导期限']=jia_df.columns[5]
                   qing.loc[i,'银行分类']=jia_df.loc[j,'银行分类']
                   qing.loc[i,'银行分类2']=jia_df.loc[j,'银行类型']

                   qing.loc[i,'交易日']=str(shijian)
                   qing.loc[i,'交易日']=qing.loc[i,'交易日'].replace(' 00:00:00','')
                   qing.loc[i,'出票日']=qing.loc[i,'出票日'].replace(' 00:00:00','')
                   qing.loc[i,'到期日']=qing.loc[i,'到期日'].replace(' 00:00:00','')
                   qing.loc[i,'到期月']=qing.loc[i,'到期日'][:(len(qing.loc[i,'到期日'])-3)]

                   qing.loc[i,'承兑行号']=qing.loc[i,'承兑行号'].replace('.0','')
               
                   shijiancha=str(qing.loc[i,'到期日2']-shijian) #转化为str
                   shijiancha=int(shijiancha.replace(' days 00:00:00',''))  #转化为int
                   qing.loc[i,'期限']=shijiancha
                   qing.loc[i,'ji1']=shijiancha*qing.loc[i,'票面金额']
                   qing.loc[i,'ji2']=shijiancha*qing.loc[i,'票面金额']*qing.loc[i,'邮储指导价']
                   qing.loc[i,'可用额度']=jia_df.loc[j,'可用额度']
                   qing.loc[i,'生效截至日']=jia_df.loc[j,'生效截至日']
                   qing.loc[i,'授信有效']=jia_df.loc[j,'授信有效']
                   qing.loc[i,'我行评级']=jia_df.loc[j,'我行评级']
                   suanqingdan=suanqingdan+1




         elif (qing.loc[i,'到期日2']>=qixian5[0]) and (qing.loc[i,'到期日2']<=qixian5[1])  :

           for j in range (0,len(jia_df)) :
               if jia_df.loc[j,'银行类型'] in qing.loc[i,'承兑行'] and (float(jia_df.loc[j,jia_df.columns[6]])>=1):
                   if (qing.loc[i,'票面金额']<1000000) and (qing.loc[i,'票面金额']>=500000):
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[6]]+0.10
                       qing.loc[i,'小票票据']=1
                   elif qing.loc[i,'票面金额']<500000:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[6]]+0.15
                       qing.loc[i,'小票票据']=2
                   else:
                       qing.loc[i,'邮储指导价']=jia_df.loc[j,jia_df.columns[6]]
                       qing.loc[i,'小票票据']=0
                   qing.loc[i,'指导期限']=jia_df.columns[6]
                   qing.loc[i,'银行分类']=jia_df.loc[j,'银行分类']
                   qing.loc[i,'银行分类2']=jia_df.loc[j,'银行类型']

                   qing.loc[i,'交易日']=str(shijian)
                   qing.loc[i,'交易日']=qing.loc[i,'交易日'].replace(' 00:00:00','')
                   qing.loc[i,'出票日']=qing.loc[i,'出票日'].replace(' 00:00:00','')
                   qing.loc[i,'到期日']=qing.loc[i,'到期日'].replace(' 00:00:00','')
                   qing.loc[i,'到期月']=qing.loc[i,'到期日'][:(len(qing.loc[i,'到期日'])-3)]

                   qing.loc[i,'承兑行号']=qing.loc[i,'承兑行号'].replace('.0','')
               
                   shijiancha=str(qing.loc[i,'到期日2']-shijian) #转化为str
                   shijiancha=int(shijiancha.replace(' days 00:00:00',''))  #转化为int
                   qing.loc[i,'期限']=shijiancha
                   qing.loc[i,'ji1']=shijiancha*qing.loc[i,'票面金额']
                   qing.loc[i,'ji2']=shijiancha*qing.loc[i,'票面金额']*qing.loc[i,'邮储指导价']
                   qing.loc[i,'可用额度']=jia_df.loc[j,'可用额度']
                   qing.loc[i,'生效截至日']=jia_df.loc[j,'生效截至日']
                   qing.loc[i,'授信有效']=jia_df.loc[j,'授信有效']
                   qing.loc[i,'我行评级']=jia_df.loc[j,'我行评级']
                   suanqingdan=suanqingdan+1
                   
    if suanqingdan<=0:
        print('整个清单都不能收！或者请清单检查格式。提示：1.出票日、到期日要是日期格式，2.是否有其他“承兑”、“付款”之类的列名存在，系统误认为是错误的“承兑行”列。')
        del qing['到期日2']
        qing2=qing
        
    else:
        qing['加权利率']=qing.loc[:,'ji2'].sum()/qing.loc[:,'ji1'].sum()
        del qing['到期日2']



        qing=qing[['票号','票面金额','出票人','承兑行','承兑行号','出票日','到期日','交易日','银行分类','银行分类2','邮储指导价','小票票据','指导期限','加权利率','贴现行','可用额度','我行评级','生效截至日','授信有效','期限','到期月']]
#三、将算好的清单写入excel
        qing2=qing.replace(np.nan,99)
     
        qing2=qing2[qing2['邮储指导价'] != 99]  #排除NAN
        chengdui=qing2['票面金额'].groupby(qing2['银行分类']).sum()/10000
        print('  ')

        zongjin=qing2['票面金额'].sum()/10000
        print('总金额：%s'%zongjin)
        print('  清单分类如下：')

        print(chengdui)
        print('  ')
        yuefen=qing2['票面金额'].groupby(qing2['到期月']).sum()/10000
        print(yuefen)
        print('  ')
        qixian=qing2['期限'].mean()
        print(qixian)
        print('  ')
        print('提示：票据持有方式选：持有！申报清单总金额和张数是否和对方实际发来的一致？承兑行是否有错别字？')

    
    





#四、制作导
        qing2['导汇票']=1
        qing2['导出票人账号']=''
        qing2['导收款人名称']=''
        qing2['导1']=''
        qing2['导2']=''
        qing2['导3']=''
        qing2['同城']=1
        qing2=qing2[['导汇票','票号','票面金额','出票日','到期日','出票人','导出票人账号','承兑行号','承兑行','导收款人名称','导1','导2','导3','承兑行号','同城','交易日','期限']]

        qing2=qing2.fillna('')  #把日期列的nan 数值用空值填充，统一空值

        qing2=qing2[(qing2['票号'] !='')]
        qing2= qing2.reset_index(drop=True)    #重新定义索引
        qing=qing.fillna('')  #把日期列的nan 数值用“NAN”填充，统一空值


        qing=qing[(qing['票号'] !='')]
        qing= qing.reset_index(drop=True)    #重新定义索引
        
        
def heimingdan():
    global qing,qing2,shijian0
    hei1=pd.read_excel('转贴现买断价格计算/系统黑名单.xls',encoding='GB18030')
  #  hei2=pd.read_excel('转贴现买断价格计算/系统黑名单企业.xls',encoding='GB18030')           
    
    for i in range(0,len(hei1)):
        if '/' in  hei1.loc[i,'银行黑名单']:      
            erhei= hei1.loc[i,'银行黑名单'].split('/')
            for j in range(0,len(qing)):
                if (erhei[0] in qing.loc[j,'承兑行']) and (erhei[1] in qing.loc[j,'承兑行']):
                    qing.loc[j,'黑名单']=hei1.loc[i,'黑名单类型']
                    qing2.loc[j,'黑名单']=hei1.loc[i,'黑名单类型']
            
                   # break
            
            
            
        else:
            for j in range(0,len(qing)):
                if hei1.loc[i,'银行黑名单'] in qing.loc[j,'承兑行']:
                    qing.loc[j,'黑名单']=hei1.loc[i,'黑名单类型']
                    qing2.loc[j,'黑名单']=hei1.loc[i,'黑名单类型']
                  #  break
    url3='临时清单/'+shijian0+duifang+'导入.xls'
    writer = pd.ExcelWriter(url3)
    qing2.to_excel(writer,'Sheet1')
    writer.save()

    url2='临时清单/'+shijian0+duifang+'算加权.xls'
    writer = pd.ExcelWriter(url2)
    qing.to_excel(writer,'Sheet1')
    writer.save()
for i in range(0,1):
    print('\n')
    duifang=input('请输入第%s个文件名：'%i)
 #   duifang=''+duifang|
    url=('临时清单/%s'%duifang)
    if duifang=='':
        continue
    else:
        
        suanqingdan()
        heimingdan() 
        

