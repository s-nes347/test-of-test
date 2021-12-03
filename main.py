import os
import sys
import re
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import ftplib


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    
    word = event.message.text
    if word == "たてくら":
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="ともき")
    )
    
    elif re.match(r"^\d+$",word):
        
        dir_name = "/{}{}".format(word[0], "0"*(len(word)-1))
        pdf_list = []
        web_address = "test9test.html.xdomain.jp"
        
        ftp = ftplib.FTP("sv2.html.xdomain.ne.jp")
        ftp.set_pasv('true')
        ftp.login("test9test.html.xdomain.jp", "pass0347")
        ftp.cwd(dir_name)
        file_list = ftp.nlst(".")
        print(file_list)
        for pdf_path in file_list:
            if pdf_path in word:
                pdf_list.append(web_address + dir_name + "/" + pdf_path)
                
        if not pdf_list:
            for pdf_path in pdf_list:
            
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=pdf_path)
            )
        
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="データがありません。")
            )
            
        
    else:    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="半角数字で入力して下さい。")
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)