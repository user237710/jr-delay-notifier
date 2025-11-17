import requests
from bs4 import BeautifulSoup

url = "https://www.jrkyushu.co.jp/train_status/"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

# 路線ごとのブロックを取得
lines = soup.find_all("div", class_="train_info")

for line in lines:
    name = line.find("h3").get_text(strip=True)
    status = line.find("p").get_text(strip=True)

    if "鹿児島本線" in name:
        print(name, status)


def notify_line(message):
    line_token = "YOUR_LINE_ACCESS_TOKEN"
    line_user_id = "YOUR_USER_ID"

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={"Authorization": f"Bearer " + line_token},
        json={
            "to": line_user_id,
            "messages": [{"type": "text", "text": message}]
        }
    )

# 遅延があれば通知
if "遅延" in status:
    notify_line(f"{name}で遅延が発生しています: {status}")

