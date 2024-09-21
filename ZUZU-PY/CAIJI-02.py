import os
import requests
import re
import base64
import cv2
import datetime
from datetime import datetime
from bs4 import BeautifulSoup

# 获取rtp目录下的文件名
files = os.listdir('rtp-02')

files_name = []

# 去除后缀名并保存至provinces_isps
for file in files:
    name, extension = os.path.splitext(file)
    files_name.append(name)

# 忽略不符合要求的文件名
provinces_isps = [name for name in files_name if name.count('_') == 1]

# 打印结果
print(f"本次查询：{provinces_isps}的组播节目")

keywords = []

for province_isp in provinces_isps:
    # 读取文件并删除空白行
    try:
        with open(f'rtp/{province_isp}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines if line.strip()]
        # 获取第一行中以包含 "rtp://" 的值作为 mcast
        if lines:
            first_line = lines[0]
            if "rtp://" in first_line:
                mcast = first_line.split("rtp://")[1].split(" ")[0]
                keywords.append(province_isp + "_" + mcast)
    except FileNotFoundError:
        print(f"文件 '{province_isp}.txt' 不存在. 跳过此文件.")

for keyword in keywords:
    province, isp, mcast = keyword.split("_")
    # 根据不同的 isp 设置不同的 org 值
    if province == "北京" and isp == "联通":
        org = "China Unicom Beijing Province Network"
    elif isp == "联通":
        org = "CHINA UNICOM China169 Backbone"
    elif isp == "电信":
        org = "Chinanet"
    elif isp == "移动":
        org = "China Mobile communications corporation"

    current_time = datetime.now()  # 获取当前时间
    timeout_cnt = 0   # 初始化超时计数器
	html_content_history = []  # 用于存储HTML响应内容的历史记录
    result_urls = set()  # 初始化一个集合来存储结果URL
	same_html_count = 0  # 初始化HTML内容相同的计数器
    while len(result_urls) == 0 and timeout_cnt <= 5 and same_html_count < 20:  # 循环直到找到结果URL、超时次数超过5次或HTML相同20次
        try:
            # 构造搜索URL的基础部分			
            search_url = 'https://fofa.info/result?qbase64='
			# 构造搜索文本，包括目标名称、国家和区域
            search_txt = f'\"Rozhuk\" && country=\"CN\" && region=\"{province}\"'
			# 将搜索文本编码为UTF-8，然后转换为base64编码
            bytes_string = search_txt.encode('utf-8')			
            search_txt = base64.b64encode(bytes_string).decode('utf-8')
			# 将base64编码的搜索文本添加到搜索URL中
            search_url += search_txt
			# 打印当前时间和搜索URL
            print(f"{current_time} 查询运营商 : {province}{isp} ，查询网址 : {search_url}")
			# 发送GET请求到搜索URL
            response = requests.get(search_url, timeout=30)
			# 检查请求是否成功
            response.raise_for_status()
			# 获取响应的HTML内容
            html_content = response.text
			        # 检查HTML内容是否与上一次相同
            if html_content_history and html_content == html_content_history[-1]:
                same_html_count += 1
            else:
                same_html_count = 0  # 重置计数器

            # 更新HTML内容历史记录
            html_content_history.append(html_content)
								
			# 使用BeautifulSoup解析HTML内容
            html_soup = BeautifulSoup(html_content, "html.parser")
			# 定义正则表达式来查找IP地址和端口
            pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"
			# 使用正则表达式查找所有匹配的URL
            urls_all = re.findall(pattern, html_content)
			# 将找到的URL转换为集合，去除重复项
            result_urls = set(urls_all)
			# 打印当前时间和找到的URL集合
            print(f"{current_time} result_urls:{result_urls}")
            # 初始化一个列表来存储有效的IP地址
            valid_ips = []

            # 遍历所有视频链接
            for url in result_urls:
                video_url = url + "/rtp/" + mcast

                # 用OpenCV读取视频
                cap = cv2.VideoCapture(video_url)

                # 检查视频是否成功打开
                if not cap.isOpened():
                    print(f"{current_time} {video_url} 无效")
                    continue  # Skip to the next URL

                # 读取视频的宽度和高度
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
				# 打印视频URL和分辨率
                print(f"{current_time} {video_url} 的分辨率为 {width}x{height}")
                # 如果视频的宽度和高度都大于0，则认为该IP地址有效
                if width > 0 and height > 0:
                    valid_ips.append(url)
				# 释放VideoCapture对象	
                cap.release()
                # 如果找到了有效的IP地址
            if valid_ips:
				# 读取现有的RTP文件内容
                rtp_filename = f'rtp/{province}_{isp}.txt'
                with open(rtp_filename, 'r', encoding='utf-8') as file:
                    data = file.read()
				# 构造新的文件名	
                txt_filename = f'{province}{isp}CJ-02.txt'
				# 写入新的文件内容，替换RTP URL
                with open(txt_filename, 'w') as new_file:
                    for url in valid_ips:
                        new_data = data.replace("rtp://", f"{url}/rtp/")
                        new_file.write(new_data)
                # 打印生成的文件名和保存位置
                print(f'已生成播放列表，保存至{txt_filename}')
            else:
				# 如果没有找到有效的IP地址
                print(f"未找到合适的 IP 地址。")
       # 尝试捕获两种异常：requests.Timeout 和 requests.RequestException
        except (requests.Timeout, requests.RequestException) as e:
		    print(f"{current_time} 请求错误: {e}")
			# 如果发生超时或请求异常，增加超时计数器
            timeout_cnt += 1
		    # 检查是否因为HTML内容相同20次而跳出循环
        if same_html_count == 20:
            print(f"{current_time} HTML内容连续20次相同，跳出循环。")
            break
	        # 移除html_content_history中最后一个元素（因为是最新的HTML内容，可能不是重复的）
    html_content_history.pop()	
				
			# 打印当前时间和发生超时的省份，以及异常次数
            print(f"{current_time} [{province}]搜索请求发生超时，异常次数：{timeout_cnt}")
			# 判断超时次数是否超过5次
            if timeout_cnt <= 5:
		    # 如果没有超过5次，则继续执行循环，尝试重新发送请求
                continue
            else:
			# 如果超过5次，则打印错误信息并停止处理	
                print(f"{current_time} 搜索IPTV频道源[]，超时次数过多：{timeout_cnt} 次，停止处理")
print('节目表制作完成！ 文件输出在当前文件夹！')
