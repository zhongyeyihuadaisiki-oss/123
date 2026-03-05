import requests
from bs4 import BeautifulSoup
import os

BARK_KEY = os.getenv('BARK_KEY')
# 监控 LivePocket 鸣潮搜索结果页
TARGET_URL = "https://t.livepocket.jp/p/search?search_word=%E9%B3%B4%E6%BD%AE"
STATUS_FILE = "last_event_count.txt"

def send_notification(count):
    if not BARK_KEY: return
    title = "【鸣潮抢票雷达】"
    body = f"检测到 LivePocket 变动！当前共有 {count} 个项目，请尽快查看！"
    # level=active 确保响铃；url 让点击通知直接跳转抢票页
    api_url = f"https://api.day.app/{BARK_KEY}/{title}/{body}?url={TARGET_URL}&level=active&isArchive=1&group=WutheringWaves"
    requests.get(api_url)

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'}
    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 统计 LivePocket 上的鸣潮活动列表项
        events = soup.select('.list_item')
        current_count = len(events)
        print(f"当前活动总数: {current_count}")

        last_count = 0
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, 'r') as f:
                content = f.read().strip()
                last_count = int(content) if content.isdigit() else 0
        
        # 只要数量和上次不一样（通常是增加），就发推送
        if current_count != last_count:
            send_notification(current_count)
            with open(STATUS_FILE, 'w') as f:
                f.write(str(current_count))
            print(f"检测到变动，推送已发出：{current_count}")
        else:
            print("数量未变，继续监控中...")
            
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    main()
