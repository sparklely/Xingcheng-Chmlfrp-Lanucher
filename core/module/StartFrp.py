from core.initialize import CheckFile
from core.network import ChmlfrpAPI

# 启动frp
def start(tun_id):
    if CheckFile.CheckFrp():
        # 检查用户是否拥有该隧道
        data=ChmlfrpAPI.user_tun()
    else:return False