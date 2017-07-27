import itchatmp
from itchatmp.content import TEXT
from tuling import get_response

itchatmp.update_config(itchatmp.WechatConfig(
    token='48fLSTTBDVI5TIDpd1gLdFYwKqex4Mk',
    appId = 'wx34c7eb36575d6084',
    appSecret = 'iWPsYqgLW5OWmhUpIXcSlOjwkWjZyGImSJy20F2d9auXmoO6OpSqPXEixgPfJfW5')
   
@itchatmp.msg_register(TEXT)
def text_reply(msg):
    reply = get_response(msg['Content'])
    return {'MsgType': itchatmp.content.TEXT, 'Content': reply}

app = itchatmp.run(isWsgi=True)
