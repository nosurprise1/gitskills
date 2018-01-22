#!flask/bin/python
from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
from flask.ext.httpauth import HTTPBasicAuth
import datetime,time,json
from flask import request
auth = HTTPBasicAuth()
import urllib.parse
app = Flask(__name__)
client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')
#piaofen2是记录exe的操作
db = client.piaofen2
collection = db.piaofen2  #http://www.jb51.net/article/77537.htm



@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
     return('wrong password or usename!!!!!')

@app.route('/<int:task_id>', methods=['GET'])
@auth.login_required

def get_tasks(task_id):
    shijian2=time.strftime('%H:%M',time.localtime(time.time()))
    shijian11=time.strftime('%y-%m-%d',time.localtime(time.time()))
    shijian11 = datetime.datetime.strptime(shijian11, "%y-%m-%d")
    shijian10=shijian11-datetime.timedelta(days=1)  #明天
    shijian0=shijian11-datetime.timedelta(days=1)
    shijian01=shijian11-datetime.timedelta(days=2)
    shijian02=shijian11-datetime.timedelta(days=3)
    shijian014=shijian11-datetime.timedelta(days=30)
    shijian11=shijian11.strftime("%Y-%m-%d")  #今天
    shijian0=shijian0.strftime("%Y-%m-%d")     #昨天
    shijian01=shijian01.strftime("%Y-%m-%d")   #前天
    shijian02=shijian02.strftime("%Y-%m-%d")   #大前天
    caozuo= request.args.get('caozuo')
    print(caozuo) 
    ggg = request.args.get('ggg')
    print(ggg)
    #获取业务撮合关键词
    leixing = request.args.get('leixing')
    print(leixing)
    jigou=request.args.get('jigou')
    print(jigou)
    lianxi=request.args.get('lianxi')
    print(lianxi)
    beizhu=request.args.get('beizhu')
    print(beizhu)
    qixian=request.args.get('qixian')
    print(qixian)    
    
    #获取资讯搜索关键词
    mubiao=request.args.get('mubiao')
    print(mubiao)    
    jiansuoci=request.args.get('jiansuoci')
    print(jiansuoci)    

        
    #获取存单分析关键词
    yinhang_cun=request.args.get('yinhang_cun')
    print(yinhang_cun)    
    qixian_cun=request.args.get('qixian_cun')
    print(qixian_cun)    

    
    #获取市场分析关键词
    yewu=request.args.get('yewu')
    print(yewu)  
    
    
    data=pd.DataFrame({'time':[shijian11],
                              'time2':[shijian2],
                              '业务类型':[leixing],
                              '银行':[jigou],
                              '联系人':[lianxi],
                              '备注':[beizhu],
                              '期限':[qixian],
                              '搜索目标':[mubiao],
                              '检索词':[jiansuoci],
                              '业务分析':[yewu],
                              '用户':[ggg],
                             '操作':[caozuo]
                              })    
                  
    records = json.loads(data.T.to_json()).values()
    collection.insert(records)
    print(data)     
    
    
    
    
    if task_id==1:
          shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          shijian2 = datetime.datetime.strptime(shijian2, "%Y-%m-%d")
          shijian2=shijian2.strftime("%Y-%m-%d")  
          db3 = client.piaofen
          collection3 = db3.piaofen   
          cursor3 = collection3.find({
                                                 'time':str(shijian2)
                                                 })
          piaofen_df = pd.DataFrame(list(cursor3))
          print(piaofen_df)
          if piaofen_df.empty:
             return('999')
          else:
            del piaofen_df['_id']

            piaofen_df=piaofen_df.to_json()

            return(piaofen_df)
         # df = pd.DataFrame([['a', 'b'], ['c', 'd']])
         # df=df.to_json(orient='index')
         # return(df)

    elif task_id==2:
                   if leixing=='票据买断':
                       yec='chu'
                   elif leixing=='票据卖断':
                       yec='shou'
                   elif leixing=='票据收买返':
                       yec='chuhui'
                   elif leixing=='票据出回购':
                       yec='shouhui'
                   elif leixing=='票据收代持':
                       yec='chudai'
                   elif leixing=='票据出代持':
                       yec='shoudai'
                   elif leixing=='收福费廷':
                       yec='chufu'
                   elif leixing=='出福费廷':
                       yec='shoufu'
                   elif leixing=='收存单':
                       yec='chucun'            
                   elif leixing=='出存单':
                       yec='shoucun'               
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {yec:1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   if piaofen_df.empty:
                        return('999')
          
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)

            
    elif task_id==14:
        db3 = client.zixun
        collection3 = db3.zixun   
        cursor3 = collection3.find({"$and":[{'爬取日期':{'$gte':str(shijian014)}},{mubiao:{'$regex':jiansuoci}}]})    
        zixun_df = pd.DataFrame(list(cursor3))
        if zixun_df.empty:
                return('999')
        zixun_df = zixun_df.sort_values(by='爬取日期', ascending=True)
        zixun_df =  zixun_df.reset_index(drop=True)  
        
        del zixun_df['_id']
        zixun_df=zixun_df[['爬取日期','标题','权重','时间','内容','链接','序号']]
        zixun_df.rename(columns={'爬取日期': '日期', '权重': '分类', '序号': '来源'}, inplace=True) 

        zixun_df=zixun_df.to_json()
        
        return(zixun_df)    
    elif task_id==15:
        print(yinhang_cun)
        db3 = client.cundan
        collection3 = db3.cundan  
        cursor3 = collection3.find({"$and":[{'发行日':{'$gte':str(shijian014)}},{'发行人':{'$regex':yinhang_cun}}]}) 
        
        cun_df = pd.DataFrame(list(cursor3))
        print(cun_df)
        if cun_df.empty:
                return('999')
        cun_df = cun_df.sort_values(by='爬取日期', ascending=True)
        cun_df =  cun_df.reset_index(drop=True)  
        
        del cun_df['_id']
        #cun_df=cun_df[['爬取日期','','权重','时间','内容','链接','序号']]
        cun_df.rename(columns={'爬取日期': '日期'}, inplace=True) 

        cun_df=cun_df.to_json()
        
        return(cun_df)    
        
    else:
        return('网络不好!!!!!')



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=90,debug=True)
