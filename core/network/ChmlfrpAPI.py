from core.g_var import User
from core.module import log
import requests

# 登录
def login(Name,Password):
    try:
        data = requests.get("https://panel.chmlfrp.cn/api/login.php",{"username": Name,"password":Password}).json()
        log.info("{Name} 尝试登录")
        data=requests.get("https://panel.chmlfrp.cn/api/login.php",{"username": Name,"password":Password}).json()
        # 放入数据
        User.id = data['userid']
        User.token = data['token']
        User.LoginData = data
        return True
    except:
        log.warn("{Name} 无法登录")
        return False

# 隧道列表获取
def user_tun():
    try:
        log.info(f"token:{User.token} 尝试获取隧道信息")
        data=requests.get("https://panel.chmlfrp.cn/api/usertunnel.php",{"token":User.token}).json()
        return data
    except:
        return None