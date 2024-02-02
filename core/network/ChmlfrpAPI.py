import requests

from core.g_var import User
from core.module import log

# 登录
def login(Name,Password):
    try:
        data=requests.get("https://panel.chmlfrp.cn/api/login.php",{"username": Name,"password":Password}).json()
        log.info("尝试登录...")
        # 放入数据
        User.id = data['userid']
        User.token = data['token']
        User.LoginData = data
        return True,None
    except:
        log.error("登录失败")
        return False,"未知原因"

# 隧道列表获取
def user_tun():
    try:
        log.info(f"token:{User.token} 尝试获取隧道信息")
        data=requests.get("https://panel.chmlfrp.cn/api/usertunnel.php",{"token":User.token}).json()
        return True,data
    except:
        return False,None