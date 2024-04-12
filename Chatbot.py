#Import Library
import mysql.connector
import json
from datetime import datetime
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dieating_bot"
)
cursor = mydb.cursor(buffered=True)
import json
import os
from flask import Flask, jsonify, render_template_string
from flask import request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import PostbackEvent

# Flask
app = Flask(__name__)
configuration = Configuration('B5PkFP4VMlDVhYqchBr+9fv20YZqQ1XbJZV/A+DTQRAFY0kWaMipXCFgCuJDI5SgFnSbIqM4HQX6uEgRV4ziPEmig5i25ouf6COyvFfNe79dPeXY/LMJnV8qqVZ3klTwCdJLrrdBVg8C+4icyE5TVQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('791683a66db4e6aa130ea57fcd352157')

'''@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
        print(body)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(PostbackEvent)
def handle_postback(event):
    # Assuming PostbackContent exists and contains the needed datetime data
    postback_data = event.postback.data  # The data returned by the postback action, typically you'd use it to distinguish actions
    params = event.postback.params  # This should include 'date' or 'time' selected by the datetimepicker
    
    if params and 'date' in params:
        selected_date = params['date']
        # Process the selected date
        # Echo back the selected date as a confirmation or further processing
        reply_with_text(event.reply_token, f"You selected the date: {selected_date}")
    elif params and 'time' in params:
        selected_time = params['time']
        # Process the selected time
        # Echo back the selected time
        reply_with_text(event.reply_token, f"You selected the time: {selected_time}")

def reply_with_text(reply_token, text):
    api_client = ApiClient(configuration)
    line_bot_api = MessagingApi(api_client)
    reply_message = ReplyMessageRequestืเพนา 
        reply_token=reply_token,
        messages=[TextMessage(text=text)]
    )
    line_bot_api.reply_message_with_http_info(reply_message)'''

@app.route('/', methods=['POST'])

def Mainfuction():

    #รับ intent จาก Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    #เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    answer_from_bot = generating_answer(question_from_dailogflow_raw)

    return jsonify(answer_from_bot)

def generating_answer(question_from_dailogflow_dict):

    #Print intent ที่รับมาจาก Dailogflow
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #เก็บค่า ชื่อของ intent ที่รับมาจาก Dailogflow
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"] 

    #ลูปตัวเลือกของฟังก์ชั่นสำหรับตอบคำถามกลับ
    if intent_group_question_str == 'ปริมาณแคลอรี่ต่อวันชาย':
        answer_str = BMRMale(question_from_dailogflow_dict)
    elif intent_group_question_str == 'ปริมาณแคลอรี่ต่อวันหญิง':
        answer_str = BMRFemale(question_from_dailogflow_dict)    
    elif intent_group_question_str == 'เมนูอาหาร':
        answer_str = food_cal(question_from_dailogflow_dict)
    elif intent_group_question_str == 'คำนวณปริมาณแคลอรี่ต่อวัน':
        answer_str = BMR(question_from_dailogflow_dict)
    elif intent_group_question_str == 'แก้ไขคำนวณปริมาณแคลอรี่ต่อวัน':
        answer_str = changeBMR()
    elif intent_group_question_str == 'สรุปแคลอรี่':
        answer_str = cal_result(question_from_dailogflow_dict)
    elif intent_group_question_str == 'บันทึกแคลอรี่':
        answer_str = save_cal(question_from_dailogflow_dict)
    elif intent_group_question_str == 'วันที่ย้อนหลัง':
        answer_str = past_cal_result(question_from_dailogflow_dict)
    elif intent_group_question_str == 'แนะนำเมนูอาหารเพื่อสุขภาพ':
        answer_str = healthy_food()
    else: answer_str = 'ไม่เข้าใจ คุณต้องการอะไร'

    #สร้างการแสดงของ dict
    answer_from_bot = answer_str
    #แปลงจาก dict ให้เป็น JSON
    return answer_from_bot

def healthy_food():
    try:
      healthy_mess = {
          "fulfillmentMessages": [
        {
          "payload": {
            "line": {
              "altText": "this is an image carousel template",
              "type": "template",
              "template": {
                "type": "image_carousel",
                "columns": [
                  {
                    "action": {
                      "uri": "https://vogue.co.th/beauty/wellness-healthy-food",
                      "label": "Vogue Beauty",
                      "type": "uri"
                    },
                    "imageUrl": "https://lh5.googleusercontent.com/d/11-0UG1sMSSMj14VcV4qhZZ6bV2GcoHWO"
                  },
                  {
                    "action": {
                      "type": "uri",
                      "label": "Wongnai",
                      "uri": "https://www.wongnai.com/cooking/cookbooks/healthy-food-recipes"
                    },
                    "imageUrl": "https://lh5.googleusercontent.com/d/1DN0E9lwXobOkV1Pjfnf9mOTgjytY1YgQ"
                  }
                ]
              }
            }
          },
          "platform": "LINE"
        }
      ]
      }
      return healthy_mess
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex
    
def changeBMR(): #เปลี่ยนแปลง BMR
    try:
      flex_changebmr = {
            "fulfillmentMessages": [
            {
              "payload": {
                "line": {
                  "type": "template",
                  "altText": "this is a confirm template",
                  "template": {
                    "type": "confirm",
                    "actions": [
                      {
                        "label": "ชาย",
                        "text": "คำนวณปริมาณแคลอรี่ต่อวันของผู้ชาย",
                        "type": "message"
                      },
                      {
                        "text": "คำนวณปริมาณแคลอรี่ต่อวันของผู้หญิง",
                        "type": "message",
                        "label": "หญิง"
                      }
                    ],
                    "text": "ระบุเพศสภาพ"
                  }
                }
              },
              "platform": "LINE"
            },
            {
              "text": {
                "text": [
                  ""
                ]
              }
            }
          ]
          }
      return flex_changebmr
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex

def BMR(respond_dict): #คำนวน BMR
    try:
      user_id = respond_dict['originalDetectIntentRequest']['payload']['data']['source']['userId']
      sql = "SELECT * FROM user_detail WHERE user_id = '{}'"
      cursor.execute(sql.format(user_id))
      result = cursor.fetchone()
      if (result is not None and result[0] == user_id):
        flex_bmr = {
        "fulfillmentMessages": [
          {
            "payload": {
              "line": {
                "altText": "Flex Message",
                "contents": {
                  "footer": {
                    "contents": [
                      {
                        "type": "spacer"
                      },
                      {
                        "spacing": "sm",
                        "type": "box",
                        "contents": [
                          {
                            "type": "box",
                            "contents": [
                              {
                                "color": "#000000FF",
                                "margin": "sm",
                                "type": "text",
                                "size": "xl",
                                "text": "BMR",
                                "weight": "bold",
                                "contents": []
                              },
                              {
                                "text": str(round(result[5], 1))+" kcal",
                                "type": "text",
                                "size": "xl",
                                "contents": [],
                                "align": "end",
                                "weight": "bold"
                              }
                            ],
                            "layout": "baseline"
                          }
                        ],
                        "layout": "vertical"
                      },
                      {
                        "size": "xs",
                        "margin": "sm",
                        "color": "#AAAAAA",
                        "contents": [],
                        "text": "คือ อัตราการความต้องการเผาผลาญของร่างกาย",
                        "type": "text",
                      },
                      {
                        "size": "xs",
                        "margin": "sm",
                        "color": "#AAAAAA",
                        "contents": [],
                        "text": "หรือจำนวนแคลอรี่ขั้นต่ำที่ต้องการใช้ในชีวิตแต่ละวัน",
                        "type": "text",
                      },
                      {
                        "action": {
                          "label": "แก้ไข",
                          "text": "แก้ไขคำนวณปริมาณแคลอรี่ต่อวัน",
                          "type": "message"
                        },
                        "color": "#19B500FF",
                        "margin": "sm",
                        "type": "button"
                      }
                    ],
                    "layout": "vertical",
                    "type": "box"
                  },
                  "body": {
                    "type": "box",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "url": "https://cdn-icons-png.flaticon.com/128/10109/10109492.png"
                              },
                              {
                                "margin": "sm",
                                "color": "#000000FF",
                                "type": "text",
                                "weight": "bold",
                                "text": "เพศ",
                                "contents": []
                              },
                              {
                                "text": str(result[1]),
                                "contents": [],
                                "type": "text",
                                "align": "end",
                                "color": "#000000FF",
                                "size": "sm"
                              }
                            ]
                          },
                          {
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/3787/3787837.png",
                                "type": "icon"
                              },
                              {
                                "color": "#000000FF",
                                "weight": "bold",
                                "text": "อายุ",
                                "margin": "sm",
                                "contents": [],
                                "type": "text"
                              },
                              {
                                "align": "end",
                                "contents": [],
                                "color": "#000000FF",
                                "text": str(result[4]),
                                "type": "text",
                                "size": "sm"
                              }
                            ],
                            "layout": "baseline",
                            "type": "box"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/866/866711.png",
                                "type": "icon"
                              },
                              {
                                "weight": "bold",
                                "text": "น้ำหนัก",
                                "color": "#000000FF",
                                "type": "text",
                                "contents": [],
                                "margin": "sm"
                              },
                              {
                                "type": "text",
                                "contents": [],
                                "color": "#000000FF",
                                "size": "sm",
                                "align": "end",
                                "text": str(result[2])+" kg"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "url": "https://cdn-icons-png.flaticon.com/128/7410/7410369.png"
                              },
                              {
                                "contents": [],
                                "color": "#000000FF",
                                "margin": "sm",
                                "type": "text",
                                "text": "ส่วนสูง",
                                "weight": "bold"
                              },
                              {
                                "type": "text",
                                "text": str(result[3])+" cm",
                                "size": "sm",
                                "contents": [],
                                "color": "#000000FF",
                                "align": "end"
                              }
                            ]
                          }
                        ],
                        "spacing": "sm"
                      }
                    ],
                    "layout": "vertical",
                    "spacing": "md",
                    "action": {
                      "type": "uri",
                      "uri": "https://linecorp.com",
                      "label": "Action"
                    }
                  },
                  "type": "bubble"
                },
                "type": "flex"
              }
            },
            "platform": "LINE"
          },
          {
            "text": {
              "text": [
                ""
              ]
            }
          }
        ]
        }
        return flex_bmr
      elif (result is None):
          flex_nobmr = {
            "fulfillmentMessages": [
            {
              "payload": {
                "line": {
                  "type": "template",
                  "altText": "this is a confirm template",
                  "template": {
                    "type": "confirm",
                    "actions": [
                      {
                        "label": "ชาย",
                        "text": "คำนวณปริมาณแคลอรี่ต่อวันของผู้ชาย",
                        "type": "message"
                      },
                      {
                        "text": "คำนวณปริมาณแคลอรี่ต่อวันของผู้หญิง",
                        "type": "message",
                        "label": "หญิง"
                      }
                    ],
                    "text": "ระบุเพศสภาพ"
                  }
                }
              },
              "platform": "LINE"
            },
            {
              "text": {
                "text": [
                  ""
                ]
              }
            }
          ]
          }
          return flex_nobmr
      else:
          print("No result found in the database")
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex


