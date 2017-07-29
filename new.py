import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='yourToken',
    appId = 'yourAppId',
    appSecret = 'yourAppSecret'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return msg['content']

itchatmp.run()
