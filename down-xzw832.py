import os
import shutil
import subprocess
import threading
import time
from git import Repo, NoSuchPathError, InvalidGitRepositoryError
from dulwich import porcelain
import requests

# 定义变量
#如果有本地文件 先删除
#file_to_delete = 'S_weishi.txt'
file_url = 'https://raw.githubusercontent.com/xzw832/cmys/refs/heads/main/S_weishi.txt'
download_path = './'

# 删除指定目录下的文件
try:
    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
        print(f"文件 {file_to_delete} 已成功删除。")
    else:
        print(f"文件 {file_to_delete} 不存在，无需删除。")
except Exception as e:
    print(f"删除文件时出错: {e}")

# 从URL下载新文件到指定目录
try:
    # 发送HTTP GET请求到文件URL
    response = requests.get(file_url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 定义本地文件路径
        local_file_path = os.path.join(download_path, 'S_weishi.txt')

        # 将文件内容写入到本地
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print(f"文件已成功下载到 {local_file_path}")
    else:
        print(f"下载文件时出错，状态码: {response.status_code}")
except Exception as e:
    print(f"下载文件时出错: {e}")
	