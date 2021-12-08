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

# get Config Vars
#line
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
#ftp
web_address = os.getenv('WEB_ADDRESS', None)
ftp_path = os.getenv('FTP_PATH', None)
ftp_pass = os.getenv('FTP_PASS', None)

#確認用
if channel_secret is None:
    print('LINE_CHANNEL_SECRETがありません')
    sys.exit(1)
if channel_access_token is None:
    print('LINE_CHANNEL_ACCESS_TOKENがありません')
    sys.exit(1)
if web_address is None:
    print('WEB_ADDRESSがありません')
    sys.exit(1)
if ftp_path is None:
    print('FTP_PATHがありません')
    sys.exit(1)
if ftp_pass is None:
    print('FTP_PASSがありません')
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
                
        ftp = ftplib.FTP(ftp_path)
        ftp.set_pasv('true')
        ftp.login(web_address, ftp_pass)
        
        try:
            ftp.cwd(dir_name)
            file_list = ftp.nlst(".")
            for pdf_path in file_list:
                if word in pdf_path:
                    pdf_list.append(web_address + dir_name + "/" + pdf_path)
                    
            if pdf_list:
                num = len(pdf_list)
                
                if num == 1:
                
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=pdf_list[0])
                )
                    
                elif num == 2:
                    
                    line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=pdf_list[0]), TextSendMessage(text=pdf_list[1])]
                )

                else:
                    
                    line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=pdf_list[0]), TextSendMessage(text=pdf_list[1]), TextSendMessage(text=pdf_list[2])]
                )
                      
            else:
                #print("NO2")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="データがありません。")
                )
        
        except :
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