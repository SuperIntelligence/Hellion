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
    def processTrigger(self, callback, mousebutton):
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
                self.moveCommand(callback[1], callback[2])
            elif func == "attackCommand":
                self.attackCommand(callback[1], callback[2])
            elif func == "patrolCommand":
                self.patrolCommand(callback[1], callback[2])
            elif func == "stopCommand":
                self.stopCommand()
            elif func == "holdCommand":
                self.holdCommand()
            elif func == "gatherCommand":
                self.gatherCommand(callback[1], callback[2])
            elif func == "buildtownhallCommand":
                self.buildtownhallCommand(callback[1], callback[2])
            elif func == "buildhouseCommand":
                self.buildhouseCommand(callback[1], callback[2])
            elif func == "buildbarrackCommand":
                self.buildbarrackCommand(callback[1], callback[2])
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
            
            
