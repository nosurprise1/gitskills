#!flask/bin/python
from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
from flask.ext.httpauth import HTTPBasicAuth
import datetime,time
auth = HTTPBasicAuth()

app = Flask(__name__)
client=MongoClient('mongodb://root:' + '5768116' + '@139.196.79.93')
#shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
#shijian2 = datetime.datetime.strptime(shijian2, "%Y-%m-%d")
#shijian2=shijian2.strftime("%Y-%m-%d")  #今天
         
#db3 = client.piaofen
#collection3 = db3.piaofen   
#cursor3 = collection3.find({
#                                                'time':str(shijian2)
#                                                 })
#print(type(cursor3))

#piaofen_df = pd.DataFrame(list(cursor3))

#print(piaofen_df.encode("utf-8", "ignore") )
#piaofen=piaofen_df.to_json(orient='split')
#print(piaofen)




@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
     return('!!!!!')

@app.route('/<int:task_id>', methods=['GET'])
@auth.login_required

def get_tasks(task_id):

    if task_id==1:
          shijian2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
          shijian2 = datetime.datetime.strptime(shijian2, "%Y-%m-%d")
          shijian2=shijian2.strftime("%Y-%m-%d")  #今天
          
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


          





    else:
        abort(404)



if __name__ == '__main__':
    app.run(debug=True)
