import requests
from bs4 import BeautifulSoup
import os

# --- 配置 ---
BARK_KEY = os.getenv('BARK_KEY') # 在 GitHub Secrets 中配置
TARGET_URL = "https://news.yahoo.co.jp/topics/top-picks"
STATUS_FILE = "last_news.txt"

def send_notification(news_title):
    if not BARK_KEY:
        print("错误：未配置 BARK_KEY")
        return
    # 编码通知内容
    msg = f"测试成功！日本雅虎新头条：{news_title}"
    url = f"https://api.day.app/{BARK_KEY}/{msg}?isArchive=1&group=Test"
    requests.get(url)

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }
    
    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取雅虎新闻头条的标题
        # 雅虎的结构很稳，头条通常在 sc-xxxx 这种类名下的 li 里，我们直接找 a 标签
        news_items = soup.select('ul.newsFeed_list li a')
        if not news_items:
            print("未能抓取到新闻，可能是页面结构变了")
            return

        current_top_news = news_items[0].get_text(strip=True)
        print(f"当前最新新闻: {current_top_news}")

        # 读取上次记录的新闻标题
        last_news = ""
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                last_news = f.read().strip()
        
        # 对比
        if current_top_news != last_news:
            print("检测到内容更新，准备发送通知...")
            send_notification(current_top_news)
            
            # 更新本地文件以供下次对比
            with open(STATUS_FILE, 'w', encoding='utf-8') as f:
                f.write(current_top_news)
        else:
            print("内容未发生变化，跳过通知。")
            
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    main()
