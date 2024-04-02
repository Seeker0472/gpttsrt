# encoding:utf-8
import os
import configargparse as argparse
from .constants import DEFAULT_PATH_IN, DEFAULT_PATH_COMPLETED, DEFAULT_PATH_OUT, MAX_THREAD, LINE_PER_REQUEST, \
    CONF_FILE_NAME
from .log import logging


def get_args():
    # 解析参数
    logging.info("解析参数")
    parser = argparse.ArgumentParser()
    if os.path.exists(CONF_FILE_NAME):
        print(f'使用默认配置文件:{CONF_FILE_NAME}')
        parser.add_argument("-c", "--config", required=False, is_config_file=True, default=CONF_FILE_NAME,
                            help="配置文件路径")
    else:
        parser.add_argument("-c", "--config", required=False, is_config_file=True, help="配置文件路径")
    parser.add_argument('--path_in', type=str, default=DEFAULT_PATH_IN, help='输入srt文件的文件夹路径')
    parser.add_argument('--path_completed', type=str, default=DEFAULT_PATH_COMPLETED, help='已完成srt文件的文件夹路径')
    parser.add_argument('--path_out', type=str, default=DEFAULT_PATH_OUT, help='输出srt文件的文件夹路径')
    parser.add_argument('--max_thread', type=int, default=MAX_THREAD, help='最大线程数')
    parser.add_argument('--line_per_request', type=int, default=LINE_PER_REQUEST, help='每次请求的行数')
    parser.add_argument('--api_key', type=str, default='', help='OpenAI API key')
    parser.add_argument('--mirror_url', type=str, default=None, help='OpenAI mirror url')

    options = parser.parse_args()

    return options
