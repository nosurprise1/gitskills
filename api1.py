#!flask/bin/python
from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
from flask.ext.httpauth import HTTPBasicAuth
import datetime,time
from flask import request
auth = HTTPBasicAuth()
import urllib.parse
app = Flask(__name__)
client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')



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
          
          if piaofen_df.empty:
             aaa='empty'
             return(jsonify(aaa))
          else:
            del piaofen_df['_id']

            piaofen_df=piaofen_df.to_json()

            return(piaofen_df)
         # df = pd.DataFrame([['a', 'b'], ['c', 'd']])
         # df=df.to_json(orient='index')
         # return(df)

    elif task_id==2:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chu':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)

    elif task_id==3:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shou':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)

    elif task_id==4:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chuhui':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)

    elif task_id==5:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shouhui':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)  

    elif task_id==6:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chudai':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)  

    elif task_id==7:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shoudai':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)                

    elif task_id==8:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chufu':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)                

    elif task_id==9:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chufu':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)                

    elif task_id==10:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chuli':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)                

    elif task_id==11:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shouli':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)                

           

    elif task_id==12:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'chucun':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)                

    elif task_id==13:
                   db3 = client.piaofen
                   collection3 = db3.piaofen   
                   cursor3 = collection3.find({"$and":[
                                                   {"$or":[{'time':str(shijian11)},{'time':str(shijian0)},{'time':str(shijian01)},{'time':str(shijian02)}]},
                                                   {'shoucun':1},
                                                   {'hanglei2':1},
                                                    ]})
                   piaofen_df = pd.DataFrame(list(cursor3))
                   del piaofen_df['_id']

                   piaofen_df=piaofen_df.to_json()

                   return(piaofen_df)                
    elif task_id==14:
        
        
        sou = request.args.get('text')
        print(sou)
        sou=urllib.parse.unquote(sou)
        print(sou)
        db3 = client.zixun
        collection3 = db3.zixun   
        cursor3 = collection3.find({"$and":[{'爬取日期':{'$gte':str(shijian014)}},{'标题':{'$regex':sou}}]})    
        zixun_df = pd.DataFrame(list(cursor3))
        if zixun_df.empty:
                return('999')
        zixun_df = zixun_df.sort_values(by='爬取日期', ascending=True)
        zixun_df =  zixun_df.reset_index(drop=True)  
        
        del zixun_df['_id']

        zixun_df=zixun_df.to_json()
        
        return(zixun_df)    
    elif task_id==15:
        sou = request.args.get('text')
        print(sou)
        sou=urllib.parse.unquote(sou)
        print(sou)
        
        db3 = client.zixun
        collection3 = db3.zixun   
        cursor3 = collection3.find({"$and":[{'爬取日期':{'$gte':str(shijian014)}},{'内容':{'$regex':sou}}]})    
        zixun_df = pd.DataFrame(list(cursor3))
        if zixun_df.empty:
                return('999')
        zixun_df = zixun_df.sort_values(by='爬取日期', ascending=True)
        zixun_df =  zixun_df.reset_index(drop=True)  
                
        del zixun_df['_id']

        zixun_df=zixun_df.to_json()
        
        return(zixun_df)    
        
    else:
        return('网络不好!!!!!')



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=90,debug=True)
