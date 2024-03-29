import turtle
from math import sin, cos, atan2, radians, degrees, sqrt
# constants for screen size
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

# turtle screen
screen = turtle.Screen()
screen.setup(SCREEN_HEIGHT, SCREEN_WIDTH)
screen.tracer(0)
screen.colormode(255)

class Bullet:
    def __init__(self, x, y, rot, color):
        self.tur = turtle.Turtle()
        self.tur.speed(0)
        self.tur.width(4)
        self.tur.hideturtle()
        self.tur.color(color)
        self.posx = x
        self.posy = y
        self.rot = rot
        self.bspd = 1
        self.size = 10
        self.firing = True

    def spdx(self, rot, spd):
        return cos(radians(rot))*spd
    
    def spdy(self, rot, spd):
        return sin(radians(rot))*spd

    def draw(self):
        self.tur.penup()
        self.tur.goto(self.posx, self.posy)
        self.tur.setheading(self.rot)
        self.tur.pendown()
        self.tur.forward(self.size)

    def distTank(self, posx, posy, tank):
        xterm = (posx-tank.posx)**2
        yterm = (posy-tank.posy)**2
        return sqrt(xterm+yterm)

    def screenCollision(self):
        rightbound = (SCREEN_WIDTH/2)-(self.size*2)
        leftbound = ((SCREEN_WIDTH/2)*-1)+self.size
        if self.posx > rightbound: # off the right
            return True
        if self.posx < leftbound: # off the left
            return True

        topbound = (SCREEN_HEIGHT/2)-self.size
        botbound = ((SCREEN_HEIGHT/2)*-1)+(self.size*2)
        if self.posy > topbound: # off the top
            return True
        if self.posy < botbound: # off the bottom
            return True
        
        return False

    def tankCollision(self, AllTanks):
        testx = self.posx + self.spdx(self.rot, self.size)
        testy = self.posy + self.spdy(self.rot, self.size)
        for tank in AllTanks:
            if self.distTank(testx, testy, tank) < tank.size:
                return tank
        return False

    def tick(self, AllTanks):
        self.tur.clear()
        if self.firing:
            self.posx += self.spdx(self.rot, self.bspd)
            self.posy += self.spdy(self.rot, self.bspd)

            if self.screenCollision(): 
                self.firing = False 
                return

            if self.tankCollision(AllTanks): 
                self.firing = False
                return

            self.draw()
            

# class for main tank (player and all tanks) that AI tank uses as parent
class Tank:
    def __init__(self, color, x, y, r):
        # turtle properties for each tank
        self.tur = turtle.Turtle()
        self.tur.speed(0)
        self.tur.width(3)
        self.tur.hideturtle()
        self.tur.color(color)
        # list to store fired bullets and cooldown between shots
        self.bullets = list()
        self.cooldown = 0
        self.basecd = 100
        # basic properties like speed, position, rotation
        self.driving = False
        self.rot = r #90 is up
        self.rotspd = 0 
        self.basespdrot = 1 # should be a divisor of 360
        self.rotating = False
        # self.spd = 0
        self.basespd = 0.25
        self.posx = x
        self.posy = y
        self.size = 10

        self.color = color

    def turretSize(self):
        return self.size*1.5
    
    # util functions for speed of tank and bullet
    def spdx(self, rot, spd):
        return cos(radians(rot))*spd
    
    def spdy(self, rot, spd):
        return sin(radians(rot))*spd
    
    # functions to rotate right and left
    def rotR(self):
        self.startRot(self.basespdrot*-1)
    
    def rotL(self):
        self.startRot(self.basespdrot)

    # functions to start moving and stop moving
    def start(self):
        self.driving = True

    def stop(self):
        self.driving = False

    def startRot(self, spd):
        self.rotating = True
        self.rotspd = spd

    def stopRot(self):
        self.rotating = False

    # function called when you shoot
    def fire(self):
        if self.cooldown != 0:
            return # do not shoot if on cooldown
        else:
            self.bullets.append(Bullet(self.posx, self.posy, self.rot, self.color))
            self.cooldown = self.basecd
    
    # calls other functions to draw the full tank
    def draw(self):
        self.drawBody()
        self.drawTurret()
        
    def drawBody(self):
        self.tur.penup()
        self.tur.setpos(self.posx+self.size, self.posy)
        self.tur.setheading(90)
        self.tur.pendown()
        self.tur.circle(self.size)

    def drawTurret(self):
        self.tur.penup()
        self.tur.setpos(self.posx, self.posy)
        self.tur.setheading(self.rot)
        self.tur.pendown()
        self.tur.forward(self.turretSize())

    # util functions for finding distance/rotation between tank and self
    def distTank(self, tank):
        xterm = (self.posx-tank.posx)**2
        yterm = (self.posy-tank.posy)**2
        return sqrt(xterm+yterm)

    def rotTank(self, tank):
        xterm = self.posx-tank.posx
        yterm = self.posy-tank.posy
        return degrees(atan2(yterm, xterm)+radians(180))

    def rotCollisionTank(self, tank):
        xterm = self.posx-tank.posx
        yterm = self.posy-tank.posy
        return degrees(atan2(yterm, xterm))

    # checks if tank is hitting anything every tick
    def collisionTickCheck(self, AllTanks):
        #check screen border collisions
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

        # check tank to tank collision
        for tank in AllTanks:
            if self.distTank(tank) < (self.size+tank.size): # if collide
                spd = (self.basespd * len(AllTanks))/2 # dividing by 2 allows tanks to push each other
                rot = self.rotCollisionTank(tank)
                self.posx += self.spdx(rot, spd)
                self.posy += self.spdy(rot, spd)

    def sortDistAI(self, AllTanks):
        tanksDist = list()
        tanksOrder = [_ for _ in range(1, len(AllTanks)+1)]

        for i in range(len(AllTanks)):
            tanksDist.append(self.distTank(AllTanks[i]))

        unsorted = True
        while unsorted:
            unsorted = False
            for i in range(len(AllTanks)-1):
                if tanksDist[i] > tanksDist[i+1]:
                    tanksDist[i], tanksDist[i+1] = tanksDist[i+1], tanksDist[i]
                    tanksOrder[i], tanksOrder[i+1] = tanksOrder[i+1], tanksOrder[i]
                    unsorted = True
        
        return tanksDist, tanksOrder

    # performs movememnt, drawing, and any collision checks
    def tick(self, AllTanks):
        self.tur.clear()
        if self.rotating:
            self.rot += self.rotspd
        if self.driving:
            spd = self.basespd * len(AllTanks)
            self.posx += cos(radians(self.rot))*spd
            self.posy += sin(radians(self.rot))*spd
        if self.cooldown > 0:
            self.cooldown -= 1
        # print(self.bullets)
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.tick(AllTanks)
                if not bullet.firing:
                    self.bullets.remove(bullet)
        self.collisionTickCheck(AllTanks)
        tanksDist, tanksOrder = self.sortDistAI(AllTanks)
        print("Tanks in Distance Order")
        for i in range(len(tanksDist)):
            print(tanksOrder[i], tanksDist[i])
        self.draw()