def food_cal(respond_dict): #ฟังก์ชั่นสำหรับบอกแคลลอรี่ในอาหาร
    try:
      food = str(respond_dict["queryResult"]["parameters"]["Food"])
      sql = "SELECT * FROM food WHERE food_thai = '{}'"
      cursor.execute(sql.format(food))
      result = cursor.fetchone()
      if (result is None):
          no_menu = {
              "fulfillmentMessages": [
            {
              "text": {
                "text": [
                  "โอ๊ะเหมือนเราจะไม่มีเมนูนี้นะ"
                ]
              },
              "platform": "LINE"
            },
            {
              "payload": {
                "line": {
                  "type": "template",
                  "altText": "this is a confirm template",
                  "template": {
                    "type": "confirm",
                    "actions": [
                      {
                        "label": "เริ่มเลย",
                        "uri": "https://liff.line.me/2003832737-KyxVgqqA",
                        "type": "uri"
                      },
                      {
                        "text": "ไม่เป็นไร คุณสามารถเพิ่มเมนูนี้ได้ด้วยตัวเองโดยกดปุ่มในเมนูนะะ",
                        "type": "message",
                        "label": "ไว้ทีหลัง"
                      }
                    ],
                    "text": "เพิ่มเมนูนี้กันเถอะ"
                  }
                }
              },
              "platform": "LINE"
            }
          ]
          }
          answer_bot = no_menu
      else: 
          global food_id
          food_id = str(result[0])
          #answer_function = "{} \n\n พลังงาน = {} kcal \n โปรตีน = {} g\n คาร์โบไฮเดรต = {} g\n ไขมัน = {} g\n ไฟเบอร์ = {} g\n โซเดียม = {} g\n น้ำตาล {} g\n"
          flex = {
              "fulfillmentMessages": [
            {
              "payload": {
                "line": {
                  "altText": "Flex Message",
                  "contents": {
                    "body": {
                      "spacing": "md",
                      "action": {
                        "type": "uri",
                        "label": "Action",
                        "uri": "https://linecorp.com"
                      },
                      "layout": "vertical",
                      "contents": [
                        {
                          "text": str(result[1]),
                          "type": "text",
                          "weight": "bold",
                          "contents": [],
                          "size": "xl"
                        },
                        {
                          "type": "box",
                          "spacing": "sm",
                          "contents": [
                            {
                              "layout": "baseline",
                              "type": "box",
                              "contents": [
                                {
                                  "url": "https://cdn-icons-png.flaticon.com/128/5550/5550932.png",
                                  "type": "icon"
                                },
                                {
                                  "weight": "bold",
                                  "text": "พลังงาน",
                                  "contents": [],
                                  "color": "#27B300FF",
                                  "margin": "sm",
                                  "type": "text"
                                },
                                {
                                  "text": str(result[3])+" kcal",
                                  "type": "text",
                                  "contents": [],
                                  "size": "sm",
                                  "align": "end",
                                  "color": "#27B300FF"
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
                                  "text": "โปรตีน",
                                  "color": "#14A7D7FF",
                                  "contents": [],
                                  "weight": "bold",
                                  "margin": "sm",
                                  "type": "text"
                                },
                                {
                                  "align": "end",
                                  "contents": [],
                                  "text": str(round(result[4], 2))+" g",
                                  "size": "sm",
                                  "type": "text",
                                  "color": "#14A7D7FF"
                                }
                              ]
                            },
                            {
                              "type": "box",
                              "contents": [
                                {
                                  "type": "icon",
                                  "url": "https://cdn-icons-png.flaticon.com/128/7194/7194052.png"
                                },
                                {
                                  "text": "ไขมัน",
                                  "contents": [],
                                  "margin": "sm",
                                  "type": "text",
                                  "color": "#F3D100FF",
                                  "weight": "bold"
                                },
                                {
                                  "contents": [],
                                  "size": "sm",
                                  "color": "#E3C300FF",
                                  "type": "text",
                                  "text": str(round(result[5], 2))+" g",
                                  "align": "end"
                                }
                              ],
                              "layout": "baseline"
                            },
                            {
                              "layout": "baseline",
                              "type": "box",
                              "contents": [
                                {
                                  "url": "https://cdn-icons-png.flaticon.com/128/8493/8493969.png",
                                  "type": "icon"
                                },
                                {
                                  "contents": [],
                                  "margin": "sm",
                                  "text": "คาร์โบไฮเดรต",
                                  "type": "text",
                                  "color": "#8A1ABFFF"
                                },
                                {
                                  "size": "sm",
                                  "text": str(round(result[6], 2))+" g",
                                  "color": "#8A1ABFFF",
                                  "contents": [],
                                  "align": "end",
                                  "type": "text"
                                }
                              ]
                            },
                            {
                              "contents": [
                                {
                                  "type": "icon",
                                  "url": "https://cdn-icons-png.flaticon.com/128/305/305434.png"
                                },
                                {
                                  "type": "text",
                                  "text": "โซเดียม",
                                  "color": "#1ED2C1FF",
                                  "margin": "sm",
                                  "contents": []
                                },
                                {
                                  "align": "end",
                                  "color": "#1ED2C1FF",
                                  "margin": "xxl",
                                  "type": "text",
                                  "contents": [],
                                  "text": str(round(result[8], 2))+" mg",
                                  "weight": "bold",
                                  "size": "sm"
                                }
                              ],
                              "type": "box",
                              "layout": "baseline"
                            },
                            {
                              "contents": [
                                {
                                  "url": "https://cdn-icons-png.flaticon.com/128/194/194394.png",
                                  "type": "icon"
                                },
                                {
                                  "contents": [],
                                  "color": "#FE397BFF",
                                  "margin": "sm",
                                  "text": "น้ำตาล",
                                  "type": "text",
                                  "weight": "bold"
                                },
                                {
                                  "align": "end",
                                  "margin": "sm",
                                  "text": str(round(result[9], 2))+" g",
                                  "color": "#FE397BFF",
                                  "contents": [],
                                  "type": "text",
                                  "size": "sm",
                                  "weight": "bold"
                                }
                              ],
                              "type": "box",
                              "layout": "baseline"
                            }
                          ],
                          "layout": "vertical"
                        },
                        {
                          "text": "คุณค่าทางโภชนาการต่อ 100 กรัมของส่วนที่กินได้",
                          "size": "xxs",
                          "type": "text",
                          "color": "#AAAAAA",
                          "contents": []
                        },
                        {
                          "type": "text",
                          "text": "ข้อมูลจากสำนักโภชนาการ กรมอนามัย ฉบับปี 2561",
                          "contents": [],
                          "size": "xxs",
                          "color": "#AAAAAA"
                        }
                      ],
                      "type": "box"
                    },
                    "footer": {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [
                        {
                          "style": "primary",
                          "action": {
                            "label": "บันทึกแคลลอรี่",
                            "type": "message",
                            "text": "บันทึก"
                          },
                          "color": "#19B500FF",
                          "type": "button"
                        }
                      ]
                    },
                    "type": "bubble"
                  },
                  "type": "flex"
                }
              },
              "platform": "LINE"
            }
          ]
          }
          answer_bot = flex
      return answer_bot
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex
    
    
    

