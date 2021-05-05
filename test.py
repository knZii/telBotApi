from api import Telegram

TOKEN = "1781512807:AAG2rV9gkqwC_6A6eQVz6p9ufdNWoKp6UN8"

bot = Telegram(TOKEN)

def start(msg):
    return "hello!", [["wow"]]

def wow(msg):
    print("OMG!")
    return "Hello!", None

def help(msg):
    print("a")
    return msg.message.text + " is not found! type /start", None

bot.handle(start, "/start")
bot.handle(wow, "wow")
bot.notHandle(help)

bot.run()