import pygame, random, sys, math, copy
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 1200
WINDOWHEIGHT = 900

# color
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
gray = (128,128,128)
darkgray = (40,40,40)

# initial setting
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf' 18)
pygame.display.set_caption('Pathfinder')

# class
class Cworld:
    actors = []
    size = 9600, 9600
    
    def tick():
        for actor in actors:
            actor.action()
            
class Cinterface:
    cameraX = 0.0
    cameraY = 0.0
    cameraWidth = 1200
    cameraHeight = 600
    
    mouseDownX = 0
    mouseDownY = 0
    mouseUpX = 0
    mouseUpY = 0
    
    # state: normal, move, attack, patrol, gather, buildtownhall, buildhouse, buildbarrack, selectbuilding
    state = "normal"
    troops = []
    mouseTriggers = [] # [x,y,width, height, [function, arg, ...]]
    keyboardTriggers = [] # [key, [function, arg, ...]]
    
    def moveCameraToActor(self, actor):
        self.cameraX = actor.position[0] - 600
        self.cameraY = actor.position[1] - 300
        if self.cameraX < 0:
            cameraX = 0
        if self.cameraY < 0:
            cameraY = 0

    def selectActor(self, actor):
        self.troops = [actor]
        
    def move(self):
        self.state = "move"
    
    def attack(self):
        self.state = "attack"
    
    def patrol(self):
        self.state = "patrol"
    
    def build(self):
        self.state = "build"
    
    def buildtownhall(self):
        self.state = "buildtownhall"
    
    def buildhouse(self):
        self.state = "buildhouse"
    
    def buildbarrack(self):
        self.state = "buildbarrack"
    
    def iscollideActor(self, posX, posY):
        # return actor collide to given position. actor collisionos circle.
        for actor in world.actors:
            if (actor.position[0] - posX - self.CameraX)**2 + (actor.position[1] - posY - self.CameraY)**2 <= actor.size**2:
                return actor
        return -1
    
    def moveCommand(self, posX, posY):
        # command actor. moveground or movetarget
        actor = iscollideActor(posX, posY)
        if actor == -1:
            for troop in self.troops:
                troop.destination = [posX + self.cameraX, posY + self.cameraY]
                troop.command = "moveground"
        else:
            for troop in self.troops:
                troop.target = actor
                troop.command = "movetarget"
                
    def movetargetCommand(self, target):
        for troop in self.troops:
            troop.target = target
            troop.command = "movetarget"
            
    def attackCommand(self, posX, posY):
        # command actor. moveground or movetarget
        actor = iscollideActor(posX, posY)
        if actor == -1:
            for troop in self.troops:
                troop.destination = [posX + self.cameraX, posY + self.cameraY]
                troop.command = "attackground"
        else:
            for troop in self.troops:
                troop.target = actor
                troop.command = "attacktarget"
                
    def attacktargetCommand(self, target):
        for troop in self.troops:
            troop.target = target
            troop.command = "attacktarget"
            
    def patrolCommand(self, posX, posY):
        # command actor. moveground or movetarget
        actor = iscollideActor(posX, posY)
        if actor == -1:
            for troop in self.troops:
                troop.destination = [posX + self.cameraX, posY + self.cameraY]
                troop.source = copy.deepcopy(troop.position)
                troop.command = "patrolground"
        else:
            for troop in self.troops:
                troop.target = actor
                troop.source = copy.deepcopy(troop.position)
                troop.command = "patroltarget"
                
    def patroltargetCommand(self, target):
        for troop in self.troops:
            troop.target = target
            troop.source = copy.deepcopy(troop.position)
            troop.command = "attacktarget"
            
    def stopCommand(self):
        for troop in self.troops:
            troop.command = "stop"
            
    def holdCommand(self):
        for troop in self.troops:
            troop.command = "hold"
            
    def gatherCommand(self, posX, posY):
        # gather target or invalid
        actor = iscollideActor(posX, posY)
        if actor.name == "food":
            for troop in self.troops:
                troop.target = actor
                troop.command = "gather"
                
    def buildtownhallCommand(self, posX, posY):
        self.troop[0].destination = [posX, posY]
        self.troop[0].command = "buildtownhall"
        
    def buildhouseCommand(self, posX, posY):
        self.troop[0].destination = [posX, posY]
        self.troop[0].command = "buildhouse"
        
    def buildbarrackCommand(self, posX, posY):
        self.troop[0].destination = [posX, posY]
        self.troop[0].command = "buildbarrack"
        
    def phalanxCommand(self):
        for troop in self.troops:
            troop.command = "phalanx"
    
    def unphalanxCommand(self):
        for troop in self.troops:
            troop.command = "unphalanx"
            
    def cancel(self):
        self.state = "normal"
        
    # process trigger
    def processTrigger(self, callback, mousebutton, mouseDownX, mouseDownY, mouseUpX, mouseUpY):
        # mousebutton: 1-leftclick, 2-middleclick, 3-rightclick, 4-scrollup, 5-scrolldown
        func = callback[0]
        if mousebutton == 1:
            if func == "clickActorInterface":
                self.moveCameraToActor(callback[1]) # actor class
            elif func == "clickMultiInterface":
                self.selectActor(callback[1])
            elif func == "move":
                self.move()
            elif func == "attack":
                self.attack()
            elif func == "patrol":
                self.patrol()
            elif func == "gather":
                self.gather()
            elif func == "build":
                self.build()
            elif func == "buildtownhall":
                self.buildtownhall()
            elif func == "buildhouse":
                self.buildhouse()
            elif func == "buildbarrack":
                self.buildbarrack()
            elif func == "moveCommand":
                self.moveCommand(mouseDownX, mouseDownY)
            elif func == "attackCommand":
                self.attackCommand(mouseDownX, mouseDownY)
            elif func == "patrolCommand":
                self.patrolCommand(mouseDownX, mouseDownY)
            elif func == "stopCommand":
                self.stopCommand()
            elif func == "holdCommand":
                self.holdCommand()
            elif func == "gatherCommand":
                self.gatherCommand(mouseDownX, mouseDownY)
            elif func == "buildtownhallCommand":
                self.buildtownhallCommand(mouseDownX, mouseDownY)
            elif func == "buildhouseCommand":
                self.buildhouseCommand(mouseDownX, mouseDownY)
            elif func == "buildbarrackCommand":
                self.buildbarrackCommand(mouseDownX, mouseDownY)
            elif func == "phalanxCommand":
                self.phalanxCommand()
            elif func == "unphalanxCommand":
                self.unphalanxCommand()
        elif mousebutton == 2:
            pass
        elif mousebutton == 3:
            if func == "clickActorInterface":
                self.movetargetCommand(callback[1])
            elif func == "clickMultiInterface":
                self.movetargetCommand(callback[1])
            elif func == "move":
                pass
            elif func == "attack":
                pass
            elif func == "patrol":
                pass
            elif func == "gather":
                pass
            elif func == "build":
                pass
            elif func == "buildtownhall":
                pass
            elif func == "buildhouse":
                pass
            elif func == "buildbarrack":
                pass
            elif func == "moveCommand":
                self.cancel()
            elif func == "attackCommand":
                self.cancel()
            elif func == "patrolCommand":
                self.cancel()
            elif func == "stopCommand":
                pass
            elif func == "holdCommand":
                pass
            elif func == "gatherCommand":
                self.cancel()
            elif func == "buildtownhallCommand":
                self.cancel()
            elif func == "buildthouseCommand":
                self.cancel()
            elif func == "buildbarrackCommand":
                self.cancel()
            elif func == "phalanxCommand":
                pass
            elif func == "unphalanxCommand":
                pass
        elif mousebutton == 4:
            pass
        elif mousebutton == 5:
            pass
        
    # render and processinput
    def tick():
        DISPLAYSURF.fill(gray)
        # draw map
        for actor in world.actors:
            positionX = unit.position[0] - cameraX
            positionY = unit.position[1] - cameraY
            
            img = pygame.image.load(actor.image)
            img = pygame.transform.scale(img, (actor.size, actor.size))
            DISPLAYSURF.blit(img, (positionX, positionY))
            
        pygame.draw.rect(DISPLAYSURF, gray, (0,600,1200,300))
        pygame.draw.line(DISPLAYSURF, black, (0,600), (1200,600), 5)
        pygame.draw.line(DISPLAYSURF, black, (300,600), (300,900), 5)
        pygame.draw.line(DISPLAYSURF, black, (900,600), (900,900), 5)
        
        # draw minimap
        for actor in world.actors:
            positionX = unit.position[0] * 300 / world.size[0]
            positionY = unit.position[1] * 300 / world.size[1] + 600
            pygame.draw.rect(DISPLAYSURF, green, positionX, positionY, unit.size/32, unit.size/32)
            
        # draw interface & make trigger
        if len(self.troops) == 1:
            pygame.draw.line(DISPLAYSURF, black, (450,600), (450,750), 3)
            pygame.draw.line(DISPLAYSURF, black, (300,750), (450,750), 3)
            self.mouseTriggers.append([300,600,150,150,["clickActorInterface", self.troops[0]]])
            # draw image
        elif len(self.troops) >= 2:
            pygame.draw.line(DISPLAYSURF, black, (375,600), (375,900))
            pygame.draw.line(DISPLAYSURF, black, (450,600), (450,900))
            pygame.draw.line(DISPLAYSURF, black, (525,600), (525,900))
            pygame.draw.line(DISPLAYSURF, black, (600,600), (600,900))
            pygame.draw.line(DISPLAYSURF, black, (675,600), (675,900))
            pygame.draw.line(DISPLAYSURF, black, (750,600), (750,900))
            pygame.draw.line(DISPLAYSURF, black, (825,600), (825,900))
            pygame.draw.line(DISPLAYSURF, black, (300,700), (900,700))
            pygame.draw.line(DISPLAYSURF, black, (300,800), (900,800))
            
            for i in range(len(self.troops)):
                x = i % 8
                y = int(i / 8)
                troop = self.troops[i]
                img = pygame.image.load(troop.image)
                img = pygame.transform.scale(img, (69,90))
                DISPLAYSURF.blit(img, (303+x*75, 605+y*100))
                self.mouseTriggers.append([300+x*75, 600+y*100, 75,100, ["clickMultiInterface", self.troops[i]]])
        # draw command & make trigger
        
def distance(positionX, positionY):
    return math.sqrt((positionX[0]-positionY[0])**2 + (positionX[1] - positionY[1])**2)
        
class Cactor:
    pass

class Cunit(Cactor):
    pass

class Cworker(Cunit):
    pass

class Cwarrior(Cunit):
    pass

class Carcher(Cunit):
    pass

class Cknight(Cunit):
    pass

class Cstructure(Cactor):
    pass

class Ctownhall(Cstructure):
    pass

class Chouse(Cstructure):
    pass

class Cbarrack(Cstructure):
    pass

            
