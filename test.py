from api import Telegram

TOKEN = "6177676684:AAEQeGI1truZ8YYAyAY5U7ISXSypzWRmU38"

bot = Telegram(TOKEN)


def start(msg):
    return "hello!", [[{"wow": wow}, {"help": help}], [{"mahan": wow}]]


def wow(msg):
    return "Hello!", None


def help(msg):
    print("a")
    return msg.message.text + " is not found! type /start", None


bot.handle(start, "/start")
bot.notHandle(help)

bot.run()
