from core.module import log
from core.command import run
from core.initialize.CheckFile import CheckFrp


log.info("开始检查文件完整性")
# 检查文件完整性
if CheckFrp():
    # 启动
    run()
else:
    log.error("缺失frp核心")
    input("停止启动")