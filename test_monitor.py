import requests
from bs4 import BeautifulSoup
import os

BARK_KEY = os.getenv('BARK_KEY')
# 换一个极其稳定的页面：雅虎日本帮助页，几乎不换结构
TARGET_URL = "https://www.yahoo.co.jp/"
STATUS_FILE = "last_news.txt"

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'}
    try:
        res = requests.get(TARGET_URL, headers=headers, timeout=15)
        print(f"HTTP 状态码: {res.status_code}") # 确认网络通不通
        
        soup = BeautifulSoup(res.text, 'html.parser')
        # 直接抓页面上的任意文本进行对比
        content = soup.find('title').get_text()
        print(f"抓取到的网页标题: {content}")

        # 暴力验证法：手动制造一个“内容变动”
        # 我们每次运行都加上当前时间戳，确保内容永远和上次不一样
        import time
        current_data = f"{content} - {time.time()}" 

        # 发送推送
        msg = f"验证成功！系统正在监控中。当前时间戳：{time.time()}"
        print("准备发送 Bark 推送...")
        requests.get(f"https://api.day.app/{BARK_KEY}/{msg}?group=Verify")
        
        # 更新文件
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            f.write(current_data)
        print("推送已发出，请查看手机历史记录")

    except Exception as e:
        print(f"还是失败了，错误原因: {e}")

if __name__ == "__main__":
    main()
