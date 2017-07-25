
server {
        listen 80;
        server_name new.vtao.net;
        access_log /var/log/nginx/new.vtao.net.log;
        location / {
                include fastcgi_params;
                fastcgi_pass unix:/tmp/py-fcgi.sock;
        }
        location /static/ {
                root /var/webpy;
                if (-f $request_filename){
                        rewrite ^/static/(.*)$ /static/$1 break;
                }
        }
}
 
 

#!/usr/bin/env python
import web
import datetime
 
urls=(
        '/', 'index',
)
 
app=web.application(urls, globals())
 
class index:
        def GET(self):
                return "Hello, world! now is:"+str(datetime.datetime.utcnow())
 
if __name__=="__main__":
        web.wsgi.runwsgi=lambda func,addr=None: web.wsgi.runfcgi(func,addr)
        app.run()
 
