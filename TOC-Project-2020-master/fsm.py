from transitions.extensions import GraphMachine

import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction

from utils import send_text_message, send_carousel_message, send_button_message, send_image_message

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text == "Hi"

    def on_enter_menu(self, event):
        title = '請選擇您要查詢的項目'
        text = '請問需要「中文(TW)」還是「English(GB)」服務?還是查看「fsm結構圖」'
        btn = [
            MessageTemplateAction(
                label = '中文(TW)',
                text ='中文(TW)'
            ),
            MessageTemplateAction(
                label = 'English(GB)',
                text = 'English(GB)'
            ),
        ]
        url='https://i.imgur.com/Bx1WwI1.png'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_chinese(self, event):
        text = event.message.text
        if (text == '中文(TW)'):
            return True
        return False
    def on_enter_chinese(self, event):
        title = '中文(TW)'
        text = '請選擇您要查詢的項目:'
        btn = [
            MessageTemplateAction(
                label = '社團介紹',
                text ='社團介紹'
            ),
            MessageTemplateAction(
                label = '如何參加',
                text = '如何參加'
            ),
            MessageTemplateAction(
                label = '時間地點',
                text = '時間地點'
            ),
        ]
        url='https://i.imgur.com/x7D85Rf.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_C_indroduction(self, event):
        text = event.message.text
        if (text == '社團介紹'):
            return True
        return False
    def on_enter_C_indroduction(self, event):
        title = '社團介紹'
        text = '歡迎加入成大國際演講社!\n遍佈全球的國際英語演講社，帶你認識全世界。'
        btn = [
            MessageTemplateAction(
                label = '入社須知',
                text = '入社須知'
            ),
            MessageTemplateAction(
                label = '近期活動',
                text = '近期活動'
            ),
        ]
        url='https://i.imgur.com/x7D85Rf.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_C_join(self, event):
        text = event.message.text
        if (text == '如何參加'):
            return True
        return False
    def on_enter_C_join(self, event):
        title = '如何參加'
        text = '歡迎參加我們每周日晚上的一般社課或星期六早上、星期四晚上的讀書會，隨時都歡迎加入呦!'
        btn = [
            MessageTemplateAction(
                label = '入社須知',
                text = '入社須知'
            ),
            MessageTemplateAction(
                label = '近期活動',
                text = '近期活動'
            ),
        ]
        url = 'https://i.imgur.com/62AUesc.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_C_time(self, event):
        text = event.message.text
        if (text == '時間地點'):
            return True
        return False
    def on_enter_C_time(self, event):
        title = '時間地點'
        text = '平時社課:\n每周日:18:30~21:30\n#第一學生活動中心會議室'
        btn = [
            MessageTemplateAction(
                label = '入社須知',
                text = '入社須知'
            ),
            MessageTemplateAction(
                label = '近期活動',
                text = '近期活動'
            ),
        ]
        url = 'https://i.imgur.com/L7E1svr.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        

    def is_going_to_C2_requirement(self, event):
        text = event.message.text
        return text == "入社須知"

    def on_enter_C2_requirement(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token,'出席:自由\n身分:不限(學生、已工作、外校皆可)\n演講:自願制\n社費:400\n輸入「Hi」回到主選單')
        self.go_back()
    def is_going_to_C2_recentactivity(self, event):
        text = event.message.text
        return text == "近期活動"

    def on_enter_C2_recentactivity(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token,'#目前寒假活動期間，本社團無活動，如此欲參加，可參考台南地區其他國際英語演講協會。\n輸入「Hi」回到主選單')
        self.go_back()
        
    def is_going_to_show_fsm_photo(self,event):
        text=event.message.text
        return text.lower()=='fsm'
        
    def on_enter_show_fsm_photo(self,event):
        reply_token = event.reply_token
        url='https://raw.githubusercontent.com/CrazyRyan0812/CrazyRyan-TOC/master/fsm.png'
        send_image_message(reply_token, url)
        self.go_back()

    def is_going_to_english(self, event):
        text = event.message.text
        if (text == 'English(GB)'):
            return True
        return False
    def on_enter_english(self, event):
        title = 'English(GB)'
        text = 'Please select query items:'
        btn = [
            MessageTemplateAction(
                label = 'Club Introduction',
                text ='Club Introduction'
            ),
            MessageTemplateAction(
                label = 'How to Participate',
                text = 'How to Participate'
            ),
            MessageTemplateAction(
                label = 'Time & Location',
                text = 'Time & Location'
            ),
        ]
        url = 'https://i.imgur.com/x7D85Rf.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_E_indroduction(self, event):
        text = event.message.text
        if (text == 'Club Introduction'):
            return True
        return False
    def on_enter_E_indroduction(self, event):
        title = 'Club Introduction'
        text = 'Hello Friend!\nLeading you know the world.'
        btn = [
            MessageTemplateAction(
                label = 'Member notice',
                text = 'Member notice'
            ),
            MessageTemplateAction(
                label = 'Recent Activities',
                text = 'Recent Activities'
            ),
        ]
        url='https://i.imgur.com/x7D85Rf.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
    
    def is_going_to_E_join(self, event):
        text = event.message.text
        if (text == 'How to Participate'):
            return True
        return False
    def on_enter_E_join(self, event):
        title = 'How to Participate'
        text = 'Join in our regular meeting in every Sunday night!'
        btn = [
            MessageTemplateAction(
                label = 'Member notice',
                text = 'Member notice'
        ),
            MessageTemplateAction(
                label = 'Recent Activities',
                text = 'Recent Activities'
        ),
        ]
        url='https://i.imgur.com/62AUesc.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_E_time(self, event):
        text = event.message.text
        if (text == 'Time & Location'):
            return True
        return False
    def on_enter_E_time(self, event):
        title = 'Time & Location'
        text = 'Time:(Sun)18:30~21:30\n#First Student Activity Room'
        btn = [
            MessageTemplateAction(
                label = 'Member notice',
                text = 'Member notice'
            ),
            MessageTemplateAction(
                label = 'Recent Activities',
                text = 'Recent Activities'
            ),
        ]
        url = 'https://i.imgur.com/L7E1svr.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
    def is_going_to_E2_requirement(self, event):
        text = event.message.text
        return text == "Member notice"

    def on_enter_E2_requirement(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token,'Attendance: no requirement for attending every meeting or activity \nMember: (everyone who are interested in English speaking) no limitation (NCKU students, non-NCKU students or non-students)\nDelivering Speech: voluntary \nFee:NTD400 \nEnter ”Hi” to return to menu.')
        self.go_back()
    def is_going_to_E2_recentactivity(self, event):
        text = event.message.text
        return text == "Recent Activities"

    def on_enter_E2_recentactivity(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token,'#During the winter vacation, NCKU Toastmasters has no activities. If you want to experience regular meetings or groupiii, you can contact with other Toastmasters in Tainan.\n Enter ”Hi” to return to menu.')
        self.go_back()
    