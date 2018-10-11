import itchat,time

newInstance = itchat.new_instance()

newInstance.auto_login(hotReload=True)

friends = newInstance.get_friends()

for friend in friends:
    newInstance.send('', toUserName=friend['UserName'])

@newInstance.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg.text

newInstance.run()