# def BMI(respond_dict): #ฟังก์ชั่นสำหรับคำนวนน้ำหนัก

#     #เก็บค่าของ Weight กับ Height
#     weight1 = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Weight.original"])
#     height1 = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Height.original"])
    
#     #คำนวนน้ำหนัก
#     BMI = weight1/(height1/100)**2
#     if BMI < 18.5 :
#         answer_function = "ผอมจังเลย"
#     elif 18.5 <= BMI < 23.0:
#         answer_function = "สมส่วนจ้าา"
#     elif 23.0 <= BMI < 25.0:
#         answer_function = "ค่อนข้างอ้วนเลยนะ"
#     elif 25.0 <= BMI < 30:
#         answer_function = "อ้วนล่ะจ้าาา"
#     else :
#         answer_function = "อ้วนมากจ้าา"
#     return answer_function

def BMRMale(respond_dict):
    try:
      user_id = respond_dict['originalDetectIntentRequest']['payload']['data']['source']['userId']
      sqlselect = "SELECT * FROM user_detail WHERE user_id = '{}'"
      cursor.execute(sqlselect.format(user_id))
      result = cursor.fetchone()

      #เก็บค่าของ Weight,Height และ Age
      weight = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Weight.original"])
      height = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Height.original"])
      age = int(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Age.original"])

      #คำนวน BMR ชาย
      BMR = 66+(13.7*weight)+(5*height)-(6.8*age)
      if (result is not None and result[0] == user_id):
          sqlupdate = "UPDATE user_detail SET user_weight = %s, user_height	= %s, user_age = %s, user_bmr = %s  WHERE user_id = '%s'" % (weight, height, age, BMR, user_id)
          valueupdate = (weight, height, age, BMR, user_id)
          cursor.execute(sqlupdate)
          mydb.commit()
      elif (result is None):
          malestr = 'ชาย'
          sqlinsert = "INSERT INTO user_detail (user_id, user_gender, user_weight, user_height, user_age, user_bmr) VALUES ('%s','%s', %s, %s, %s, %s)" % (user_id, malestr, weight, height, age, BMR)
          valueinsert = (user_id, malestr, weight, height, age, BMR)
          cursor.execute(sqlinsert)
          mydb.commit()
      else:
          print("No user_id on database.")
      BMRstr = {
        "fulfillmentMessages": [
          {
            "payload": {
              "line": {
                "altText": "Flex Message",
                "contents": {
                  "footer": {
                    "contents": [
                      {
                        "type": "spacer"
                      },
                      {
                        "spacing": "sm",
                        "type": "box",
                        "contents": [
                          {
                            "type": "box",
                            "contents": [
                              {
                                "color": "#000000FF",
                                "margin": "sm",
                                "type": "text",
                                "size": "xl",
                                "text": "BMR",
                                "weight": "bold",
                                "contents": []
                              },
                              {
                                "text": str(round(BMR, 1))+" kcal",
                                "type": "text",
                                "size": "xl",
                                "contents": [],
                                "align": "end",
                                "weight": "bold"
                              }
                            ],
                            "layout": "baseline"
                          }
                        ],
                        "layout": "vertical"
                      },
                      {
                        "size": "xs",
                        "margin": "sm",
                        "color": "#AAAAAA",
                        "contents": [],
                        "text": "คือ อัตราการความต้องการเผาผลาญของร่างกาย",
                        "type": "text",
                      },
                      {
                        "size": "xs",
                        "margin": "sm",
                        "color": "#AAAAAA",
                        "contents": [],
                        "text": "หรือจำนวนแคลอรี่ขั้นต่ำที่ต้องการใช้ในชีวิตแต่ละวัน",
                        "type": "text",
                      },
                      {
                        "action": {
                          "label": "แก้ไข",
                          "text": "แก้ไขคำนวณปริมาณแคลอรี่ต่อวัน",
                          "type": "message"
                        },
                        "color": "#19B500FF",
                        "margin": "sm",
                        "type": "button"
                      }
                    ],
                    "layout": "vertical",
                    "type": "box"
                  },
                  "body": {
                    "type": "box",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "url": "https://cdn-icons-png.flaticon.com/128/10109/10109492.png"
                              },
                              {
                                "margin": "sm",
                                "color": "#000000FF",
                                "type": "text",
                                "weight": "bold",
                                "text": "เพศ",
                                "contents": []
                              },
                              {
                                "text": "ชาย",
                                "contents": [],
                                "type": "text",
                                "align": "end",
                                "color": "#000000FF",
                                "size": "sm"
                              }
                            ]
                          },
                          {
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/3787/3787837.png",
                                "type": "icon"
                              },
                              {
                                "color": "#000000FF",
                                "weight": "bold",
                                "text": "อายุ",
                                "margin": "sm",
                                "contents": [],
                                "type": "text"
                              },
                              {
                                "align": "end",
                                "contents": [],
                                "color": "#000000FF",
                                "text": str(age),
                                "type": "text",
                                "size": "sm"
                              }
                            ],
                            "layout": "baseline",
                            "type": "box"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/866/866711.png",
                                "type": "icon"
                              },
                              {
                                "weight": "bold",
                                "text": "น้ำหนัก",
                                "color": "#000000FF",
                                "type": "text",
                                "contents": [],
                                "margin": "sm"
                              },
                              {
                                "type": "text",
                                "contents": [],
                                "color": "#000000FF",
                                "size": "sm",
                                "align": "end",
                                "text": str(weight)+" kg"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "url": "https://cdn-icons-png.flaticon.com/128/7410/7410369.png"
                              },
                              {
                                "contents": [],
                                "color": "#000000FF",
                                "margin": "sm",
                                "type": "text",
                                "text": "ส่วนสูง",
                                "weight": "bold"
                              },
                              {
                                "type": "text",
                                "text": str(height)+" cm",
                                "size": "sm",
                                "contents": [],
                                "color": "#000000FF",
                                "align": "end"
                              }
                            ]
                          }
                        ],
                        "spacing": "sm"
                      }
                    ],
                    "layout": "vertical",
                    "spacing": "md",
                    "action": {
                      "type": "uri",
                      "uri": "https://linecorp.com",
                      "label": "Action"
                    }
                  },
                  "type": "bubble"
                },
                "type": "flex"
              }
            },
            "platform": "LINE"
          },
        ]
        }
      return BMRstr
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex
    
