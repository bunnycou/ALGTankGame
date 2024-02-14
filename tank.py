import turtle
from math import sin, cos, radians
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
screen = turtle.Screen()
screen.setup(SCREEN_HEIGHT, SCREEN_WIDTH)
screen.tracer(0)
screen.colormode(255)

class Tank:
    def __init__(self, color, x, y, r):
        self.tur = turtle.Turtle()
        self.tur.speed(0)
        self.tur.width(3)
        self.tur.hideturtle()
        self.tur.color(color)
        self.mxSpd = 3
        self.acc = 0.05
        self.rot = r #90 is up
        self.rotspd = 5
        self.spd = 0
        self.posx = x
        self.posy = y
        self.size = 10
    
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
        self.tur.penup()
        self.tur.setpos(x+rad, y)
        self.tur.setheading(90)
        self.tur.pendown()
        self.tur.circle(rad)

    def drawTurret(self, x, y, size):
        self.tur.penup()
        self.tur.setpos(x, y)
        self.tur.setheading(self.rot)
        self.tur.pendown()
        self.tur.forward(size*1.5)

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
        self.tur.clear()
        self.posx += cos(radians(self.rot))*self.spd
        self.posy += sin(radians(self.rot))*self.spd
        self.collisionTickCheck()
        self.draw()
        screen.update()

def main():
    player = Tank((0,0,255), 0,0,90)
    enemy = Tank((255,0,0), 100,100, 0)
    enemy.tick()
    player.tick()
    screen.onkeyrelease(player.slowdown, "Up")
    screen.onkeypress(player.speedup, "Up")
    screen.onkeypress(player.rotL, "Left")
    screen.onkeypress(player.rotR, "Right")
    screen.onkeyrelease(player.fire, "space")
    screen.listen()
    screen.mainloop()

main()