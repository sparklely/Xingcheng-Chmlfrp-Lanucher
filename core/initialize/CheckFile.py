import os

# 检查frp核心是否存在
def CheckFrp():
    # 判断系统类型
    if os.name=="nt":
        return os.path.isfile("./frpc.exe") and os.path.isfile("./frps.exe")
    else:
        return os.path.isfile("./frpc") and os.path.isfile("./frps")