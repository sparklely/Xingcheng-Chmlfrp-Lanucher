from core.initialize import CheckFile
from core.network import ChmlfrpAPI
from core.module import log
from core.g_var import User
import os

# 启动frp
def start(tun_id):
    log.info(f"token:{User.token} ID:{tun_id} 尝试启动")
    if CheckFile.CheckFrp():
        # 检查用户是否拥有该隧道
        data=ChmlfrpAPI.user_tun()
        fash=False
        for da in data:
            if da["id"]==tun_id:
                fash=True
                break
        if fash:
            # 驱动frp核心
            if os.name=="nt":
                os.system("start frpc.exe"+" -u "+User.token+" -p "+tun_id)
            else:
                os.system("start frpc"+" -u "+User.token+" -p "+tun_id)
            log.info(f"启动frp: token:{User.token} ID:{tun_id} 已拉起")
            return "已拉起frp核心"
        else:
            log.warn(f"启动frp: ID:{tun_id} 不属于token:{User.token}")
            return f"ID:{tun_id} 不属于你"
    else:
        log.error("启动frp: 未知错误")
        return "未知错误"