from ftx import FtxClient
from twitchBotClass import TwitchBot
from general import sendOrder
import twitchConstants

# FTX -----------------------
API_KEY = ""
API_SECRET = ""
# FTX -----------------------
client = FtxClient(api_secret=API_SECRET, api_key=API_KEY)

# ___________________________
# (symbol, side, price, qty)

# (symbol, side, price,qty, type)
# ___________________________

# create bot obj

twitchBot = TwitchBot(server=twitchConstants.SERVER,
                      port=twitchConstants.PORT,
                      oauth=twitchConstants.PASS,
                      bot=twitchConstants.BOT,
                      channel=twitchConstants.CHANNEL,
                      owner=twitchConstants.OWNER)

twitchBot.joinChat()

# allOrders = []

# start reading chat
while True:
    try:
        readbuffer = twitchBot.irc.recv(1024).decode()
    except:
        readbuffer = ""
    for text in readbuffer.split("\r\n"):
        if text == "":
            continue
        else:
            # get user name, get message text
            newUser = twitchBot.getUser(text)
            newMessage = twitchBot.getMessage(text)
            if newMessage[0] == "!":
                if twitchBot.isOrder(newMessage):   # and twitchBot.whatOrder(newMessage)
                    print("trying")
                    sendOrder(newMessage, client, newUser, twitchBot)