def BMRFemale(respond_dict): #คำนวณ BMR ผู้หญิง
    try:
      user_id = respond_dict['originalDetectIntentRequest']['payload']['data']['source']['userId']
      cursor = mydb.cursor()
      sqlselect = "SELECT * FROM user_detail WHERE user_id = '{}'"
      cursor.execute(sqlselect.format(user_id))
      result = cursor.fetchone()

      #เก็บค่าของ Weight,Height และ Age
      weight = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Weight.original"])
      height = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Height.original"])
      age = int(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Age.original"])

      #คำนวน BMR หญิง
      BMR = 665+(9.6*weight)+(1.8*height)-(4.7*age)
      if (result is not None and result[0] == user_id):
          sqlupdate = "UPDATE user_detail SET user_weight = %s, user_height	= %s, user_age = %s, user_bmr = %s  WHERE user_id = '%s'" % (weight, height, age, BMR, user_id)
          print("SQL Statement:", sqlupdate)
          cursor.execute(sqlupdate)
          mydb.commit()
      elif (result is None):
          femalestr = 'หญิง'
          sqlinsert = "INSERT INTO user_detail (user_id, user_gender, user_weight, user_height, user_age, user_bmr) VALUES ('%s','%s', %s, %s, %s, %s)" % (user_id, femalestr, weight, height, age, BMR)
          print("SQL Statement:", sqlinsert)
          cursor.execute(sqlinsert)
          mydb.commit()
      else:
          print("No user_id on database.")
      BMRstr = {
        "fulfillmentMessages": [
          {
            "payload": {
              "line": {
                "altText": "Flex Message",
                "contents": {
                  "footer": {
                    "contents": [
                      {
                        "type": "spacer"
                      },
                      {
                        "spacing": "sm",
                        "type": "box",
                        "contents": [
                          {
                            "type": "box",
                            "contents": [
                              {
                                "color": "#000000FF",
                                "margin": "sm",
                                "type": "text",
                                "size": "xl",
                                "text": "BMR",
                                "weight": "bold",
                                "contents": []
                              },
                              {
                                "text": str(round(BMR, 1))+" kcal",
                                "type": "text",
                                "size": "xl",
                                "contents": [],
                                "align": "end",
                                "weight": "bold"
                              }
                            ],
                            "layout": "baseline"
                          }
                        ],
                        "layout": "vertical"
                      },
                      {
                        "size": "xs",
                        "margin": "sm",
                        "color": "#AAAAAA",
                        "contents": [],
                        "text": "คือ อัตราการความต้องการเผาผลาญของร่างกาย",
                        "type": "text",
                      },
                      {
                        "size": "xs",
                        "margin": "sm",
                        "color": "#AAAAAA",
                        "contents": [],
                        "text": "หรือจำนวนแคลอรี่ขั้นต่ำที่ต้องการใช้ในชีวิตแต่ละวัน",
                        "type": "text",
                      },
                      {
                        "action": {
                          "label": "แก้ไข",
                          "text": "แก้ไขคำนวณปริมาณแคลอรี่ต่อวัน",
                          "type": "message"
                        },
                        "color": "#19B500FF",
                        "margin": "sm",
                        "type": "button"
                      }
                    ],
                    "layout": "vertical",
                    "type": "box"
                  },
                  "body": {
                    "type": "box",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "url": "https://cdn-icons-png.flaticon.com/128/10109/10109492.png"
                              },
                              {
                                "margin": "sm",
                                "color": "#000000FF",
                                "type": "text",
                                "weight": "bold",
                                "text": "เพศ",
                                "contents": []
                              },
                              {
                                "text": "หญิง",
                                "contents": [],
                                "type": "text",
                                "align": "end",
                                "color": "#000000FF",
                                "size": "sm"
                              }
                            ]
                          },
                          {
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/3787/3787837.png",
                                "type": "icon"
                              },
                              {
                                "color": "#000000FF",
                                "weight": "bold",
                                "text": "อายุ",
                                "margin": "sm",
                                "contents": [],
                                "type": "text"
                              },
                              {
                                "align": "end",
                                "contents": [],
                                "color": "#000000FF",
                                "text": str(age),
                                "type": "text",
                                "size": "sm"
                              }
                            ],
                            "layout": "baseline",
                            "type": "box"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/866/866711.png",
                                "type": "icon"
                              },
                              {
                                "weight": "bold",
                                "text": "น้ำหนัก",
                                "color": "#000000FF",
                                "type": "text",
                                "contents": [],
                                "margin": "sm"
                              },
                              {
                                "type": "text",
                                "contents": [],
                                "color": "#000000FF",
                                "size": "sm",
                                "align": "end",
                                "text": str(weight)+" kg"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "url": "https://cdn-icons-png.flaticon.com/128/7410/7410369.png"
                              },
                              {
                                "contents": [],
                                "color": "#000000FF",
                                "margin": "sm",
                                "type": "text",
                                "text": "ส่วนสูง",
                                "weight": "bold"
                              },
                              {
                                "type": "text",
                                "text": str(height)+" cm",
                                "size": "sm",
                                "contents": [],
                                "color": "#000000FF",
                                "align": "end"
                              }
                            ]
                          }
                        ],
                        "spacing": "sm"
                      }
                    ],
                    "layout": "vertical",
                    "spacing": "md",
                    "action": {
                      "type": "uri",
                      "uri": "https://linecorp.com",
                      "label": "Action"
                    }
                  },
                  "type": "bubble"
                },
                "type": "flex"
              }
            },
            "platform": "LINE"
          },
          {
            "text": {
              "text": [
                ""
              ]
            }
          }
        ]
        }
      return BMRstr
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex

