import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# 生成当日页面URL
today = datetime.now()
date_str = today.strftime("%Y-%m-%d")
url = f"https://daily.juya.uk/issues/{date_str}/"
crawl_time = today.strftime("%Y-%m-%d %H:%M:%S")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # ✅ 只取 main#main-content 里面的内容
    main_tag = soup.select_one("main#main-content")
    if not main_tag:
        email_body = "<p>⚠️ 未找到 main#main-content，今日日报可能还未发布</p>"
    else:
        # 获取main内部原始HTML，保留全部文字、超链接、图片、标题列表
        email_body = str(main_tag)

    # 组装完整邮件HTML，增加基础样式，防止邮件客户端乱排版
    email_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{font-family: system-ui, sans-serif; font-size:15px; line-height:1.6;}}
img {{max-width:100%; height:auto;}}
hr {{border:0; border-top:1px solid #aaa; margin:1.5rem 0;}}
a {{color:#2563eb;}}
</style>
</head>
<body>
<h2>📰 AI早报 {date_str}</h2>
<p>抓取页面地址：<a href="{url}">{url}</a></p>
<p>抓取时间戳：{crawl_time}</p>
<hr>
{email_body}
</body>
</html>
"""

except Exception as e:
    email_html = f"""
<!DOCTYPE html>
<html>
<body>
<h2>❌ 抓取失败</h2>
<p>目标页面：{url}</p>
<p>抓取时间：{crawl_time}</p>
<p>错误信息：{str(e)}</p>
</body>
</html>
"""

with open("mail.html", "w", encoding="utf-8") as f:
    f.write(email_html)