# subclass of Tank for non player tanks
class TankAI(Tank):
    def __init__(self, color, x, y, r, num):
        super(TankAI, self).__init__(color, x, y, r)
        self.rotspd = 0.2
        self.basespd = 0.1
        self.id = num

    def AI_drive(self, player): # drive
        self.start()
        if self.distTank(player) < 75:
            self.stop()
    
    def AI_rot(self, player): # rotate ai tank towards player
        goalRot = self.rotTank(player) # rotation that would face ai towards player
        if self.rot > goalRot+1: # if need to rotate right without passing 0
            lrotd = 360-self.rot+goalRot
            rrotd = self.rot-goalRot
        elif self.rot < goalRot-1: # if need to rotate left without passing 0
            lrotd = goalRot-self.rot
            rrotd = self.rot+360-goalRot
        else: # if rotation is equal to the goal rotation
            return

        if lrotd < rrotd: # if left is faster
            self.rot += self.rotspd # rotate left
        else: # if right is faster or equal
            self.rot -= self.rotspd # rotate right

        # correct rotation to be between 0-360
        if self.rot > 360: self.rot-=360
        if self.rot < 0: self.rot+=360
    
    def tick(self, AllTanks, player):
        self.tur.clear()
        self.AI_rot(player) # rotate tank towards player
        self.AI_drive(player)
        if self.driving:
            spd = self.basespd * len(AllTanks)
            self.posx += cos(radians(self.rot))*spd
            self.posy += sin(radians(self.rot))*spd
        self.collisionTickCheck(AllTanks)
        self.draw()

# where the program starts
def main():
    # create tanks and add them to lists of enemy tanks and all tanks
    player = Tank((0,0,255), 0,0,90)
    # create enemy tanks
    enemyTanks = list()
    enemyTanks.append(TankAI((255,0,0), -100,-100,90, 1))
    enemyTanks.append(TankAI((255,0,0), 100,100,90, 2))
    # all tanks list
    AllTanks = list()
    AllTanks.append(player)
    for tank in enemyTanks:
        AllTanks.append(tank)
    # register keybinds
    screen.onkeypress(player.start, "Up")
    screen.onkeyrelease(player.stop, "Up")
    screen.onkeypress(player.rotL, "Left")
    screen.onkeyrelease(player.stopRot, "Left")
    screen.onkeypress(player.rotR, "Right")
    screen.onkeyrelease(player.stopRot, "Right")
    screen.onkeyrelease(player.fire, "space")
    screen.listen()
    # main game loop
    while True:
        player.tick(AllTanksbutThisOne(AllTanks, player))
        for tank in enemyTanks:
            tank.tick(AllTanksbutThisOne(AllTanks, tank), player)
        screen.update()

def AllTanksbutThisOne(AllTanks, tank):
    return [t for t in AllTanks if t != tank]

main()
