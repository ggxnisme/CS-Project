import requests
import schedule
import time
from datetime import datetime
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dieating_bot"
)
cursor = mydb.cursor(buffered=True)
user_id = "U4ce0b39357adc0389954424456349496"


def send_flex_message_to_all():
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer B5PkFP4VMlDVhYqchBr+9fv20YZqQ1XbJZV/A+DTQRAFY0kWaMipXCFgCuJDI5SgFnSbIqM4HQX6uEgRV4ziPEmig5i25ouf6COyvFfNe79dPeXY/LMJnV8qqVZ3klTwCdJLrrdBVg8C+4icyE5TVQdB04t89/1O/w1cDnyilFU="
    }
    date_time = datetime.today()
    formatted_date = date_time.strftime('%Y%m%d')
    formatted_date_str = date_time.strftime('%d/%m/%Y')
    sql = "SELECT * FROM save_detail WHERE user_id = '%s' and DATE(save_date) = '%s'" % (user_id, formatted_date)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    sql_user = "SELECT * FROM user_detail WHERE user_id = '%s'" % (user_id)
    cursor.execute(sql_user)
    result_user = cursor.fetchone()
    print(result_user)
    if (result == []):
        no_cal_result = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": "เหมือนวันนี้คุณจะยังไม่ได้บันทึกอะไรนะ ลองพิมชื่ออาหารแล้วกดบันทึกดูสิ:)"
            }
        ]
        }
        answer_flex = no_cal_result
    else:
        all_kcal, all_protein, all_fat, all_carbs, all_sodium, all_sugar, user_bmr = 0, 0, 0, 0, 0, 0, 0
        user_bmr = result_user[5]
        menu_contents = []
        for i in result:        
          data = i
          sql = "SELECT * FROM food WHERE food_id = {}"
          cursor.execute(sql.format(data[1]))
          food_result = cursor.fetchone()
          all_kcal = all_kcal + food_result[3]
          all_protein = all_protein + food_result[4]
          all_fat = all_fat + food_result[5]
          all_carbs = all_carbs + food_result[6]
          all_sodium = all_sodium + food_result[8]
          all_sugar = all_sugar + food_result[9]
          

          menu_contents.append({
                "type": "text",
                "text": food_result[1], 
                "contents": []
            })
          
          result_flex = {
              "to": user_id,
                "messages": [{
                    "type": "flex",
                    "altText": "This is a Flex Message",
                    "contents": {
                        "type": "bubble",
                        "header": {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 0,
                            "contents": [
                            {
                                "type": "text",
                                "text": "สรุปประจำวัน",
                                "weight": "bold",
                                "size": "md",
                                "align": "center",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": formatted_date_str,
                                "size": "xl",
                                "align": "center",
                                "contents": []
                            }
                            ]
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "action": {
                            "type": "uri",
                            "label": "Action",
                            "uri": "https://linecorp.com"
                            },
                            "contents": [
                            {
                                "type": "text",
                                "text": "สรุปอาหารที่ทานทั้งหมด",
                                "weight": "bold",
                                "align": "center",
                                "contents": []
                            },
                            *menu_contents
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "สรุปโภชนาการรวม",
                                "weight": "bold",
                                "align": "center",
                                "contents": []
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://cdn-icons-png.flaticon.com/128/5550/5550932.png"
                                },
                                {
                                    "type": "text",
                                    "text": "พลังงานรวม",
                                    "weight": "bold",
                                    "color": "#27B300FF",
                                    "margin": "sm",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(round(all_kcal, 2))+" kcal",
                                    "size": "sm",
                                    "color": "#27B300FF",
                                    "align": "end",
                                    "contents": []
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://cdn-icons-png.flaticon.com/128/12918/12918996.png"
                                },
                                {
                                    "type": "text",
                                    "text": "โปรตีนรวม",
                                    "weight": "bold",
                                    "color": "#14A7D7FF",
                                    "flex": 0,
                                    "margin": "sm",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(round(all_protein, 2))+" g",
                                    "size": "sm",
                                    "color": "#14A7D7FF",
                                    "align": "end",
                                    "contents": []
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://cdn-icons-png.flaticon.com/128/7194/7194052.png"
                                },
                                {
                                    "type": "text",
                                    "text": "ไขมันรวม",
                                    "weight": "bold",
                                    "color": "#F3D100FF",
                                    "margin": "sm",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(round(all_fat, 2))+" g",
                                    "size": "sm",
                                    "color": "#E3C300FF",
                                    "align": "end",
                                    "contents": []
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://cdn-icons-png.flaticon.com/128/8493/8493969.png"
                                },
                                {
                                    "type": "text",
                                    "text": "คาร์โบไฮเดรตรวม",
                                    "color": "#8A1ABFFF",
                                    "margin": "sm",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(round(all_carbs, 2))+" g",
                                    "size": "sm",
                                    "color": "#8A1ABFFF",
                                    "align": "end",
                                    "contents": []
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://cdn-icons-png.flaticon.com/128/305/305434.png"
                                },
                                {
                                    "type": "text",
                                    "text": "โซเดียมรวม",
                                    "color": "#1ED2C1FF",
                                    "margin": "sm",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(round(all_sodium, 2))+" mg",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#1ED2C1FF",
                                    "align": "end",
                                    "margin": "xxl",
                                    "contents": []
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://cdn-icons-png.flaticon.com/128/194/194394.png"
                                },
                                {
                                    "type": "text",
                                    "text": "น้ำตาลรวม",
                                    "weight": "bold",
                                    "color": "#FE397BFF",
                                    "margin": "sm",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(round(all_sugar, 2))+" g",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#FE397BFF",
                                    "align": "end",
                                    "margin": "sm",
                                    "contents": []
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://cdn-icons-png.flaticon.com/128/7927/7927615.png"
                                },
                                {
                                    "type": "text",
                                    "text": "BMR",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#000000FF",
                                    "align": "start",
                                    "margin": "sm",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(user_bmr)+" kcal",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#000000FF",
                                    "align": "end",
                                    "margin": "sm",
                                    "contents": []
                                }
                                ]
                            },
                            {
                                "text": "ข้อมูลทั้งหมดเป็นเพียงการคำนวณจากเมนูอาหาร",
                                "type": "text",
                                "contents": [],
                                "color": "#AAAAAA",
                                "margin": "lg",
                                "size": "xs"
                            },
                            {
                                "text": "ที่ผู้ใช้งานเพิ่มผ่าน LINE Chat นี้เท่านั้น",
                                "type": "text",
                                "contents": [],
                                "color": "#AAAAAA",
                                "margin": "lg",
                                "size": "xs"
                            },
                            {
                                "type": "button",
                                "action": {
                                "type": "message",
                                "label": "ดูสรุปย้อนหลัง",
                                "text": "ดูสรุปย้อนหลัง"
                                }
                            },
                            {
                                "type": "spacer",
                                "size": "xs"
                            }
                            ]
                        }
                    }
                }]
                }
        answer_flex = result_flex
    response = requests.post(url, headers=headers, json=answer_flex)
    print(response.text)

send_flex_message_to_all()