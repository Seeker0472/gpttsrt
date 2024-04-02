# encoding:utf-8
import os
import concurrent.futures
from time import sleep

from tqdm import tqdm  # 导入tqdm
from .cmd import get_args
from .log import logging
from .gpt_translate import translate_sub
from .constants import set_openai


def main():
    # 解析参数
    args = get_args()

    path_in = args.path_in
    path_completed = args.path_completed
    path_out = args.path_out
    max_thread = args.max_thread
    line_per_request = args.line_per_request
    set_openai(args.api_key, args.mirror_url)
    logging.info(f"输入路径: {path_in}, 输出路径: {path_out}, 已完成路径: {path_completed}, 最大线程数: {max_thread}, "
                 f"每次请求的行数: {line_per_request}")
    print(args)
    print(f"输入路径: {path_in}, 输出路径: {path_out}, 已完成路径: {path_completed}, 最大线程数: {max_thread}, "
          f"每次请求的行数: {line_per_request}")
    # 初始化目录
    init(path_out, path_completed)
    go(path_in, path_out, path_completed, max_thread, line_per_request)


def init(path_out, path_completed):
    if not os.path.exists(path_out):
        os.mkdir(path_out)
    if not os.path.exists(path_completed):
        os.mkdir(path_completed)


def task(file):
    sleep(1)
    print(file)
    return file


def go(path_in, path_out, path_complete, max_thread, line_per_request):
    file_path = ''
    # try:
    logging.info('start')
    print('start')
    all_files = os.listdir(path_in)
    files_path = []
    for file in all_files:
        file_path = os.path.join(path_in, file)
        if os.path.isfile(file_path):
            files_path.append(file_path)


    # 创建一个线程池执行器
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread) as executor:
        # 提交任务给线程池并收集Future对象
        futures = [executor.submit(translate_sub, file_path,path_out,path_complete,line_per_request) for file_path in files_path]

        print("任务提交完成，执行中...")

        # 使用tqdm显示任务完成进度
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="处理中"):
            result = future.result()  # 获取任务返回结果
            # tqdm会自动更新进度条，这里可以根据需要处理任务结果或者更新其他UI元素
            # print(f"任务{result}完成")  # 如果需要，可以取消这行的注释来查看每个任务的完成情况

        print("所有任务执行完毕。")
    # except Exception as e:
    #     logging.error(f"翻译失败: {file_path}")
    #     logging.error(f"错误信息: {e}")
    #     print(f"翻译失败: {file_path}")
    #     print(f"错误信息: {e}")
    #     go(path_in, path_out, path_complete, max_thread, line_per_request)
        # shutil.move(file_path, path_complete + file_path.split('/')[-1])


if __name__ == "__main__":
    main()