def cal_result(respond_dict): #สรุปแคลอรี่ในอาหาร
    try:
      user_id = respond_dict['originalDetectIntentRequest']['payload']['data']['source']['userId']
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
              "fulfillmentMessages": [
            {
              "text": {
                "text": [
                  "เหมือนวันนี้คุณจะยังไม่ได้บันทึกอะไรนะ ลองพิมชื่ออาหารแล้วกดบันทึกดูสิ:)"
                ]
              },
              "platform": "LINE"
            },
            {
              "payload": {
                "line": {
                  "altText": "this is a buttons template",
                  "type": "template",
                  "template": {
                    "title": "ดูสรุปย้อนหลังกันเถอะ",
                    "imageBackgroundColor": "#FFFFFF",
                    "text": "กดที่ปุ่ม ดูสรุปย้อนหลัง",
                    "actions": [
                      {
                        "text": "ดูสรุปย้อนหลัง",
                        "type": "message",
                        "label": "ดูสรุปย้อนหลัง"
                      }
                    ],
                    "type": "buttons"
                  }
                }
              },
              "platform": "LINE"
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
                "fulfillmentMessages": [
              {
                "payload": {
                  "line": {
                    "contents": {
                      "body": {
                        "action": {
                          "uri": "https://linecorp.com",
                          "label": "Action",
                          "type": "uri"
                        },
                        "layout": "vertical",
                        "type": "box",
                        "contents": [
                          {
                            "contents": [],
                            "type": "text",
                            "text": "สรุปอาหารที่ทานทั้งหมด",
                            "align": "center",
                            "weight": "bold"
                          },
                          *menu_contents
                        ]
                      },
                      "type": "bubble",
                      "header": {
                        "layout": "vertical",
                        "type": "box",
                        "contents": [
                          {
                            "size": "md",
                            "align": "center",
                            "contents": [],
                            "type": "text",
                            "weight": "bold",
                            "text": "สรุปประจำวัน"
                          },
                          {
                            "size": "xl",
                            "text": formatted_date_str,
                            "type": "text",
                            "align": "center",
                            "contents": []
                          }
                        ]
                      },
                      "footer": {
                        "type": "box",
                        "contents": [
                          {
                            "align": "center",
                            "weight": "bold",
                            "contents": [],
                            "text": "สรุปโภชนาการรวม",
                            "type": "text"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/5550/5550932.png",
                                "type": "icon"
                              },
                              {
                                "color": "#27B300FF",
                                "type": "text",
                                "text": "พลังงานรวม",
                                "contents": [],
                                "weight": "bold",
                                "margin": "sm"
                              },
                              {
                                "text": str(round(all_kcal, 2))+" kcal",
                                "type": "text",
                                "color": "#27B300FF",
                                "contents": [],
                                "size": "sm",
                                "align": "end"
                              }
                            ]
                          },
                          {
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/12918/12918996.png",
                                "type": "icon"
                              },
                              {
                                "contents": [],
                                "text": "โปรตีนรวม",
                                "weight": "bold",
                                "color": "#14A7D7FF",
                                "margin": "sm",
                                "type": "text"
                              },
                              {
                                "color": "#14A7D7FF",
                                "contents": [],
                                "type": "text",
                                "size": "sm",
                                "align": "end",
                                "text": str(round(all_protein, 2))+" g"
                              }
                            ],
                            "layout": "baseline",
                            "type": "box"
                          },
                          {
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "url": "https://cdn-icons-png.flaticon.com/128/7194/7194052.png"
                              },
                              {
                                "weight": "bold",
                                "color": "#F3D100FF",
                                "contents": [],
                                "type": "text",
                                "text": "ไขมันรวม",
                                "margin": "sm"
                              },
                              {
                                "type": "text",
                                "size": "sm",
                                "align": "end",
                                "contents": [],
                                "text": str(round(all_fat, 2))+" g",
                                "color": "#E3C300FF"
                              }
                            ],
                            "type": "box"
                          },
                          {
                            "type": "box",
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/8493/8493969.png",
                                "type": "icon"
                              },
                              {
                                "contents": [],
                                "text": "คาร์โบไฮเดรตรวม",
                                "color": "#8A1ABFFF",
                                "type": "text",
                                "margin": "sm"
                              },
                              {
                                "contents": [],
                                "text": str(round(all_carbs, 2))+" g",
                                "align": "end",
                                "size": "sm",
                                "type": "text",
                                "color": "#8A1ABFFF"
                              }
                            ],
                            "layout": "baseline"
                          },
                          {
                            "layout": "baseline",
                            "type": "box",
                            "contents": [
                              {
                                "url": "https://cdn-icons-png.flaticon.com/128/305/305434.png",
                                "type": "icon"
                              },
                              {
                                "type": "text",
                                "contents": [],
                                "color": "#1ED2C1FF",
                                "margin": "sm",
                                "text": "โซเดียมรวม"
                              },
                              {
                                "margin": "xxl",
                                "weight": "bold",
                                "align": "end",
                                "text": str(round(all_sodium, 2))+" g",
                                "color": "#1ED2C1FF",
                                "type": "text",
                                "contents": [],
                                "size": "sm"
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
                                "contents": [],
                                "weight": "bold",
                                "margin": "sm",
                                "type": "text",
                                "color": "#FE397BFF",
                                "text": "น้ำตาลรวม"
                              },
                              {
                                "weight": "bold",
                                "align": "end",
                                "type": "text",
                                "contents": [],
                                "text": str(round(all_sugar, 2))+" g",
                                "margin": "sm",
                                "color": "#FE397BFF",
                                "size": "sm"
                              }
                            ]
                          },
                          {
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "url": "https://cdn-icons-png.flaticon.com/128/7927/7927615.png"
                              },
                              {
                                "color": "#000000FF",
                                "size": "lg",
                                "text": "BMR",
                                "margin": "sm",
                                "contents": [],
                                "type": "text",
                                "align": "start",
                                "weight": "bold"
                              },
                              {
                                "text": str(user_bmr)+" kcal",
                                "contents": [],
                                "margin": "sm",
                                "size": "lg",
                                "weight": "bold",
                                "type": "text",
                                "color": "#000000FF",
                                "align": "end"
                              }
                            ],
                            "margin": "lg",
                            "spacing": "sm",
                            "type": "box"
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
                        ],
                        "layout": "vertical"
                      }
                    },
                    "altText": "Flex Message",
                    "type": "flex"
                  }
                },
                "platform": "LINE"
              }
            ]
            }
          answer_flex = result_flex  
      return answer_flex
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex

