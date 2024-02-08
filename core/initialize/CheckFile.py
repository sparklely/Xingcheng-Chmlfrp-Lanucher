from os import path,name,makedirs
# 检查frp核心是否存在
def CheckFrp():
    # 判断系统类型
    if name=="nt":
        return path.isfile("./frp/frpc.exe")
    else:
        return path.isfile("./frp/frpc")

# 检查缓存文件夹是否存在
def CheckTemp():
    if not path.isdir("temp"):
        # 不存在创建
        makedirs("temp")