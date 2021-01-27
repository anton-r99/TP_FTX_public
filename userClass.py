import time


class TwitchUser:
    def __init__(self, name, position, orderTime, client):
        self.name = name
        self.position = position
        self.orderTime = orderTime
        self.userOrders = []
        self.lastLong = 0.0
        self.lastShort = 0.0
        self.lastSL = 0.0
        self.timeout = 60.0
        self.rememberOrder(client)
        self.buySl = "b-sl"
        self.sellSl = "s-sl"

    def initTimeout(self, position, orderTime):
        if position == "!b":
            self.lastLong = orderTime
        elif position == "!s":
            self.lastShort = orderTime
        elif position == self.buySl or position == self.sellSl:
            self.lastSL = orderTime

    def checkTimeout(self, position):
        if position == "!b":
            print("position is !b")
            return self.timePassed(self.timeout, self.lastLong)
        if position == "!s":
            return self.timePassed(self.timeout, self.lastShort)
        if position == self.buySl or position == self.sellSl:
            return self.timePassed(self.timeout, self.lastSL)

    def rememberOrder(self, orderSent):
        self.userOrders.append(orderSent)

    def updateOpenOrders(self, client, ticker):
        currentOrders = client.get_open_orders(ticker)
        for userOrder in enumerate(self.userOrders):
            for index in range(len(currentOrders)):
                for _ in currentOrders[index]:
                    if userOrder[1]['id'] == currentOrders[index]['orderId']:
                        self.userOrders[userOrder[0]] = currentOrders[index]

    def updateOpenTriggerOrders(self, client, ticker):
        currentOrders = client.get_open_trigger_orders(ticker)
        for userOrder in enumerate(self.userOrders):
            for index in range(len(currentOrders)):
                for _ in currentOrders[index]:
                    if userOrder[1]['id'] == currentOrders[index]['orderId']:
                        self.userOrders[userOrder[0]] = currentOrders[index]

    @staticmethod
    def timePassed(timeout, tradeType):
        return time.time() - tradeType > timeout

    def getOrders(self):
        if len(self.userOrders) != 0:
            return self.userOrders
        else:
            return print("No orders")
