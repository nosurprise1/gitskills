import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wxdca1daea0b4961c4',
    appSecret = 'c0254c2306907abf729b98c38e9eaf55'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return(msg['Content'])

itchatmp.run()
