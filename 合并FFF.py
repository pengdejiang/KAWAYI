import urllib.request
from urllib.parse import urlparse
from datetime import datetime, timedelta, timezone
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import tempfile
from datetime import datetime
import os

# 用于存储从每个URL读取的内容
all_lines = []

def process_url(url):
    try:
        # 创建一个请求对象并添加自定义header
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

        # 打开URL并读取内容
        with urllib.request.urlopen(req) as response:
            # 以二进制方式读取数据，然后解码为字符串
            text = response.read().decode('utf-8')
            # 将读取的内容按行存储到all_lines列表中（这里保持原样，不进行任何修改）
            all_lines.extend(text.split('\n'))
            # 打印读取的行数（可选，用于调试）
            print(f"从{url}读取OK")

    except Exception as e:
        print(f"处理URL {url} 时发生错误：{e}")

# 定义要处理的URL列表
urls = [
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%8C%97%E4%BA%AC%E8%81%94%E9%80%9AFFF.txt",#北京联通
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%94%B5%E4%BF%A1FFF.txt",#四川电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%9B%9B%E5%B7%9D%E8%81%94%E9%80%9AFFF.txt",#四川联通
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%A4%A9%E6%B4%A5%E8%81%94%E9%80%9AFFF.txt",#天津联通
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%AE%89%E5%BE%BD%E7%94%B5%E4%BF%A1FFF.txt",#安徽电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%B1%B1%E4%B8%9C%E7%94%B5%E4%BF%A1FFF.txt",#山东电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%B1%B1%E8%A5%BF%E8%81%94%E9%80%9AFFF.txt",#山西联通
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%B9%BF%E4%B8%9C%E7%94%B5%E4%BF%A1FFF.txt",#广东电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%B9%BF%E8%A5%BF%E7%94%B5%E4%BF%A1FFF.txt",#广西电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B1%9F%E8%8B%8F%E7%94%B5%E4%BF%A1FFF.txt",#江苏电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B2%B3%E5%8C%97%E7%94%B5%E4%BF%A1FFF.txt",#河北电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B2%B3%E5%8D%97%E7%94%B5%E4%BF%A1FFF.txt",#河南电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B2%B3%E5%8D%97%E8%81%94%E9%80%9AFFF.txt",#河南联通
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B5%99%E6%B1%9F%E7%94%B5%E4%BF%A1FFF.txt",#浙江电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B9%96%E5%8C%97%E7%94%B5%E4%BF%A1FFF.txt",#湖北电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B9%96%E5%8D%97%E7%94%B5%E4%BF%A1FFF.txt",#湖南电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E8%B4%B5%E5%B7%9E%E7%94%B5%E4%BF%A1FFF.txt",#贵州电信
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E8%BE%BD%E5%AE%81%E8%81%94%E9%80%9AFFF.txt",#辽宁联通
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E9%87%8D%E5%BA%86%E7%94%B5%E4%BF%A1FFF.txt",#重庆电信

]

# 处理每个URL
for url in urls:
    if url.startswith("http"):
        print(f"处理URL: {url}")
        process_url(url)

# 定义输出文件路径
output_file = "speedtest/result/hebing-FFF.txt"

# 确保输出文件所在的目录存在（如果不存在则创建）
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# 将合并后的文本写入文件
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            # 写入文件时，如果line不为空字符串则添加换行符，否则只写入空行（保持原样）
            f.write(line + '\n' if line.strip() else '\n')
    print(f"合并后的文本已保存到文件: {output_file}")

except Exception as e:
    print(f"保存文件时发生错误：{e}")
