import itchat,time

newInstance = itchat.new_instance()

newInstance.auto_login(hotReload=True)

friends = newInstance.get_friends()

for friend in friends:
    if friend['NickName'] == '火云邪神本尊' :
        r = newInstance.send(" ", toUserName=friend['UserName'])
    elif friend['RemarkName'] == '拉黑了我' :
        r = newInstance.send(" ", toUserName=friend['UserName'])

@newInstance.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg.text

newInstance.run()