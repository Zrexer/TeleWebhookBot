# python3

token: str = ""
ads = [ '' ]

import telebot 
import json
import httpx

class PoulJson(object):
    def __init__(self, jsonData: dict = {}):
        self.js = jsonData
    
    def flex(self, flexRange: int = 4, sortKeys: bool = True):
        return json.dumps(self.js, indent=flexRange, sort_keys=sortKeys)

def setLoop(chatID: str, botToken: str):
    dbs[chatID] = botToken
    return dbs

def getInfo(tokenRe):
    try:
        url = f"https://api.telegram.org/bot{tokenRe}/getWebhookInfo"
        data = httpx.Client().get(url).json()
        return {"local-error" : False, "result" : data}
    except Exception as E:
        return{"local-error" : True, "error-info" : E}

def delHook(tokenRe):
    try:
        url = f"https://api.telegram.org/bot{tokenRe}/deleteWebhook"
        data = httpx.Client().get(url).json()
        return {"local-error" : False, "reuslt" : data}
    except Exception as E:
        return{"local-error" : True, "error-info" : E}
    
def setHook(tokenRe, url):
    try:
        url = f"https://api.telegram.org/bot{tokenRe}/setWebhook?url={url}"
        data = httpx.Client().get(url).json()
        return {"local-error" : False, "result" : data}
    except Exception as E:
        return{"local-error" : True, "error-info" : E}

dbs = {}
chMembers = []

app = telebot.TeleBot(token=token)
print("Started")

@app.message_handler(content_types=['text'], chat_types=['private', 'supergroup'])
def WEBER(msg):
    text = str(msg.text)
    chat = str(msg.chat.id)

    if not chat in chMembers:chMembers.append(chat) if not chat.startswith("-") else None

    if text == "/start":
        app.reply_to(msg, "Give more Information: /info ✨")

    if text == "/info":
        infoData = PoulJson({
            "Save Webhook in Database" : "/save <TOKEN>",
            "Set Webhook": "/web-set <WEBHOOK-URL>",
            "Get Webhook information": "/web-info <TOKEN>",
            "Delete the Webhook" : "/web-del <TOKEN>"
        }).flex()
        app.reply_to(msg, infoData)

    if text.startswith("/save"):
        saver = text.replace("/save ", '')
        if saver == "/save":
            app.reply_to(msg, "🔺 Please Set the Bot Token: /save TOKEN")
        else:
            setLoop(str(msg.from_user.id), saver)
            app.reply_to(msg, "🍷 Your Token was Save in Database")
        
    
    if text.startswith("/web-info"):
        if not str(msg.from_user.id) in dbs.keys():
            app.reply_to(msg, "🔺 Please First Save your bot token in dbs: /save TOKEN")
        else:
            tk = dbs[str(msg.from_user.id)]
            app.reply_to(msg, PoulJson(getInfo(tk)).flex())

    if text.startswith("/web-del"):
        if not str(msg.from_user.id) in dbs.keys():
            app.reply_to(msg, "🔺 Your Token Does not Exists in Database")
        else:
            tk = dbs[str(msg.from_user.id)]
            app.reply_to(msg, PoulJson(delHook(tk)).flex())

    if text.startswith("/web-set"):
        wburl = text.replace("/web-set ", '')
        if wburl == "/web-set":
            app.reply_to(msg, "🔺 Please Set the Webhook URL: /web-set http://webhook.eg/path/to/file")
        
        else:
            if not str(msg.from_user.id) in dbs.keys():
                app.reply_to(msg, "🔺 Your Token Does not Exists in Database")
            else:
                tk = dbs[str(msg.from_user.id)]
                app.reply_to(msg, PoulJson(setHook(tk, wburl)).flex())

    if text == "members" and chat in ads:
        app.reply_to(msg, f"{len(chMembers)} Members 👾")

app.infinity_polling()
