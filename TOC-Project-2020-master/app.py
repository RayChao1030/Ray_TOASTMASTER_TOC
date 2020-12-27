import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "menu","chinese", "english", "C_indroduction", "C_join","C_time", "C2_requirement","C2_recentactivity","show_fsm_photo","E_indroduction", "E_join","E_time", "E2_requirement","E2_recentactivity"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        { #2-1
            "trigger": "advance",
            "source": "menu",
            "dest": "chinese",
            "conditions": "is_going_to_chinese",
        },
        { #2-2
            "trigger": "advance",
            "source": "menu",
            "dest": "english",
            "conditions": "is_going_to_english",
        },
        { #3-1-1
            "trigger": "advance",
            "source": "chinese",
            "dest": "C_indroduction",
            "conditions": "is_going_to_C_indroduction",
        },
        { #3-1-2
            "trigger": "advance",
            "source": "chinese",
            "dest": "C_join",
            "conditions": "is_going_to_C_join",
        },
        { #3-1-3
            "trigger": "advance",
            "source": "chinese",
            "dest": "C_time",
            "conditions": "is_going_to_C_time",
        },
        { #4-1-1-1
            "trigger": "advance",
            "source": "C_indroduction",
            "dest": "C2_requirement",
            "conditions": "is_going_to_C2_requirement",
        },
        { #4-1-1-2
            "trigger": "advance",
            "source": "C_indroduction",
            "dest": "C2_recentactivity",
            "conditions": "is_going_to_C2_recentactivity",
        },
        { #4-1-2-1
            "trigger": "advance",
            "source": "C_join",
            "dest": "C2_requirement",
            "conditions": "is_going_to_C2_requirement",
        },
        { #4-1-2-2
            "trigger": "advance",
            "source": "C_join",
            "dest": "C2_recentactivity",
            "conditions": "is_going_to_C2_recentactivity",
        },
        { #4-3-1
            "trigger": "advance",
            "source": "C_time",
            "dest": "C2_requirement",
            "conditions": "is_going_to_C2_requirement",
        },
        { #4-3-2
            "trigger": "advance",
            "source": "C_time",
            "dest": "C2_recentactivity",
            "conditions": "is_going_to_C2_recentactivity",
        },
        { #3-2-1
            "trigger": "advance",
            "source": "english",
            "dest": "E_indroduction",
            "conditions": "is_going_to_E_indroduction",
        },
        { #3-2-2
            "trigger": "advance",
            "source": "english",
            "dest": "E_join",
            "conditions": "is_going_to_E_join",
        },
        { #3-2-3
            "trigger": "advance",
            "source": "english",
            "dest": "E_time",
            "conditions": "is_going_to_E_time",
        },
        { #4-1-1
            "trigger": "advance",
            "source": "E_indroduction",
            "dest": "E2_requirement",
            "conditions": "is_going_to_E2_requirement",
        },
        { #4-1-2
            "trigger": "advance",
            "source": "E_indroduction",
            "dest": "E2_recentactivity",
            "conditions": "is_going_to_E2_recentactivity",
        },
        { #4-2-1
            "trigger": "advance",
            "source": "E_join",
            "dest": "E2_requirement",
            "conditions": "is_going_to_E2_requirement",
        },
        { #4-2-2
            "trigger": "advance",
            "source": "E_join",
            "dest": "E2_recentactivity",
            "conditions": "is_going_to_E2_recentactivity",
        },
        { #4-3-1
            "trigger": "advance",
            "source": "E_time",
            "dest": "E2_requirement",
            "conditions": "is_going_to_E2_requirement",
        },
        { #4-3-2
            "trigger": "advance",
            "source": "E_time",
            "dest": "E2_recentactivity",
            "conditions": "is_going_to_E2_recentactivity",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "show_fsm_photo",
            "conditions": "is_going_to_show_fsm_photo",
        },
        {"trigger": "go_back", "source": ["menu","chinese","english","C_indroduction","C_join","C_time","C2_requirement","C2_recentactivity","show_fsm_photo","E_indroduction", "E_join","E_time", "E2_requirement","E2_recentactivity"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


# @app.route("/callback", methods=["POST"])
# def callback():
#     signature = request.headers["X-Line-Signature"]
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     print("helloworld")
#     # parse webhook body
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#    # if event is MessageEvent and message is TextMessage, then echo text
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue

#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=event.message.text)
#         )

#     return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    print(port)
    app.run(host="0.0.0.0", port=port, debug=True)
