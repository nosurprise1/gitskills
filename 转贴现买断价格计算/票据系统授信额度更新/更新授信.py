import csv,xlrd,xlwt,datetime,time
import pandas as pd


shouxin=pd.read_excel('shouxin2.xls',encoding='GB18030')
shouxin=shouxin[['客户名称','可用额度','生效截至日']]
shouxin['d']=0


#shouxin= shouxin.reset_index(drop=True)    #重新定义索引


#一、导入指导价
jia_df=pd.read_excel('jia.xls',encoding='GB18030')
jia_df['生效截至日'] = pd.to_datetime(jia_df['生效截至日']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式


shouxin['客户名称']=shouxin['客户名称'].astype(str)

shouxin['生效截至日'] = pd.to_datetime(shouxin['生效截至日']).astype('str')     #,format='%Y%m%d'  吧yyyy-m-d 转化为yyyy-mm-dd的时间格式



for j in range(0,len(shouxin)):
  for i in range(0,len(jia_df)):
    if jia_df.loc[i,'银行类型'] in shouxin.loc[j,'客户名称']:
        shouxin.loc[j,'d']='已有'
        if jia_df.loc[i,'生效截至日']==shouxin.loc[j,'生效截至日'] :
          jia_df.loc[i,'可用额度']=shouxin.loc[j,'可用额度']
          
          continue
        else:
          print(jia_df.loc[i,'银行类型'])
          print(jia_df.loc[i,'生效截至日'])
          print(shouxin.loc[j,'生效截至日'])
          print(jia_df.loc[i,'可用额度'])
          print(shouxin.loc[j,'可用额度'])


          
          jia_df.loc[i,'更新']=1
          jia_df.loc[i,'生效截至日']=shouxin.loc[j,'生效截至日']
          jia_df.loc[i,'可用额度']=shouxin.loc[j,'可用额度']
        break
  


shouxin=shouxin[shouxin['d']!='已有']
shouxin= shouxin.reset_index(drop=True)    #重新定义索引
for i in range(0,len(shouxin)):
  #挑选出BBB+及以上的银行

    if ('财务' in shouxin.loc[i,'客户名称']):
        shouxin.loc[i,'d']=5      #财务公司        

    
url3='xin2.xls'
writer = pd.ExcelWriter(url3)
shouxin.to_excel(writer,'Sheet1')
writer.save()


url3='jia3.xls'
writer = pd.ExcelWriter(url3)
jia_df.to_excel(writer,'Sheet1')
writer.save()

