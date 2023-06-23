import redis as rd
import re

r = rd.Redis(
  host='redis-12900.c300.eu-central-1-1.ec2.cloud.redislabs.com',
  port=12900,
  password='uUlKJLiadqj12nYHVKcwK9TowwyuXrvb')

# CONSTANTS

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

MAIN_MENU = '''
[1] Log in
[2] Register
CHOOSE: '''

MESSAGE_MENU = '''
[1] Send messages
[2] View last messages in chat
[3] Get your last 5 messages
CHOOSE: '''

# Email checker
def check_email(email):
    if(re.fullmatch(EMAIL_REGEX, email)):
        return True
    else:
        return False

# Login/register function
def login(register = False):
    if register:
        while True:
            email = input("Insert your email: ")
            if (r.exists(email) == 0):
                break
            elif (not check_email(email)):
                print("")
            print("Email already in use!")
        while True:
            password = input("Insert your password: ")
            confirm = input("Confirm your password: ")
            if (password == confirm):
                break
            print("Password does not match confirm!")
        username = input("Insert your new username: ")
        r.hmset(email, {
            "username": username,
            "password": password,
            "messagesent": 0
        })
        return email
    else:
        email = input("Insert your username: ")
        password = input("Insert your password: ")
        confirm = r.hget(email, "password")
        if (password == confirm):
            print("Login successful!")
            return email

# Sends a message
def sendMessage(email):
    msg = input("Send a message: ")
    r.lpush(f"message:{email}", msg)
    r.lpush("message:all", msg)

# Gets last 5 messages from a user or get the last 20 messages in chat
def getMessages(email = None, all_users = False):
    if all_users:
        messages = r.lrange("message:all", 0, 20)
    else:
        messages = r.lrange(f"message:{email}", 0, 5)
    print(*messages, sep="\n")

if (__name__ == "__main__"):
    try: 
        selection = int(input(MAIN_MENU))
        if selection == 1:
            user = login()
        elif selection == 2:
            user = login(register=True)
        else:
            raise ValueError
    except:
        raise ValueError
    
    try:
        selection = int(input(MESSAGE_MENU))
        if selection == 1:
            sendMessage(user)
        elif selection == 2:
            getMessages(all_users=True)
        elif selection == 3:
            getMessages(user)
        else:
            raise ValueError
    except:
        raise ValueError