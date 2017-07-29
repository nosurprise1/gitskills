import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='123456',
    appId = 'wx7860b4c7296dcbdf',
    appSecret = 'a8db85056d55d3e74d662667b9b015ea'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return msg['content']

itchatmp.run()
