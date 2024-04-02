# encoding:utf-8
import datetime
import logging
import os
from .constants import LOG_PATH

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# 获取当前时间
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 构造日志文件名
log_filename = f"./logs/app_{current_time}.log"

# 配置日志记录器
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
