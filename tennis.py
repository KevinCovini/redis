import redis as rd

r = rd.Redis(
  host='redis-12900.c300.eu-central-1-1.ec2.cloud.redislabs.com',
  port=12900,
  password='uUlKJLiadqj12nYHVKcwK9TowwyuXrvb')


set_redis_game = {'Love' : 0, 
                  '15' : 15, 
                  '30' : 30, 
                  '40' : 40, 
                  'Adv' : 50}

get_redis_game = {0: 'Love', 
                  15: '15', 
                  30: '30', 
                  40: '40', 
                  50: 'Adv'}


if not (r.ping()):
    print("CONNECTION TERMINATED.")
print("Connected")

def setGame(game, set, match):
    r.set("Gamepoints", set_redis_game[game])
    r.set("Setpoints", set)
    r.set("Matchpoints", match)

def getGame(test = False):
    if test:
        game = int(r.get("Gamepoints"))
    else:
        game = get_redis_game[int(r.get("Gamepoints"))]
    return (game, int(r.get("Setpoints")), int(r.get("Matchpoints")))


def incrementScore():
    gamescore = int(r.get("Gamepoints"))

    # Gamepoints
    if gamescore in (0, 15):
        r.incrby("Gamepoints", 15)
    elif (gamescore == 30):
        r.incrby("Gamepoints", 10)
    elif (gamescore == 40):
        r.set("Gamepoints", 0)
        r.incr("Setpoints")

    # Setpoints
    if (int(r.get("Setpoints")) >= 6):
        r.set("Setpoints", 0)
        r.incr("Matchpoints")

    # Matchpoints
    if (int(r.get("Matchpoints")) == 3):
        r.set("Matchpoints", 0)
        print("YOU WON!!!")

setGame("Love", 0, 0)

while True:
    escape = input("Do you want to continue? [0 to escape]: ")
    if (escape == 0):
        break
    incrementScore()
    if (getGame(True) == (0, 0, 0)):
        break
    print(getGame())