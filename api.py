import requests
from types import SimpleNamespace
import json

class Telegram:
    def __init__(self, token):
        self.token = token
        self.handles = []
    def handle(self, func, msg):
        self.handles.append([func, msg])

    def notHandle(self, func):
        self.notHandle = func

    def sendMessage(self, chat_id, msg, keyboard=None, resize_keyboard=False, one_time_keyboard=False) -> bool:
        if keyboard is None:
            r = requests.get("https://api.telegram.org/bot"+ self.token +"/sendMessage", params= {"chat_id": chat_id, "text": msg})
        else:
            k = {"keyboard": keyboard, "resize_keyboard": resize_keyboard, "one_time_keyboard": one_time_keyboard}
            k = json.dumps(k)
            r = requests.get("https://api.telegram.org/bot"+ self.token +"/sendMessage", params= {"chat_id": chat_id, "text": msg, "reply_markup": k})
        r = r.json()
        return r["ok"]
    def run(self):
        lastUpdateID = 0
        while True:
            r = requests.get("https://api.telegram.org/bot"+ self.token +"/getUpdates", params={"offset": lastUpdateID+1})
            r = r.text
            r = json.loads(r, object_hook=lambda d: SimpleNamespace(**d))
            r = r.result
            if r != []:
                lastUpdateID = r[-1].update_id
            
            for msg in r:
                is_handled = False
                for i in self.handles:
                    if msg.message.text == i[1]:
                        msgForSend, kb = i[0](msg)
                        if msgForSend is not None:
                            self.sendMessage(msg.message.chat.id, msgForSend, kb, resize_keyboard=True)
                        is_handled = True
                if not is_handled:
                    msgForSend, kb = self.notHandle(msg)
                    if msgForSend is not None:
                            self.sendMessage(msg.message.chat.id, msgForSend, kb, resize_keyboard=True)