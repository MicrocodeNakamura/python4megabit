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
    def __init__(self, name, color, xy_vect, aim_vect, left_k, right_k ):
        self.name = name
        self.color = color
        self.xy = xy_vect
        self.aim = aim_vect
        self.body = set ()
        self.handle = 0
        self.head = vector(0, 0)
        self.leftkey = left_k
        self.rightkey = right_k
        self.alive = True

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

# main program. 

# 入力を受け付けるキーデータの種類

# パラメータの初期化処理。 プレイヤーの数は、以下の行の数で決定することができる。
# 初期ベクトル及び、初期方向の値は、必ず初期ベクトルの値（４の倍数）であること。
# ４の倍数でない場合は、当たり判定が真にならない。
players = []
#                                  name       body color       inital pos    initial dir      leftkey rightley
#--------------------------------------------------------------------------------------------------------------
players.append ( playerContainer ( 'player1', 'orange' , vector(-160,  180), vector(  4, 0 ) ,'Left', 'Right' ) )
players.append ( playerContainer ( 'player2', 'red'    , vector(-160,  120), vector(  4, 0 ) ,'1'   , '2'     ) )
#players.append ( playerContainer ( 'player3', 'purple' , vector(-160,   60), vector(  4, 0 ) ,'4'   , '5'     ) )
#players.append ( playerContainer ( 'player4', 'green'  , vector(160,   -60), vector( -4, 0 ) ,'7'   , '8'     ) )
#players.append ( playerContainer ( 'player5', 'blue'   , vector(160,  -120), vector( -4, 0 ) ,'q'   , 'w'     ) )
#players.append ( playerContainer ( 'player6', 'aqua'   , vector(160,  -180), vector( -4, 0 ) ,'r'   , 't'     ) )

def inside(head):
    "Return True if head inside screen."
    return -200 < head.x < 200 and -200 < head.y < 200

p1handle = 0
sleepTime = 100
subTime   = 0

# 当たり判定
def hitcheck( player ):
    for wall in players:
        if player.head in wall.body:
            return True
    return False

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
        if not inside(player.head) or hitcheck( player ):
            print('Player ' + player.color + ' lose!')
            square(player.xy.x, player.xy.y, 3, 'Black' )
            update()
            
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

if len( players) > 0:
    onkey(lambda: players[0].pnLeft(),  players[0].leftkey )
    onkey(lambda: players[0].pnRight(), players[0].rightkey )
if len( players) > 1:
    onkey(lambda: players[1].pnLeft(),  players[1].leftkey )
    onkey(lambda: players[1].pnRight(), players[1].rightkey )
if len( players) > 2:
    onkey(lambda: players[2].pnLeft(),  players[2].leftkey )
    onkey(lambda: players[2].pnRight(), players[2].rightkey )
if len( players) > 3:
    onkey(lambda: players[3].pnLeft(),  players[3].leftkey )
    onkey(lambda: players[3].pnRight(), players[3].rightkey )
if len( players) > 4:
    onkey(lambda: players[4].pnLeft(),  players[4].leftkey )
    onkey(lambda: players[4].pnRight(), players[4].rightkey )
if len( players) > 5:
    onkey(lambda: players[5].pnLeft(),  players[5].leftkey )
    onkey(lambda: players[5].pnRight(), players[5].rightkey )
draw()
done()
