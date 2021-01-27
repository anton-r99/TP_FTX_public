import socket


class TwitchBot:
    def __init__(self, server, port, oauth, bot, channel, owner):
        self.server = server
        self.port = port
        self.oauth = oauth
        self.bot = bot
        self.channel = channel
        self.owner = owner
        self.irc = socket.socket()
        self.irc.connect((self.server, self.port))
        self.irc.send(("PASS " + self.oauth + "\n" +
                       "NICK " + self.bot + "\n" +
                       "JOIN #" + self.channel + "\n").encode())
        self.limitOrders = ["!b", "!s"]
        self.triggerOrders = ["!s-sl", "!b-sl"]
        self.ticker = "ETH-PERP"
        self.defSize = 0.001
        self.triggerType = "stop"
        self.reduce_only = True
        self.cancel = False

    # JOIN CHAT __________________________________

    def joinChat(self):
        Loading = True
        while Loading:
            readbuffer_join = self.irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = self.loadingComplete(line)

    def loadingComplete(self, line):
        if "End of /NAMES list" in line:
            print("Bot has joined " + self.channel + "'s Channel!")
            self.sendMessage("Ape Bot has joined!")
            return False
        else:
            return True

    def sendMessage(self, message):
        messageTmp = "PRIVMSG #" + self.channel + " :" + message
        self.irc.send((messageTmp + "\n").encode())

    @staticmethod
    def getUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        print(user)
        return user

    @staticmethod
    def getMessage(line):
        try:
            message = (line.split(":", 2))[2]
        except:
            message = ""
        return message

    @staticmethod
    def Console(line):
        if "PRIVMSG" in line:
            return False
        else:
            return True

    # JOIN CHAT __________________________________

    # ORDER CHECKING ___________________________________
    def isOrder(self, message):
        messageLen = message.count(" ")
        command = message.split()
        if messageLen == 1 and command[0] in self.limitOrders and command[1].replace('.', '', 1).isdigit() \
                and int(command[1]) != 0:
            return True
        elif messageLen == 1 and command[0] in self.triggerOrders and command[1].replace('.', '', 1).isdigit()\
                and int(command[1]) != 0:
            return True
        else:
            return False


    # ORDER CHECKING ___________________________________

    # LIMIT ORDERS _____________________________________
    @staticmethod
    def getLimitSide(direction):
        if direction == "!b":
            side = "buy"
        elif direction == "!s":
            side = "sell"
        else:
            side = None
        return side

    def getLimitOrder(self, message):
        direction, entry = message.split()
        side = self.getLimitSide(direction)
        postOrder = [self.ticker, side, entry, self.defSize]
        return postOrder

    @staticmethod
    def postLimit(postOrder, client):
        client.place_order(*postOrder, post_only=True)
        print("order has been placed")

    # LIMIT ORDERS _____________________________________

    # TRIGGER ORDERS ___________________________________
    #     UNFINISHED
    # !sell-stop 1100

    @staticmethod
    def checkTriggerOrder(lastPrice, side, trigger):
        if side == "sell" and trigger < lastPrice:
            return True
        elif side == "buy" and trigger > lastPrice:
            return True
        else:
            return False

    @staticmethod
    def getTriggerSide(message):
        if message.split()[0] == "!s-sl":
            return "sell"
        elif message.split()[0] == "!b-sl":
            return "buy"
        else:
            return "wrong syntax"

    @staticmethod
    def getTriggerPrice(message):
        return message.split()[1]

    @staticmethod
    def getStopEntry(side):
        if side == "sell":
            return -0.5
        elif side == "buy":
            return 0.5

    def getTriggerOrder(self, message):
        side = self.getTriggerSide(message)
        trigger = int(self.getTriggerPrice(message))
        entry = trigger + int(self.getStopEntry(side))
        postOrder = [self.ticker, side, self.defSize, self.triggerType, entry, self.reduce_only,
                     self.cancel, trigger]
        print(postOrder)
        return postOrder

    # client.place_conditional_order(market, side, size, type, limit, reduce_only, cancel, trigger)
    # client.place_conditional_order("ETH-PERP", "sell", 0.001, "stop", 1231, True, True, 1232)

    @staticmethod
    def postTrigger(postOrder, client):
        client.place_conditional_order(*postOrder)

    # TRIGGER ORDERS ___________________________________

    # OTHER ____________________________________________

    @staticmethod
    def getFuture(future, client):
        futureInfo = client.get_future(future)
        return futureInfo['last']

    def getNetSize(self, client):
        return client.get_position(self.ticker)["netSize"]

