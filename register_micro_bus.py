import itchat
from itchat.content import *
import re, json

TOKEN = '0083570248794aa965701441dd42923530a0abe78901'
ITEMID = '21001'

newInstance = itchat.new_instance()

newInstance.auto_login(hotReload=True)


@newInstance.msg_register([TEXT, SHARING])
def invite_micro_bus(msg):
    if msg['ToUserName'] == 'filehelper':
        global inviteId, inviteCode
        content = msg['Content']
        regx_inviteId = r'inviteId=(\w+)'
        regx_inviteCode = r'inviteCode=(\d+)'
        inviteIdResult = re.search(regx_inviteId, content)
        inviteCodeResult = re.search(regx_inviteCode, content)
        if inviteIdResult:
            inviteId = inviteIdResult.group(1)
        else:
            return
        if inviteCodeResult:
            inviteCode = inviteCodeResult.group(1)
        else:
            return

        # 开始获取用于登录的手机号码
        global mobile
        getMobile = False
        while not getMobile:
            param = {
                'action': 'getmobile',
                'token': TOKEN,
                'itemId': ITEMID
            }
            r = newInstance.s.get('http://api.fxhyd.cn/UserInterface.aspx', params=param)
            regx_mobile = r'success\|(\d+)'
            mobileResult = re.search(regx_mobile, r.text)
            if mobileResult:
                getMobile = True
                mobile = mobileResult.group(1)

        # 短信注册 微公交
        sendCode = False
        while not sendCode:
            param = {
                'account': mobile
            }
            r = newInstance.s.post('https://api.wgjev.net/app/login/sendCode', params=param)
            j = json.loads(r.text)
            if j.get('code') == '200':
                sendCode = True

        # 易码获取短信验证码
        global code
        getCode = False
        while not getCode:
            param = {
                'action': 'getsms',
                'token': TOKEN,
                'itemId': ITEMID,
                'mobile': mobile,
                'release': 1
            }
            r = newInstance.s.get('http://api.fxhyd.cn/UserInterface.aspx', params=param)
            regx_getCode = r'success\|.*(\d{4})'
            getCodeResult = re.search(regx_getCode, r.text)
            if getCodeResult:
                getCode = True
                code = getCodeResult.group(1)

        # 进行注册
        param = {
            'account': mobile,
            'password': code,
            'inviteId': inviteId,
            'inviteCode': inviteCode
        }
        r = newInstance.s.post('https://api.wgjev.net/app/login/inviteReg', params=param)
        j = json.loads(r.text)
        if j.get('code') == '200':
            newInstance.send("register micro bus success", 'filehelper')

            # 使用过的手机号码拉黑
            param = {
                'action': 'addignore',
                'token': TOKEN,
                'itemid': ITEMID,
                'mobile': mobile
            }
            r = newInstance.s.get('http://api.fxhyd.cn/UserInterface.aspx', params=param)


newInstance.run()
