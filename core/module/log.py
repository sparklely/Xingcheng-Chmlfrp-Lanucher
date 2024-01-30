from initialize.config import config
from datetime import datetime

# 获取时间
def _time():
    # 获取当前时间
    now = datetime.now()
    # 格式化为 "小时:分钟:秒" 字符串
    time_str = now.strftime("%H:%M:%S")
    return time_str
# log基本函数
def _log(text):
    print(text)
# info处理
def info(text):
    if config.config["log"]["info"]:
        _log(f"[{_time()} info] {text}")
# warn处理
def warn(text):
    if config.config["log"]["warn"]:
        _log(f"[{_time()} warn] {text}")
# error处理
def info(text):
    if config.config["log"]["error"]:
        _log(f"[{_time()} error] {text}")