def past_cal_result(respond_dict):
    try:
        user_id = respond_dict['originalDetectIntentRequest']['payload']['data']['source']['userId']
        date_time = (respond_dict["queryResult"]["outputContexts"][0]["parameters"]["date"])
        date_time_obj = datetime.fromisoformat(date_time[:-6]) 
        print(date_time_obj)
        formatted_date = date_time_obj.strftime('%Y%m%d')
        formatted_date_str = date_time_obj.strftime('%d/%m/%Y')
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
                "fulfillmentMessages": [
              {
                "text": {
                  "text": [
                    "เหมือนวันที่คุณระบุจะไม่มีข้อมูลนะ:)"
                  ]
                },
                "platform": "LINE"
              },
              {
                "payload": {
                  "line": {
                    "altText": "this is a buttons template",
                    "type": "template",
                    "template": {
                      "title": "ดูสรุปย้อนหลังกันเถอะ",
                      "imageBackgroundColor": "#FFFFFF",
                      "text": "กดที่ปุ่ม ดูสรุปย้อนหลัง",
                      "actions": [
                        {
                          "text": "ดูสรุปย้อนหลัง",
                          "type": "message",
                          "label": "ดูสรุปย้อนหลัง"
                        }
                      ],
                      "type": "buttons"
                    }
                  }
                },
                "platform": "LINE"
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
                  "fulfillmentMessages": [
                {
                  "payload": {
                    "line": {
                      "contents": {
                        "body": {
                          "action": {
                            "uri": "https://linecorp.com",
                            "label": "Action",
                            "type": "uri"
                          },
                          "layout": "vertical",
                          "type": "box",
                          "contents": [
                            {
                              "contents": [],
                              "type": "text",
                              "text": "สรุปอาหารที่ทานทั้งหมด",
                              "align": "center",
                              "weight": "bold"
                            },
                            *menu_contents
                          ]
                        },
                        "type": "bubble",
                        "header": {
                          "layout": "vertical",
                          "type": "box",
                          "contents": [
                            {
                              "size": "md",
                              "align": "center",
                              "contents": [],
                              "type": "text",
                              "weight": "bold",
                              "text": "สรุปประจำวัน"
                            },
                            {
                              "size": "xl",
                              "text": formatted_date_str,
                              "type": "text",
                              "align": "center",
                              "contents": []
                            }
                          ]
                        },
                        "footer": {
                          "type": "box",
                          "contents": [
                            {
                              "align": "center",
                              "weight": "bold",
                              "contents": [],
                              "text": "สรุปโภชนาการรวม",
                              "type": "text"
                            },
                            {
                              "type": "box",
                              "layout": "baseline",
                              "contents": [
                                {
                                  "url": "https://cdn-icons-png.flaticon.com/128/5550/5550932.png",
                                  "type": "icon"
                                },
                                {
                                  "color": "#27B300FF",
                                  "type": "text",
                                  "text": "พลังงานรวม",
                                  "contents": [],
                                  "weight": "bold",
                                  "margin": "sm"
                                },
                                {
                                  "text": str(round(all_kcal, 2))+" kcal",
                                  "type": "text",
                                  "color": "#27B300FF",
                                  "contents": [],
                                  "size": "sm",
                                  "align": "end"
                                }
                              ]
                            },
                            {
                              "contents": [
                                {
                                  "url": "https://cdn-icons-png.flaticon.com/128/12918/12918996.png",
                                  "type": "icon"
                                },
                                {
                                  "contents": [],
                                  "text": "โปรตีนรวม",
                                  "weight": "bold",
                                  "color": "#14A7D7FF",
                                  "margin": "sm",
                                  "type": "text"
                                },
                                {
                                  "color": "#14A7D7FF",
                                  "contents": [],
                                  "type": "text",
                                  "size": "sm",
                                  "align": "end",
                                  "text": str(round(all_protein, 2))+" g"
                                }
                              ],
                              "layout": "baseline",
                              "type": "box"
                            },
                            {
                              "layout": "baseline",
                              "contents": [
                                {
                                  "type": "icon",
                                  "url": "https://cdn-icons-png.flaticon.com/128/7194/7194052.png"
                                },
                                {
                                  "weight": "bold",
                                  "color": "#F3D100FF",
                                  "contents": [],
                                  "type": "text",
                                  "text": "ไขมันรวม",
                                  "margin": "sm"
                                },
                                {
                                  "type": "text",
                                  "size": "sm",
                                  "align": "end",
                                  "contents": [],
                                  "text": str(round(all_fat, 2))+" g",
                                  "color": "#E3C300FF"
                                }
                              ],
                              "type": "box"
                            },
                            {
                              "type": "box",
                              "contents": [
                                {
                                  "url": "https://cdn-icons-png.flaticon.com/128/8493/8493969.png",
                                  "type": "icon"
                                },
                                {
                                  "contents": [],
                                  "text": "คาร์โบไฮเดรตรวม",
                                  "color": "#8A1ABFFF",
                                  "type": "text",
                                  "margin": "sm"
                                },
                                {
                                  "contents": [],
                                  "text": str(round(all_carbs, 2))+" g",
                                  "align": "end",
                                  "size": "sm",
                                  "type": "text",
                                  "color": "#8A1ABFFF"
                                }
                              ],
                              "layout": "baseline"
                            },
                            {
                              "layout": "baseline",
                              "type": "box",
                              "contents": [
                                {
                                  "url": "https://cdn-icons-png.flaticon.com/128/305/305434.png",
                                  "type": "icon"
                                },
                                {
                                  "type": "text",
                                  "contents": [],
                                  "color": "#1ED2C1FF",
                                  "margin": "sm",
                                  "text": "โซเดียมรวม"
                                },
                                {
                                  "margin": "xxl",
                                  "weight": "bold",
                                  "align": "end",
                                  "text": str(round(all_sodium, 2))+" g",
                                  "color": "#1ED2C1FF",
                                  "type": "text",
                                  "contents": [],
                                  "size": "sm"
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
                                  "contents": [],
                                  "weight": "bold",
                                  "margin": "sm",
                                  "type": "text",
                                  "color": "#FE397BFF",
                                  "text": "น้ำตาลรวม"
                                },
                                {
                                  "weight": "bold",
                                  "align": "end",
                                  "type": "text",
                                  "contents": [],
                                  "text": str(round(all_sugar, 2))+" g",
                                  "margin": "sm",
                                  "color": "#FE397BFF",
                                  "size": "sm"
                                }
                              ]
                            },
                            {
                              "layout": "baseline",
                              "contents": [
                                {
                                  "type": "icon",
                                  "url": "https://cdn-icons-png.flaticon.com/128/7927/7927615.png"
                                },
                                {
                                  "color": "#000000FF",
                                  "size": "lg",
                                  "text": "BMR",
                                  "margin": "sm",
                                  "contents": [],
                                  "type": "text",
                                  "align": "start",
                                  "weight": "bold"
                                },
                                {
                                  "text": str(user_bmr)+" kcal",
                                  "contents": [],
                                  "margin": "sm",
                                  "size": "lg",
                                  "weight": "bold",
                                  "type": "text",
                                  "color": "#000000FF",
                                  "align": "end"
                                }
                              ],
                              "margin": "lg",
                              "spacing": "sm",
                              "type": "box"
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
                          ],
                          "layout": "vertical"
                        }
                      },
                      "altText": "Flex Message",
                      "type": "flex"
                    }
                  },
                  "platform": "LINE"
                }
              ]
              }
            answer_flex = result_flex  
        return answer_flex
    except Exception as e:
        error_flex = {
            "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
            }
        return error_flex

def save_cal(respond_dict): #บันทึกแคลอรี่ในอาหาร
    try:
      user_id = respond_dict['originalDetectIntentRequest']['payload']['data']['source']['userId']
      sql = "SELECT * FROM food WHERE food_id = {}"
      cursor.execute(sql.format(food_id))
      result = cursor.fetchone()
      date_time = datetime.now()
      formatted_date = date_time.strftime('%Y%m%d%H%M%S')
      sqlinsert = "INSERT INTO save_detail (user_id, food_id, save_date) VALUES ('%s', %s, %s)" % (user_id, str(result[0]), formatted_date)
      cursor.execute(sqlinsert)
      mydb.commit()
      formatted_date_for_result = date_time.strftime('%Y%m%d')
      sql_cal = "SELECT * FROM save_detail WHERE user_id = '%s' and DATE(save_date) = '%s'" % (user_id, formatted_date_for_result)
      cursor.execute(sql_cal)
      result_cal = cursor.fetchall()
      all_kcal, all_protein, all_fat, all_carbs, all_sodium, all_sugar = 0, 0, 0, 0, 0, 0
      menu_contents = []
      for i in result_cal:        
        data = i
        sql_food = "SELECT * FROM food WHERE food_id = {}"
        cursor.execute(sql_food.format(data[1]))
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
            "fulfillmentMessages": [
          {
            "payload": {
              "line": {
                "type": "flex",
                "altText": "Flex Message",
                "contents": {
                  "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "text": "สรุปอาหารที่ทานทั้งหมด",
                        "align": "center",
                        "type": "text",
                        "weight": "bold",
                        "contents": []
                      },
                      *menu_contents
                    ],
                    "action": {
                      "uri": "https://linecorp.com",
                      "label": "Action",
                      "type": "uri"
                    }
                  },
                  "footer": {
                    "layout": "vertical",
                    "type": "box",
                    "contents": [
                      {
                        "align": "center",
                        "contents": [],
                        "type": "text",
                        "text": "สรุปโภชนาการรวม",
                        "weight": "bold"
                      },
                      {
                        "layout": "baseline",
                        "contents": [
                          {
                            "type": "icon",
                            "url": "https://cdn-icons-png.flaticon.com/128/5550/5550932.png"
                          },
                          {
                            "margin": "sm",
                            "contents": [],
                            "color": "#27B300FF",
                            "type": "text",
                            "weight": "bold",
                            "text": "พลังงานรวม"
                          },
                          {
                            "contents": [],
                            "size": "sm",
                            "align": "end",
                            "color": "#27B300FF",
                            "type": "text",
                            "text": str(round(all_kcal, 2))+" kcal"
                          }
                        ],
                        "type": "box"
                      },
                      {
                        "contents": [
                          {
                            "type": "icon",
                            "url": "https://cdn-icons-png.flaticon.com/128/12918/12918996.png"
                          },
                          {
                            "contents": [],
                            "weight": "bold",
                            "color": "#14A7D7FF",
                            "margin": "sm",
                            "type": "text",
                            "text": "โปรตีนรวม"
                          },
                          {
                            "contents": [],
                            "color": "#14A7D7FF",
                            "align": "end",
                            "type": "text",
                            "text": str(round(all_protein, 2))+" g",
                            "size": "sm"
                          }
                        ],
                        "type": "box",
                        "layout": "baseline"
                      },
                      {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                          {
                            "url": "https://cdn-icons-png.flaticon.com/128/7194/7194052.png",
                            "type": "icon"
                          },
                          {
                            "text": "ไขมันรวม",
                            "weight": "bold",
                            "margin": "sm",
                            "color": "#F3D100FF",
                            "contents": [],
                            "type": "text"
                          },
                          {
                            "contents": [],
                            "type": "text",
                            "align": "end",
                            "color": "#E3C300FF",
                            "size": "sm",
                            "text": str(round(all_fat, 2))+" g"
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
                            "text": "คาร์โบไฮเดรตรวม",
                            "type": "text",
                            "contents": [],
                            "margin": "sm",
                            "color": "#8A1ABFFF"
                          },
                          {
                            "align": "end",
                            "size": "sm",
                            "text": str(round(all_carbs, 2))+" g",
                            "type": "text",
                            "color": "#8A1ABFFF",
                            "contents": []
                          }
                        ]
                      },
                      {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                          {
                            "url": "https://cdn-icons-png.flaticon.com/128/305/305434.png",
                            "type": "icon"
                          },
                          {
                            "contents": [],
                            "text": "โซเดียมรวม",
                            "margin": "sm",
                            "color": "#1ED2C1FF",
                            "type": "text"
                          },
                          {
                            "text": str(round(all_sodium, 2))+" mg",
                            "type": "text",
                            "align": "end",
                            "contents": [],
                            "weight": "bold",
                            "size": "sm",
                            "color": "#1ED2C1FF",
                            "margin": "xxl"
                          }
                        ]
                      },
                      {
                        "layout": "baseline",
                        "type": "box",
                        "contents": [
                          {
                            "type": "icon",
                            "url": "https://cdn-icons-png.flaticon.com/128/194/194394.png"
                          },
                          {
                            "weight": "bold",
                            "margin": "sm",
                            "color": "#FE397BFF",
                            "type": "text",
                            "text": "น้ำตาลรวม",
                            "contents": []
                          },
                          {
                            "text": str(round(all_sugar, 2))+" g",
                            "type": "text",
                            "align": "end",
                            "size": "sm",
                            "color": "#FE397BFF",
                            "weight": "bold",
                            "margin": "sm",
                            "contents": []
                          }
                        ]
                      },
                      {
                        "type": "spacer",
                        "size": "xs"
                      }
                    ]
                  },
                  "type": "bubble"
                }
              }
            },
            "platform": "LINE"
          }
        ]
        }     
      return result_flex
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex

