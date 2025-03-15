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
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%8C%97%E4%BA%AC%E8%81%94%E9%80%9AFFF.txt?token=GHSAT0AAAAAADASAPVFLES225RZAP5BCMPAZ6V3WUQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVFKT3SXZHBGQV76OPUZ6V3XDQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%9B%9B%E5%B7%9D%E8%81%94%E9%80%9AFFF.txt?token=GHSAT0AAAAAADASAPVEXXETVGGJIEVZWGFCZ6V3YDA",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%A4%A9%E6%B4%A5%E8%81%94%E9%80%9AFFF.txt?token=GHSAT0AAAAAADASAPVFPKR3EWHSCEED2O74Z6V3ZPQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%AE%89%E5%BE%BD%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVET6I23ISHDLQSSHWQZ6V3Z3A",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%B1%B1%E4%B8%9C%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVFZON6LBUBRHTCK2O6Z6V32EQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%B1%B1%E8%A5%BF%E8%81%94%E9%80%9AFFF.txt?token=GHSAT0AAAAAADASAPVFO7PA3RQBA7FSO7NMZ6V32OA",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%B9%BF%E4%B8%9C%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVEWITHKPLNSTSDHGU2Z6V32YQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E5%B9%BF%E8%A5%BF%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVE7G4EWP2RK462LYD4Z6V33AA",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B1%9F%E8%8B%8F%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVFR4RRS4OEJ55NJMA6Z6V33JQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B2%B3%E5%8D%97%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVETEQLPGWPRPJNR7UCZ6V33VQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B2%B3%E5%8D%97%E8%81%94%E9%80%9AFFF.txt?token=GHSAT0AAAAAADASAPVF62HENOMZ5PWQHWQ6Z6V34KQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E6%B9%96%E5%8D%97%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVE2B4LMYYJWKAP7CACZ6V34VQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E8%B4%B5%E5%B7%9E%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVFUTQ473SNVIRP4QQGZ6V347A",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E8%BE%BD%E5%AE%81%E8%81%94%E9%80%9AFFF.txt?token=GHSAT0AAAAAADASAPVF5X3IVR56HQPHOFXYZ6V35GQ",
"https://raw.githubusercontent.com/pengdejiang/KAWAYI/refs/heads/main/%E9%87%8D%E5%BA%86%E7%94%B5%E4%BF%A1FFF.txt?token=GHSAT0AAAAAADASAPVEZM5ND2W5ZAPJO7DWZ6V35PQ",
	
]

# 处理每个URL
for url in urls:
    if url.startswith("http"):
        print(f"处理URL: {url}")
        process_url(url)

# 定义输出文件路径
output_file = "reaslt-CAIJI-out-all/hebing-FFF.txt"

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
