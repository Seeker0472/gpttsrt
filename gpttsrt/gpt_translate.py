# encoding:utf-8
import json
import re
import shutil

from .log import logging
from openai import OpenAI
from .constants import Open_AI_API_KEY, Open_AI_MIRROR_URL
import pysrt




def translate_texts(text):
    """
    翻译文本
    :param text: 文本
    :return: 翻译后的文本
    """
    client = OpenAI(
        api_key=Open_AI_API_KEY,
        base_url=Open_AI_MIRROR_URL
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system",
             "content": "You are a translator assistant, skilled in translating JSON object between English and Chinese .Respond should be JSON object"},
            {"role": "user",
             "content": f"Retain the original format.Follow these Chinese copywriting guidelines[1.Place one space before/after English words 2.No space between numbers and units 3.No additional spaces before/after punctuation in fullwidth form] Return only the id,translation and nothing else. \nExample:input:{{'0': 'I'll see you at the next lecture.'}} output:{{'0': '下次讲座见。'}}.\nTranslate the following JSON object into Simplified Chinese:\n{text}"}
        ],
        response_format={"type": "json_object"}
    )

    # print(completion.choices[0].message)
    data = json.loads(completion.choices[0].message.content)
    # if data.has_key('translations'):
    translation_list = None
    if 'translations' in data.keys():
        translation_list = data['translations']
    else:
        if 'translation' in data.keys():
            translation_list = data['translation']
        else:
            if not isinstance(data['0'], str):
                if isinstance(data['0'], dict) and 'translation' in data['0'].keys():
                    translation_list = data['0']['translation']
                else:
                    translation_list = data
            else:
                translation_list = data

    # print(translation_list)
    # print(completion)
    return translation_list


def translation_check(original_text, translated_text):
    """
    检查gpt3.5是不是没翻译或者把prompt翻译了
    :param original_text: 原始文本
    :param translated_text: 翻译后的文本
    :return: 是否正确翻译
    """
    tran_str = str(translated_text)
    if len(tran_str) == 0:
        logging.warning(f"Translation check failed-翻译为空: {original_text} -> {translated_text}")
        print(f"Translation check failed-翻译为空: {original_text} -> {translated_text}")
        return False
    # print(type(translated_text))
    if not isinstance(translated_text, dict):
        logging.warning(f"Translation check failed-翻译格式错误: {original_text} -> {translated_text}")
        print(f"Translation check failed-翻译格式错误: {original_text} -> {translated_text}")
        return False
    if not isinstance(translated_text['0'], str):
        logging.warning(f"Translation check failed-翻译格式错误: {original_text} -> {translated_text}")
        print(f"Translation check failed-翻译格式错误: {original_text} -> {translated_text}")
        return False
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')  # 匹配中文字符的正则表达式范围
    if not bool(chinese_pattern.search(tran_str)):
        logging.warning(f"Translation check failed-无中文: {original_text} -> {translated_text}")
        print(f"Translation check failed-无中文: {original_text} -> {translated_text}")
        return False
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo-1106",
    #     messages=[
    #         {"role": "system",
    #          "content": "You are a translaton-check assistant, skilled in checking translated text between English and Chinese"},
    #         {"role": "user",
    #          "content": f"Check the following translation. Return 'OK' if the translation is correct, 'NG' if the translation is incorrect or not been translated at all. Return only 'OK' or 'NG':\nEnglish:\n{original_text}\nChinese:\n{translated_text}"}
    #     ],
    # )
    # print(
    #     f"Check the following translation. Return 'OK' if the translation is correct, 'NG' if the translation is incorrect or not been translated at all. Return only 'OK' or 'NG':\nEnglish:\n{original_text}\nChinese:\n{translated_text}")
    # data = completion.choices[0].message.content
    # print(data)
    # if data.find('OK') == -1:
    #     return False
    if tran_str.find('按照这些中文文案规范') != -1 or tran_str.find(
            'these Chinese copywriting guidelines') != -1 or tran_str.find(
        '数字与单位之间不留空格') != -1 or tran_str.find('只返回id和翻译') != -1:
        logging.warning(f"Translation check failed-包含提示词: {original_text} -> {translated_text}")
        print(f"Translation check failed-包含提示词: {original_text} -> {translated_text}")
        return False
    return True


def translate_sub(file_path, path_out, path_complete, line_per_request):
    logging.info(f"开始翻译: {file_path}")
    subs = pysrt.open(file_path)
    sub_out = pysrt.SubRipFile()
    texts_en = []
    texts_zh = []
    # text_process=[]
    for i in range(len(subs)):
        text = subs[i].text
        texts_en.append(text)
    i = 0
    while i < len(texts_en):
        text_process = dict()
        j = 0
        offset = i
        while j < line_per_request and i < len(texts_en):
            # text_process.append(texts_en[i])
            text_process.update({str(j): texts_en[i]})
            j += 1
            i += 1

        ret_val = None
        for z in range(1, 10):
            ret_val = translate_texts(text_process)
            # 检查翻译结果
            if translation_check(text_process, ret_val):
                break
            if z >= 4:
                logging.error(f"翻译失败: {text_process}")
                raise Exception('翻译错误')
        ret_val_int = dict()
        # print("DEBUG  ret_val     ", ret_val)
        for k in list(ret_val.keys()):
            val = ret_val[k]
            # print(val)
            if val[-1] == '。' or val[-1] == '，' or val[-1] == ',' or val[-1] == '.':
                val = val[:-1]
            ret_val_int.update({int(k): val})
        now = 0
        now_end = 0
        # print(text_process, ret_val_int)
        logging.info(f"翻译结果: {text_process} -> {ret_val_int}")
        while now <= max(ret_val_int.keys()):
            now_end = now
            # while now_end + 1 < max(ret_val_int.keys()) and now_end + 1 not in ret_val_int.keys():
            while now_end + 1 < max([int(x) for x in text_process.keys()]) and now_end + 1 not in ret_val_int.keys():
                now_end += 1
            # sub_out.append(pysrt.SubRipItem(start=subs[now + i - STEP].start, end=subs[now_end + i - STEP].end,
            #                                 text=ret_val_int[now]))
            sub_out.append(pysrt.SubRipItem(start=subs[now + offset].start, end=subs[now_end + offset].end,
                                            text=ret_val_int[now]))
            now = now_end + 1

    logging.info(f"翻译完成: {file_path}")
    logging.info(f"存储到: {path_out + file_path.split('/')[-1] + '_gpt_zh.srt'}")
    sub_out.save(path_out + file_path.split('/')[-1] + '_gpt_zh.srt')
    shutil.move(file_path, path_complete + file_path.split('/')[-1])
