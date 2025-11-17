import requests

def main():
    message = "テスト通知：JR九州遅延チェック"
    line_token = "ZhPSkhFOjbQ18QLNyZeCH+mcdOJW8CYt7yxMBBiGTbCbnq7xOexwKK410s16lQ0vS+SdVyDYWsSRT95G9u2jENRIw3VLvY6X7NKsVGkx225cMIoVZeeKSDkV9fPwrOms/2ccs/bhlvY7YZaDAOcJsAdB04t89/1O/w1cDnyilFU="
    line_user_id = "U799f63217d61fbbdb2aa7591772bb767"

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={"Authorization": f"Bearer {line_token}"},
        json={
            "to": line_user_id,
            "messages": [{"type": "text", "text": message}]
        }
    )

if __name__ == "__main__":
    main()
