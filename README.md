# gpttsrt

一个使用gpt3.5来批量翻译srt字幕文件的工具,用来批量翻译公开课字幕

名字: gpt_translate_srt -> gpttsrt

## 使用方法说明

### 源码安装
    
clone 本项目到本地
```bash
git clone https://github.com/Seeker0472/gpttsrt.git
```
cd到项目目录
```bash
cd gpttsrt
```
安装
```bash
pip install -e .
```
## 配置文件
**example:** gpttsrt.conf
```conf
path_in = './input' # 输入文件夹
path_completed = './completed' # 将翻译完成的源文件移动到这个文件夹
path_out = './output' # 输出文件夹
api_key = '' # openai的api key
mirror_url= '' # openai的api url,如果不适用镜像服务就不用填
max_thread = 10 # 最大线程数(同时翻译多个文件,提高速度), 默认为10
line_per_request = 10 # 每次请求翻译的行数, 默认为10
```
## 运行
```bash
gpttsrt -c --config gpttsrt.conf
```