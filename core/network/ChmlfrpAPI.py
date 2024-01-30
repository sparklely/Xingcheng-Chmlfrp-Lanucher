from core.g_var import Uesr
import requests

# 登录
def login(Name,Password):
    try:
        data=requests.get("https://panel.chmlfrp.cn/api/login.php",{"username": Name,"password":Password}).json()
        # 放入数据
        Uesr.id=data['userid']
        Uesr.token=data['token']
        return True
    except:return False

