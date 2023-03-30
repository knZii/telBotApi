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
        self.notHandleFunc = func

    def sendMessage(self, chat_id, msg, keyboard=None) -> bool:
        if keyboard is None:
            r = requests.get("https://api.telegram.org/bot" + self.token +
                             "/sendMessage", params={"chat_id": chat_id, "text": msg})
        else:
            k = json.dumps(keyboard)
            r = requests.get("https://api.telegram.org/bot" + self.token + "/sendMessage",
                             params={"chat_id": chat_id, "text": msg, "reply_markup": k})
        r = r.json()
        return r["ok"]

    def run(self):
        lastUpdateID = 0
        while True:
            r = requests.get("https://api.telegram.org/bot" + self.token +
                             "/getUpdates", params={"offset": lastUpdateID+1})
            r = r.text
            r = json.loads(r, object_hook=lambda d: SimpleNamespace(**d))
            r = r.result
            if r != []:
                lastUpdateID = r[-1].update_id
            for msg in r:
                if not hasattr(msg, "message"):
                    continue
                # can be message/photo/...

                if not hasattr(msg.message, "text"):
                    continue
                # now its message
                is_handled = False
                for i in self.handles:
                    if msg.message.text == i[1]:

                        msgForSend, kb = i[0](msg)
                        if kb is not None:
                            keyb = []
                            for i in kb:
                                row = []
                                for j in i:
                                    self.handle(list(j.values())[
                                                0], list(j.keys())[0])
                                    row.append(list(j.keys())[0])
                                keyb.append(row)
                            k = {"keyboard": keyb, "resize_keyboard": True}
                        else:
                            k = None
                        if msgForSend is not None:
                            self.sendMessage(
                                msg.message.chat.id, msgForSend, k)
                        is_handled = True
                if not is_handled:
                    msgForSend, kb = self.notHandleFunc(msg)
                    if msgForSend is not None:
                        if kb is not None:
                            k = {"keyboard": kb, "resize_keyboard": True}
                        else:
                            k = None
                        self.sendMessage(msg.message.chat.id, msgForSend, k)
