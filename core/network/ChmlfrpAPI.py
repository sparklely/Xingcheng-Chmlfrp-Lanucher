from core.g_var import User
import requests

# 登录
def login(Name,Password):
    try:
        data = requests.get("https://panel.chmlfrp.cn/api/login.php",{"username": Name,"password":Password}).json()
        # 放入数据
        User.id = data['userid']
        User.token = data['token']
        User.LoginData = data
        return True
    except:
        return False