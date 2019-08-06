"""Tron, classic arcade game.

Exercises

1. Make the tron players faster/slower.
2. Stop a tron player from running into itself.
3. Allow the tron player to go around the edge of the screen.
4. How would you create a computer player?

"""
import sys
import time
from turtle import *
from freegames import square, vector

class playerContainer:
    def __init__(self, name, color, xy_vect, aim_vect ):
        self.name = name
        self.color = color
        self.xy = xy_vect
        self.aim = aim_vect
        self.body = set ()
        self.handle = 0
        self.head = vector(0, 0)

    def pnLeft( self ):
        self.handle -= 1
        if ( self.handle <= -6 ):
            self.handle += 6
            self.aim.rotate(90)

    def pnRight( self ):
        self.handle += 1
        if ( self.handle >= 6 ):
            self.handle -= 6
            self.aim.rotate(-90)

p1xy = vector(-100, -50)
p1aim = vector(4, 0)
p1body = set()

p2xy = vector(100, 50)
p2aim = vector(-4, 0)
p2body = set()

players = []
players.append ( playerContainer ( 'player1', 'orange' , vector(-160,  180), vector(  4, 0 ) ) )
players.append ( playerContainer ( 'player2', 'red'    , vector(-160,  120), vector(  4, 0 ) ) )
players.append ( playerContainer ( 'player3', 'purple' , vector(-160,   60), vector(  4, 0 ) ) )
players.append ( playerContainer ( 'player4', 'green'  , vector(160,   -60), vector( -4, 0 ) ) )
players.append ( playerContainer ( 'player5', 'blue'   , vector(160,  -120), vector( -4, 0 ) ) )
players.append ( playerContainer ( 'player6', 'aqua'   , vector(160,  -180), vector( -4, 0 ) ) )

def inside(head):
    "Return True if head inside screen."
    return -200 < head.x < 200 and -200 < head.y < 200

p1handle = 0
sleepTime = 100
subTime   = 0


def draw():
    global sleepTime
    global subTime

# 6 players の動作を描画し判定する
    "Advance players and draw game."
    for player in players:
        player.xy.move(player.aim)
        player.head = player.xy.copy()

    # change to p1 , hit check on p1 self.
    for player in players:
        if not inside(player.head) or player.head in players[0].body or player.head in players[1].body \
            or player.head in players[2].body or player.head in players[3].body or player.head in players[4].body \
            or player.head in players[5].body:
            print('Player blue wins!')
            time.sleep(5)
            sys.exit(0)
    # hit したらそのPlayerのライフフラグを折る。 （game over） TODO
    #        return

    for player in players:
        player.body.add( player.head )
        square(player.xy.x, player.xy.y, 3, player.color )
#        square(player.xy.x, player.xy.y, 4, player.color )

    update()

    # include players speed. Change game barance here.
    ontimer(draw, sleepTime)
#    ontimer(draw, 100)
    # Todo change level up time and curve.
    subTime += sleepTime
#    if subTime > (sleepTime):
    if subTime > (10000):
        subTime = 0
        sleepTime -=  10
        print ("Speed up" + str ( sleepTime ) )

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: players[0].pnLeft(),  'Left')
onkey(lambda: players[0].pnRight(), 'Right')
onkey(lambda: players[1].pnLeft(),  'j')
onkey(lambda: players[1].pnRight(), 'l')
draw()
done()
