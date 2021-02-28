from userClass import TwitchUser
import time

orders = ["!b", "!s", "!b-sl", "!s-sl"]
users = []


def firstArg(message):
    return message.split()[0]


def sendOrder(newMessage, client, newUser, twitchBot):
    # check if user have already sent orders in the past
    orderSent = []
    if not any(searchUser.name == newUser for searchUser in users):
        if firstArg(newMessage) == orders[0] or firstArg(newMessage) == orders[1]:
            newOrder = twitchBot.getLimitOrder(newMessage)
            orderSent = twitchBot.postLimit(newOrder, client)
        elif firstArg(newMessage) == orders[2] or firstArg(newMessage) == orders[3]:
            newOrder = twitchBot.getTriggerOrder(newMessage)
            orderSent = twitchBot.postTrigger(newOrder, client)
        userOrderTime = time.time()
        userPosition = newMessage.split()[0]
        users.append(TwitchUser(newUser, userPosition, userOrderTime, client))
        for user in users:
            if user.name == newUser:
                user.initTimeout(userPosition, userOrderTime)
                user.rememberOrder(orderSent)

    else:
        for user in users:
            if user.name == newUser and user.checkTimeout(firstArg(newMessage)):
                if firstArg(newMessage) == orders[0] or firstArg(newMessage) == orders[1]:
                    newOrder = twitchBot.getLimitOrder(newMessage)
                    orderSent = twitchBot.postLimit(newOrder, client)
                elif firstArg(newMessage) == orders[2] or firstArg(newMessage) == orders[3]:
                    newOrder = twitchBot.getTriggerOrder(newMessage)
                    orderSent = twitchBot.postTrigger(newOrder, client)
                orderTime = time.time()
                user.initTimeout(firstArg(newMessage), orderTime)
                user.rememberOrder(orderSent)
