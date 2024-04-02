# encoding:utf-8
DEFAULT_PATH_IN = "./srt_in/"
DEFAULT_PATH_COMPLETED = "./srt_completed/"
DEFAULT_PATH_OUT = "./srt_out/"
CONF_FILE_NAME = "./gpttsrt.conf"
LOG_PATH = "./logs/"
MAX_THREAD = 10
# MAX_TEP = 10
LINE_PER_REQUEST = 10
Open_AI_API_KEY = None
Open_AI_MIRROR_URL = None


def set_openai(key, url):
    global Open_AI_API_KEY, Open_AI_MIRROR_URL
    Open_AI_API_KEY = key
    Open_AI_MIRROR_URL = url
