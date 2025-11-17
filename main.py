import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# LINE通知関数
def notify_line(message):
    line_token = "ZhPSkhFOjbQ18QLNyZeCH+mcdOJW8CYt7yxMBBiGTbCbnq7xOexwKK410s16lQ0vS+SdVyDYWsSRT95G9u2jENRIw3VLvY6X7NKsVGkx225cMIoVZeeKSDkV9fPwrOms/2ccs/bhlvY7YZaDAOcJsAdB04t89/1O/w1cDnyilFU="
    line_user_id = "U799f63217d61fbbdb2aa7591772bb767"
    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={"Authorization": f"Bearer " + line_token},
        json={
            "to": line_user_id,
            "messages": [{"type": "text", "text": message}]
        }
    )

# Google Sheets接続
def connect_sheets():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("JR九州遅延ログ").sheet1
    return sheet

# 遅延情報取得
def get_delay_info():
    url = "https://www.jrkyushu.co.jp/train_status/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    delays = {}
    lines = soup.find_all("div", class_="train_info")
    for line in lines:
        name = line.find("h3").get_text(strip=True)
        status = line.find("p").get_text(strip=True)
        delays[name] = status
    return delays

# 差分チェック
def check_and_log():
    sheet = connect_sheets()
    delays = get_delay_info()

    for line, status in delays.items():
        # 前回の状態をSheetsから取得（例: 最終行を検索）
        records = sheet.get_all_records()
        prev_status = None
        for r in records[::-1]:  # 最新から逆順に見る
            if r["路線"] == line:
                prev_status = r["状態"]
                break

        # 差分がある場合のみ処理
        if prev_status != status:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([line, status, now])

            if "遅延" in status and (prev_status is None or "遅延" not in prev_status):
                notify_line(f"🚨 {line}で遅延が発生しました: {status}")
            elif "遅延" not in status and prev_status and "遅延" in prev_status:
                notify_line(f"✅ {line}の遅延が解消しました: {status}")

if __name__ == "__main__":
    check_and_log()
