'''
Author: swz128 swz12306@gmail.com
Date: 2024-11-10 06:38:32
LastEditors: swz128 swz12306@gmail.com
LastEditTime: 2024-11-12 17:38:09
FilePath: /xrzww-novel/novel_download.py
Description: 息壤中文网小说下载器
'''
import time
import hashlib
import json
import requests
from pathlib import Path

novel_name = '测试文本'         # 小说名称
novel_id = '112233'           # 小说ID
Authorization = 'Bearer xxxxxxxxxxxxxxxxxxxxxxxxx'  # 授权令牌
deviceModel = 'xxxxxxxxxxx'         # 设备型号
deviceIdentify = 'xxxxxxxxxxxxxxx' # 设备唯一标识

headers = {
    'Authorization': Authorization,
    'deviceType': 'android',
    'appVersion': '4.84',
    'timestamp': '1731188623',
    'deviceModel': deviceModel,
    'site': '1',
    'content-type': 'application/json',
    'deviceIdentify': deviceIdentify,
    'signature': '65bb52387f812517b5ccc02911d58586',    # 签名
    'headerRequestSource': 'xirang',
    'Host': 'android-api.xrzww.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.8.0'
}

# 创建目录
def create_directory(directory):
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"目录 {directory} 创建成功")
    except OSError as e:
        print(f"创建目录 {directory} 失败: {e}")

# 获取时间戳
def get_timestamp():
    return str(int(time.time()))

# 获取签名
def get_signature(deviceIdentify, timestamp):
    signature_text = deviceIdentify + timestamp + '9495ef469eb3e7ae8ef3'
    signature = hashlib.md5(signature_text.encode()).hexdigest()
    return signature

# 获取小说目录(抓包获取的目录数据)
def get_novel_directory(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data['data']

# 保存章节内容
def save_chapter_content(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)
        print(f'保存章节内容到文件 {file_name} 成功！')

# 下载章节
def download_chapter(novel_id, chapter_id, volume_directory):

    url = f'https://android-api.xrzww.com/api/downloadNovelChapterWithEncrypt?chapter_id={chapter_id}&nid={novel_id}&preload=1'
    print(url)

    timestamp = get_timestamp()
    signature = get_signature(headers['deviceIdentify'], timestamp)
    headers['timestamp'] = timestamp    # 时间戳
    headers['signature'] = signature    # 签名
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        save_chapter_content(f'{volume_directory}/{chapter_id}.json', res.text)
        print(f'{chapter_id}\t' + '下载成功')
    else:
        print(f'{chapter_id}\t' + res.status_code)


if __name__ == '__main__':

    # 获取目录数据
    data = get_novel_directory('novelDirectory.json')

    # 循环遍历下载小说章节
    for index, item in enumerate(data):

        volume_directory = Path(f'cache/{novel_name}/{item['volume_name']}')
        create_directory(volume_directory)

        for chapter in data[index]['chapter_list']:
            # 打印章节名
            print(f"\t开始下载：" + chapter['chapter_name'])
            download_chapter(data[index]['volume_nid'], chapter['chapter_id'], volume_directory)