'''
Author: swz128 swz12306@gmail.com
Date: 2024-11-10 09:48:31
LastEditors: swz128 swz12306@gmail.com
LastEditTime: 2024-11-12 17:38:45
FilePath: /xrzww-novel/novel_decrypted.py
Description: 息壤中文网小说解密解密
'''
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import json
from pathlib import Path


# 定义密钥和初始化向量
key = b"VT5aj59QCjf2J8F3"
iv = b'259c4e9881b5fe05'

# 获取小说目录(抓包获取的目录数据)
def get_novel_directory(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data['data']

# 获取章节内容(已下载的内容)
def get_chapter_content(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data['data']

# 保存章节内容
def save_chapter_content(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)
        print(f'保存章节内容到文件 {file_name} 成功！')

# 解密章节内容
def decrypt_chapter_content(encrypted_content):

    # 将加密内容从 Base64 解码
    encrypted_data = base64.b64decode(encrypted_content)

    # 创建 AES 解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        # 解密数据
        decrypted_data = cipher.decrypt(encrypted_data)
        # 移除填充
        original_data = unpad(decrypted_data, AES.block_size).decode('utf-8')
        print("解密后的内容:", original_data)
        return original_data

    except Exception as e:
        print(f"解密失败：{e}")
        return None

if __name__ == '__main__':

    # 小说名称
    novel_name = '测试文本'

    # 获取目录数据（novelDirectory.json需要抓包获取）
    directory_data = get_novel_directory('novelDirectory.json')

    fp = open(f'output/{novel_name}.txt', 'w')

    # 循环遍历下载小说章节
    for index, item in enumerate(directory_data):
        fp.write(f'《{novel_name}》\n\n\n')

        volume_directory = Path('cache/' + f'{novel_name}/' + item['volume_name'])
        fp.write(item['volume_name'] + '\n')    # 写入卷名

        for chapter in directory_data[index]['chapter_list']:
            # 打印章节名
            print(f"\t解码：" + chapter['chapter_name'])

            # 获取章节内容(未解密)
            file_name = f'{volume_directory}/{chapter["chapter_id"]}.json'
            encrypted_data = get_chapter_content(file_name)['content']

            # 解密章节内容
            decrypted_data = decrypt_chapter_content(encrypted_data)

            fp.write('\n\n' + chapter['chapter_name'] + '\n\n')    # 写入章节名
            fp.write(decrypted_data)                    # 写入章节内容
