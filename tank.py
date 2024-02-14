import turtle
from math import sin, cos, radians
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
screen = turtle.Screen()
screen.setup(SCREEN_HEIGHT, SCREEN_WIDTH)
screen.tracer(0)
tur = turtle.Turtle()
tur.speed(0)
tur.width(4)
tur.hideturtle()
tur.color(0,0,0)

class Tank:
    def __init__(self):
        pass

    mxSpd = 3
    acc = 0.05
    rot = 90 #pointing up
    rotspd = 3
    spd = 0
    posx = 0
    posy = 0
    size = 10
    
    def rotR(self):
        self.rot -= self.rotspd
        self.tick()
    
    def rotL(self):
        self.rot += self.rotspd
        self.tick()

    def speedup(self):
        self.spd += self.acc
        if self.spd > self.mxSpd:
            self.spd = self.mxSpd
        self.tick()

    def slowdown(self):
        self.spd = 0
        self.tick()

    def fire(self):
        print("pew")
    
    def draw(self):
        self.drawBody(self.posx, self.posy, self.size)
        self.drawTurret(self.posx, self.posy, self.size)
        
    def drawBody(self, x, y, rad):
        tur.penup()
        tur.setpos(x+rad, y)
        tur.setheading(90)
        tur.pendown()
        tur.circle(rad)

    def drawTurret(self, x, y, size):
        tur.penup()
        tur.setpos(x, y)
        tur.setheading(self.rot)
        tur.pendown()
        tur.forward(size*1.5)

    def collisionTickCheck(self):
        rightbound = (SCREEN_WIDTH/2)-(self.size*2)
        leftbound = ((SCREEN_WIDTH/2)*-1)+self.size
        if self.posx > rightbound: # off the right
            self.posx = rightbound
        if self.posx < leftbound: # off the left
            self.posx = leftbound

        topbound = (SCREEN_HEIGHT/2)-self.size
        botbound = ((SCREEN_HEIGHT/2)*-1)+(self.size*2)
        if self.posy > topbound: # off the top
            self.posy = topbound
        if self.posy < botbound: # off the bottom
            self.posy = botbound

    def tick(self):
        tur.clear()
        self.posx += cos(radians(self.rot))*self.spd
        self.posy += sin(radians(self.rot))*self.spd
        self.collisionTickCheck()
        self.draw()
        screen.update()

def main():
    player = Tank()
    player.tick()
    screen.onkeyrelease(player.slowdown, "Up")
    screen.onkeypress(player.speedup, "Up")
    screen.onkeypress(player.rotL, "Left")
    screen.onkeypress(player.rotR, "Right")
    screen.onkeyrelease(player.fire, "space")
    screen.listen()
    screen.mainloop()

main()