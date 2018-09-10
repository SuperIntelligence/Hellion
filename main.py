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

class Cworker(Cunit):
    ispalanx = False
    
    def __init__(self, position, destination):
        self.image = "image/warrior.png"
        self.position = position
        self.size = [32,32]
        self.possession = 1
        
        self.hp = [200,200]
        self.sp = [100,100]
        self.attack = 15
        self.armor = 2
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
        
    def palanx(self):
        self.speed = 2
        self.armor = 5
        self.ispalanx = True
    def unpalanx(self):
        self.speed = 5
        self.armor = 2
        self.ispalanx = False
    
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
        elif currentcommand == 13:
            self.palanx()
        elif currentcommand == 14:
            self.unpalanx()
 

class Cworld:
    units = []
    structures = []
    size = [0,0]

class Cplayerstate:
    #camera
    cameraposition = [0.0, 0.0]
    camerawidth = 1200
    cameraheight = 600
    
    # command state
    commandstate = 0
    # 0 -> normal
    # 1 -> select target
    # 2 -> select building
    
    # troops
    controlstate = 0 # 0-units, 1-structure
    controlunits = []
    controlstructure = []
    
# structure
class Ctownhall(Cstructure):
    supply = 10
    
    rallypoint = [0.0, 0.0]
    trainqueue = []
    trainingtime = [0, 1200]
    trainprogress = 0
    
    command = 0
    
    # function
    def __init__(self, position):
        self.image = "/image/townhall.png"
        self.portrait = ""
        self.position = position
        self.rallypoint = position
        self.size = [160, 160] # 5*5
        
    def train(self):
        self.trainprogress += 1
        if self.trainprogress >= self.trainingtime[trainqueue[0]]:
            # make unit, pop queue, initial trainprogress
            if trainqueue[0] == 1:
                worker = Cworker(self.position, self.rallypoint)
                world.unit.append(copy.deepcopy(worker)) # make unit
                self.trainqueue = self.trainqueue[1:]
                self.trainprogress = 0
            
    def setrallypoint(self, destination):
        self.rallypoint = destination
    def action(self):
        if command == 0:
            pass
        elif command == 1:
            train()
            
class Chouse(Cstructure):
    supply = 8
    def __init__(self, position):
        self.image = "/image/house.png"
        self.portrait = ""
        self.position = position
        self.size = [64,64]
        
class Cbarrack(Cstructure):
    supply = 0
    
    rallypoint = [0.0, 0.0]
    trainqueue = [] # 1-warrior
    trainingtime = [0, 1800]
    trainprogress = 0
    
    command = 0
    
    # function
    def __init__(self, position):
        self.image = "/image/barrack.png"
        self.portrait = ""
        self.position = position
        self.rallypoint = position
        self.size = [96, 96] # 3*3
        
    def train(self):
        self.trainprogress += 1
        if self.trainprogress >= self.trainingtime[trainqueue[0]]:
            # make unit, pop queue, initial trainprogress
            if trainqueue[0] == 1:
                warrior = Cwarrior(self.position, self.rallypoint)
                world.unit.append(copy.deepcopy(warrior)) # make unit
                self.trainqueue = self.trainqueue[1:]
                self.trainprogress = 0
            
    def setrallypoint(self, destination):
        self.rallypoint = destination
    def action(self):
        if command == 0:
            pass
        elif command == 1:
            train()
            
# global variable
world = Cworld()
playerstate = Cplayerstate()

def drawbasic():
    global world, playerstate
    
    DISPLAYSURF.fill(gray)
    pygame.draw.line(DISPLAYSURF, black, (0,600), (1200,900), 5)
    pygame.draw.line(DISPLAYSURF, black, (300,600), (300,900), 5)
    pygame.draw.line(DISPLAYSURF, black, (900,600), (900,900), 5)
    
    if playerstate.controlstate == 0:
