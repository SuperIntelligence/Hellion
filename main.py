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
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
pygame.display.set_caption('Pathfinder')
DISPLAYSURF.fill(gray)

# class
class Cunit:
    image = ""
    portrait = ""
    troopsicon= ""
    position = [0.0, 0.0]
    size = [0,0]
    possession = 0
    
    hp = [0,0]
    sp = [0,0]
    attack = 0
    armor = 0
    speed = 0
    reach = 0
    
    # command: 0-idle, 1-moveground, 2-movetarget, 3-stop, 4-attackground, 5-attacktarget
    # command: 6-patrolground, 7-patroltarget, 8-hold, 9-gather, 10-buildtownhall
    # command: 11-buildhouse, 12-buildbarrack, 13-palanx, 14-unpalanx
    
    currentcommand = 0 # idle
    target = 0
    source = [0.0, 0.0]
    destination = [0.0, 0.0]
    
    #function
    def idle(self):
        pass
    def moveground(self, destination):
        pass
    def movetarget(self, target):
        pass
    def stop(self):
        pass
    def attackground(self, destination):
        pass
    def attacktarget(self, destination):
        pass
    def patrolground(self, source, destination):
        pass
    def patroltarget(self, source, target):
        pass
    def hold(self):
        pass
    
    def action(self):
        if currentcommand = 0:
            self.idle()
        elif currentcommand == 1:
            self.moveground(self.destination)
        elif currentcommand == 2:
            self.movetarget(self.target)
        elif currentcommand == 3:
            self.stop()
        elif currentcommand == 4:
            self.attackground(self.destination)
        elif currentcommand == 5:
            self.attacktarget(self.target)
        elif currentcommand == 6:
            self.patrolground(self.destination)
        elif currentcommand == 7:
            self.patroltarget(self.target)
        elif currentcommand == 8:
            self.hold()

            
class Cworker(Cunit):
    resource = 0
    
    def __init__(self, position, destination):
        self.image = "image/worker.png"
        self.position = position
        self.size = [32,32]
        self.possession = 1
        
        self.hp = [100,100]
        self.sp = [100,100]
        self.attack = 5
        self.armor = 0
        self.speed = 5
        self.reach = 100
        
        # command setting
        if(position[0] == destination[0] and position[1] == destination[1]):
            currentcommand = 0 # idle
        else:
            currentcomand = 1 # moveground
        
        self.target = 0
        self.source = [0.0, 0.0]
        self.destination = destination
        
    def gather(self, target):
        pass
    def buildtownhall(self, destination):
        pass
    def buildhouse(self, destination):
        pass
    def buildbarrack(self, destination):
        pass
    
    def action(self):
        if currentcommand = 0:
            self.idle()
        elif currentcommand == 1:
            self.moveground(self.destination)
        elif currentcommand == 2:
            self.movetarget(self.target)
        elif currentcommand == 3:
            self.stop()
        elif currentcommand == 4:
            self.attackground(self.destination)
        elif currentcommand == 5:
            self.attacktarget(self.target)
        elif currentcommand == 6:
            self.patrolground(self.destination)
        elif currentcommand == 7:
            self.patroltarget(self.target)
        elif currentcommand == 8:
            self.hold()
        elif currentcommand == 9:
            self.gather(self.target)
        elif currentcommand == 10:
            self.buildtownhall(self.destination)
        elif currentcommand == 11:
            self.buildhouse(self.destination)
        elif currentcommand == 12:
            self.buildbarrack(self.destination)
            
    
