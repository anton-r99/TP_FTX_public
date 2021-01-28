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
            print("trying to post a limit order")
            orderSent = twitchBot.postLimit(newOrder, client)
            print("limit has been sent")
        elif firstArg(newMessage) == orders[2] or firstArg(newMessage) == orders[3]:
            newOrder = twitchBot.getTriggerOrder(newMessage)
            orderSent = twitchBot.postTrigger(newOrder, client)
            print("trigger has been sent")
        userOrderTime = time.time()
        userPosition = newMessage.split()[0]
        users.append(TwitchUser(newUser, userPosition, userOrderTime, client))
        for user in users:
            if user.name == newUser:
                user.initTimeout(userPosition, userOrderTime)
                user.rememberOrder(orderSent)
                #print(user.getOrders())

    else:
        for user in users:
            print("checking time out")
            if user.name == newUser and user.checkTimeout(firstArg(newMessage)):
                print("Cheking what order")
                if firstArg(newMessage) == orders[0] or firstArg(newMessage) == orders[1]:
                    newOrder = twitchBot.getLimitOrder(newMessage)
                    orderSent = twitchBot.postLimit(newOrder, client)
                elif firstArg(newMessage) == orders[2] or firstArg(newMessage) == orders[3]:
                    print("this is a trigger order")
                    newOrder = twitchBot.getTriggerOrder(newMessage)
                    print("generated trigger order")
                    orderSent = twitchBot.postTrigger(newOrder, client)
                    print("trigger has been sent")
                # newOrder = twitchBot.getLimitOrder(newMessage)
                # twitchBot.postLimit(newOrder, client)
                orderTime = time.time()
                user.initTimeout(firstArg(newMessage), orderTime)
                user.rememberOrder(orderSent)
                #user.updateOpenOrders(client, twitchBot.ticker)
                #print(user.getOrders())

