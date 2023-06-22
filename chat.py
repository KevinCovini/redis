import redis as rd
r = rd.Redis(
  host='redis-12900.c300.eu-central-1-1.ec2.cloud.redislabs.com',
  port=12900,
  password='uUlKJLiadqj12nYHVKcwK9TowwyuXrvb')


#r.set("currentuserid", 0)
currentuserid = int(r.get("currentuserid"))

def login(register = False):
    if register:
        username = input("Insert your new username: ")
        password = input("Insert your password: ")
        confirm = input("Confirm your password: ")
        if password == confirm:
            r.hmset("user:{currentuserid}", {
                "username": username,
                "password": password,
                "messagesent": 0
            })
        r.incr("currentuserid")
    else:
        username = input("Insert your username: ")

def sendMessage():
    return 0

def getMessages():
    return 0