def addMenu(menu_name):
    try:
      sql = "SELECT * FROM food WHERE food_thai = '{}'"
      cursor.execute(sql.format(menu_name))
      result = cursor.fetchone()
      global food_id
      food_id = str(result[0])
      result_flex = {
          "fulfillmentMessages": [
        {
          "payload": {
            "line": {
              "altText": "Flex Message",
              "contents": {
                "body": {
                  "spacing": "md",
                  "action": {
                    "type": "uri",
                    "label": "Action",
                    "uri": "https://linecorp.com"
                  },
                  "layout": "vertical",
                  "contents": [
                    {
                      "text": str(result[1]),
                      "type": "text",
                      "weight": "bold",
                      "contents": [],
                      "size": "xl"
                    },
                    {
                      "type": "box",
                      "spacing": "sm",
                      "contents": [
                        {
                          "layout": "baseline",
                          "type": "box",
                          "contents": [
                            {
                              "url": "https://cdn-icons-png.flaticon.com/128/5550/5550932.png",
                              "type": "icon"
                            },
                            {
                              "weight": "bold",
                              "text": "พลังงาน",
                              "contents": [],
                              "color": "#27B300FF",
                              "margin": "sm",
                              "type": "text"
                            },
                            {
                              "text": str(result[3])+" kcal",
                              "type": "text",
                              "contents": [],
                              "size": "sm",
                              "align": "end",
                              "color": "#27B300FF"
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
                              "text": "โปรตีน",
                              "color": "#14A7D7FF",
                              "contents": [],
                              "weight": "bold",
                              "margin": "sm",
                              "type": "text"
                            },
                            {
                              "align": "end",
                              "contents": [],
                              "text": str(round(result[4], 2))+" g",
                              "size": "sm",
                              "type": "text",
                              "color": "#14A7D7FF"
                            }
                          ]
                        },
                        {
                          "type": "box",
                          "contents": [
                            {
                              "type": "icon",
                              "url": "https://cdn-icons-png.flaticon.com/128/7194/7194052.png"
                            },
                            {
                              "text": "ไขมัน",
                              "contents": [],
                              "margin": "sm",
                              "type": "text",
                              "color": "#F3D100FF",
                              "weight": "bold"
                            },
                            {
                              "contents": [],
                              "size": "sm",
                              "color": "#E3C300FF",
                              "type": "text",
                              "text": str(round(result[5], 2))+" g",
                              "align": "end"
                            }
                          ],
                          "layout": "baseline"
                        },
                        {
                          "layout": "baseline",
                          "type": "box",
                          "contents": [
                            {
                              "url": "https://cdn-icons-png.flaticon.com/128/8493/8493969.png",
                              "type": "icon"
                            },
                            {
                              "contents": [],
                              "margin": "sm",
                              "text": "คาร์โบไฮเดรต",
                              "type": "text",
                              "color": "#8A1ABFFF"
                            },
                            {
                              "size": "sm",
                              "text": str(round(result[6], 2))+" g",
                              "color": "#8A1ABFFF",
                              "contents": [],
                              "align": "end",
                              "type": "text"
                            }
                          ]
                        },
                        {
                          "contents": [
                            {
                              "type": "icon",
                              "url": "https://cdn-icons-png.flaticon.com/128/305/305434.png"
                            },
                            {
                              "type": "text",
                              "text": "โซเดียม",
                              "color": "#1ED2C1FF",
                              "margin": "sm",
                              "contents": []
                            },
                            {
                              "align": "end",
                              "color": "#1ED2C1FF",
                              "margin": "xxl",
                              "type": "text",
                              "contents": [],
                              "text": str(round(result[8], 2))+" mg",
                              "weight": "bold",
                              "size": "sm"
                            }
                          ],
                          "type": "box",
                          "layout": "baseline"
                        },
                        {
                          "contents": [
                            {
                              "url": "https://cdn-icons-png.flaticon.com/128/194/194394.png",
                              "type": "icon"
                            },
                            {
                              "contents": [],
                              "color": "#FE397BFF",
                              "margin": "sm",
                              "text": "น้ำตาล",
                              "type": "text",
                              "weight": "bold"
                            },
                            {
                              "align": "end",
                              "margin": "sm",
                              "text": str(round(result[9], 2))+" g",
                              "color": "#FE397BFF",
                              "contents": [],
                              "type": "text",
                              "size": "sm",
                              "weight": "bold"
                            }
                          ],
                          "type": "box",
                          "layout": "baseline"
                        }
                      ],
                      "layout": "vertical"
                    },
                    {
                      "text": "คุณค่าทางโภชนาการต่อ 100 กรัมของส่วนที่กินได้",
                      "size": "xxs",
                      "type": "text",
                      "color": "#AAAAAA",
                      "contents": []
                    },
                    {
                      "type": "text",
                      "text": "ข้อมูลจากสำนักโภชนาการ กรมอนามัย ฉบับปี 2561",
                      "contents": [],
                      "size": "xxs",
                      "color": "#AAAAAA"
                    }
                  ],
                  "type": "box"
                },
                "footer": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "style": "primary",
                      "action": {
                        "label": "บันทึกแคลลอรี่",
                        "type": "message",
                        "text": "บันทึก"
                      },
                      "color": "#19B500FF",
                      "type": "button"
                    }
                  ]
                },
                "type": "bubble"
              },
              "type": "flex"
            }
          },
          "platform": "LINE"
        }
      ]
      }
      return jsonify(result_flex)
    except Exception as e:
      error_flex = {
          "fulfillmentMessages":[{"text": {"text": ["ไม่เข้าใจ คุณต้องการอะไร"]}}]
          }
      return error_flex
    

@app.route('/add_menu', methods=['POST'])
def add_menu():
    menu_name = request.form.get('menu_name')
    quantity = request.form.get('quantity')
    energy = request.form.get('energy')
    protein = request.form.get('protein')
    fat = request.form.get('fat')
    carbs = request.form.get('carbs')
    fiber = request.form.get('fiber')
    sodium = request.form.get('sodium')
    sugar = request.form.get('sugar')

    sql = "SELECT * FROM food ORDER BY food_id DESC;"
    cursor.execute(sql)
    result_id = cursor.fetchone()
    food_id = result_id[0] + 1
    sqlinsert = """ INSERT INTO food (food_id, food_thai, food_english, food_energy, food_protein, food_fat, food_carbs, food_fiber, food_sodium, food_sugar, image, food_type)
    VALUES
    (%s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, '%s', '%s')
    """ % (food_id, menu_name, "-", energy, protein, fat, carbs, "0", sodium, sugar, "-", "User")
    cursor.execute(sqlinsert)
    mydb.commit()

    addMenu(menu_name)

    return "ส่งฟอร์มเรียบร้อย! รบกวนกลับไปพิมพ์ชื่ออาหารที่เพิ่มอีกครั้งนะะ"
    
#Flask
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)


