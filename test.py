import itchat,time

newInstance = itchat.new_instance()


@newInstance.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg.text

newInstance.auto_login()

newInstance.run()