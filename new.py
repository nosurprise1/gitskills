import itchatmp
from itchatmp.content import TEXT
from tuling import get_response

itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wx7860b4c7296dcbdf',
    appSecret = 'a8db85056d55d3e74d662667b9b015ea'))
   
@itchatmp.msg_register(TEXT)
def text_reply(msg):
    reply = get_response(msg['Content'])
    return {'MsgType': itchatmp.content.TEXT, 'Content': reply}

app = itchatmp.run(isWsgi=True)
