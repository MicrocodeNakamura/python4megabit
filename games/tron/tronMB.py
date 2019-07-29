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

p1xy = vector(-100, -50)
p1aim = vector(4, 0)
p1body = set()

p2xy = vector(100, 50)
p2aim = vector(-4, 0)
p2body = set()

def inside(head):
    "Return True if head inside screen."
    return -200 < head.x < 200 and -200 < head.y < 200

p1handle = 0
sleepTime = 100
subTime   = 0

def p1Left():
    global p1handle
    p1handle -= 1
    if ( p1handle <= -6 ):
        p1handle += 6
        p1aim.rotate(90)

def p1Right():
    global p1handle
    p1handle += 1
    if ( p1handle >= 6 ):
        p1handle -= 6
        p1aim.rotate(-90)

def draw():
    global sleepTime
    global subTime

    "Advance players and draw game."
    p1xy.move(p1aim)
    p1head = p1xy.copy()

    p2xy.move(p2aim)
    p2head = p2xy.copy()

    # change to p1 , hit check on p1 self.
    if not inside(p1head) or p1head in p2body or p1head in p1body:
        print('Player blue wins!')
        time.sleep(5)
        sys.exit(0)
#        return

    if not inside(p2head) or p2head in p1body or p2head in p2body:
        print('Player red wins!')
        time.sleep(5)
        sys.exit(0)
#        return

    p1body.add(p1head)
    p2body.add(p2head)

    square(p1xy.x, p1xy.y, 3, 'red')
    square(p2xy.x, p2xy.y, 3, 'blue')
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
#onkey(lambda: p1aim.rotate(90), 'Left')
#onkey(lambda: p1aim.rotate(-90), 'Right')
onkey(p1Left,  'Left')
onkey(p1Right, 'Right')
onkey(lambda: p2aim.rotate(90), 'j')
onkey(lambda: p2aim.rotate(-90), 'l')
draw()
done()
