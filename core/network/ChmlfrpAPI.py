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
        try:
            if data["code"]==404:
                return False,["请先创建隧道"]
        except:
            return True,data
    except:
        return False,None

# 删除隧道
def del_tun(tun_id):
    try:
        log.info(f"token:{User.token} 正在删除隧道 id:{tun_id}")
        data=requests.get("https://panel.chmlfrp.cn/api/deletetl.php",{"token":User.token,"userid":User.id,"nodeid":tun_id}).json()
        if data["code"]==200:
            return True,None
        else:
            return False,data["error"]
    except:
        return False,None

# 节点信息
def node():
    try:
        log.info("尝试获取隧道信息")
        return requests.get("https://panel.chmlfrp.cn/api/unode.php").json()
    except:
        return [{"name":"无数据"}]

# add隧道
def addtun(type,nport,node,name,localip,dorp):
    try:
        log.info("尝试获取隧道信息")
        data=requests.get("https://panel.chmlfrp.cn/api/tunnel.php",
        {
            "token":User.token,
            "userid":User.id,
            "type":type,
            "nport":nport,
            "node":node,
            "name":name,
            "localip":localip,
            "dorp":dorp
            }).json()
        if data["code"]==200:
            return True,"创建成功"
        else:
            return False,data["error"]
    except:
        return False,"无法请求api"