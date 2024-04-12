import requests
import schedule
import time
from datetime import datetime

def send_flex_message_to_all():
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer B5PkFP4VMlDVhYqchBr+9fv20YZqQ1XbJZV/A+DTQRAFY0kWaMipXCFgCuJDI5SgFnSbIqM4HQX6uEgRV4ziPEmig5i25ouf6COyvFfNe79dPeXY/LMJnV8qqVZ3klTwCdJLrrdBVg8C+4icyE5TVQdB04t89/1O/w1cDnyilFU="
    }
    data = {
        "messages": [
            {
                "type": "text",
                "text": "ได้ดื่มน้ำบ้างไหม ดื่มน้ำหน่อยสิ อย่าปล่อยให้ร่างกายขาดน้ำละ :)"
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

send_flex_message_to_all()