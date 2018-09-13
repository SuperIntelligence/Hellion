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
    name = ""
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
    targetunit  = -1 # target unit number
    targetstructure = -1 # target structrue number
    targetstate = 0 # 0-unit, 1-structure
    
    source = [0.0, 0.0]
    destination = [0.0, 0.0]
    
    ismoveable = True
    isstopable = True
    isattackable = True
    ispatrolable = True
    isholdable = True
    isgatherable = False
    ifbuildable = False
    ispalanxable = False
    isunpalanxable = False
    
    isbuildtownhallable = False
    isbuildhouseable = False
    ifbuildbarrackable = False
    
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
    
    def __init__(self, position, destination): #destination is just for rally point
        self.name = "worker"
        self.image = "image/worker.png"
        self.position = position
        self.size = [32,32]
        self.possession = 1 # local player. need to be modify when extended
        
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
        
        self.targetunit = -1
        self.targetstructure = -1
        self.targetstate = 0 # 0-unit, 1-structure
        self.source = [0.0, 0.0]
        self.destination = destination
        
        self.isgatherable = True
        self.isbuildable = True
        
        self.isbuildtownhallable = True
        self.isbuildhouseable = True
        self.isbuildbarrackable = True
        
    def gather(self,target):
        pass
    
    def buildtownhall(self, destination):
        pass
    
    def buildhouse(self, destination):
        pass
    
    def buildbarrack(self, destination):
        pass
    
    # command: 0-idle, 1-moveground, 2-movetarget, 3-stop, 4-attackground, 5-attacktarget
    # command: 6-patrolground, 7-patroltarget, 8-hold, 9-gather, 10-buildtownhall
    # command: 11-buildhouse, 12-buildbarrack, 13-palanx, 14-unpalanx
    
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

class Cwarrior(Cunit):
    ispalanx = False
    
    def __init__(self, position, destination):
        self.name = "warrior"
        self.image = "image/warrior.png"
        self.position = position
        self.size = [32,32]
        self.possession = 1 # local player, need to be modify when extended
        
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
            currentcommand = 1 # moveground
        
        self.targetunit = -1
        self.targetstructure = -1
        self.targetstate = 0 # 0-unit, 1-structure
        self.source =[0.0, 0.0]
        self.destination = destination
        
        self.ispalanxable = True
        self.isunpalanxable = True
        
    def palanx(self):
        self.speed = 2
        self.armor = 5
        self.ispalanx = True
    
    def unpalanx(self):
        self.speed = 5
        self.armor = 2
        self.ispalanx = False
        
    def action(self):
        if currentcommand == 0:
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
    size = [9600,9600]

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
    
    currentcommand = 0 # used to order to units or structrues
    # if player press 'A' key, then commandstate -> 1,
    # and currentcommand -> 2.
    # 0-idle, 1-move, 2-stop, 3-attack, 4-patrol, 5-hold, 6-gather
    # 7-buildtownhall, 8-buildhouse, 9-buildbarrack
    # 10-palanx, 11-unpalanx
    
    # troops
    controlstate = 0 # 0-units, 1-structure
    controlunits = []
    controlstructure = []
    
    # mouse
    mousedownpos = [0,0]
    ismousedown = False
    
# structure
class Cstructure:
    image = ""
    portrait = ""
    position = [0.0, 0.0]
    size = [0.0] # pixel
    possession = 0
    
    hp = [0,0]
    armor = 0
    
    def action(self):
        pass

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
        if len(playerstate.controlunits) == 0:
            pass
        elif len(playerstate.controlunits) == 1:
            pygame.draw.line(DISPLAYSURF, black, (450,600), (450,750), 3)
            pygame.draw.line(DISPLAYSURF, black, (300,750), (450,750), 3)
        elif len(playerstate.controlunits) >= 2:
            pygame.draw.line(DISPLAYSURF, black, (375,600), (375,900))
            pygame.draw.line(DISPLAYSURF, black, (450,600), (450,900))
            pygame.draw.line(DISPLAYSURF, black, (525,600), (525,900))
            pygame.draw.line(DISPLAYSURF, black, (600,600), (600,900))
            pygame.draw.line(DISPLAYSURF, black, (675,600), (675,900))
            pygame.draw.line(DISPLAYSURF, black, (750,600), (750,900))
            pygame.draw.line(DISPLAYSURF, black, (825,600), (825,900))
            
            pygame.draw.line(DISPLAYSURF, black, (300,700), (900,700))
            pygame.draw.line(DISPLAYSURF, black, (300,800), (900,800))
    elif playerstate.controlstate == 1:
        if len(playerstate.controlstructure) == 0:
            pass
        elif len(playerstate.controlstructure) == 1:
            pygame.draw.line(DISPLAYSURF, black, (450,600), (450,750), 3)
            pygame.draw.line(DISPLAYSURF, black, (300,750), (450,750), 3)
        elif len(playerstate.controlstructure) >= 2:
            pygame.draw.line(DISPLAYSURF, black, (375,600), (375,900))
            pygame.draw.line(DISPLAYSURF, black, (450,600), (450,900))
            pygame.draw.line(DISPLAYSURF, black, (525,600), (525,900))
            pygame.draw.line(DISPLAYSURF, black, (600,600), (600,900))
            pygame.draw.line(DISPLAYSURF, black, (675,600), (675,900))
            pygame.draw.line(DISPLAYSURF, black, (750,600), (750,900))
            pygame.draw.line(DISPLAYSURF, black, (825,600), (825,900))
            
            pygame.draw.line(DISPLAYSURF, black, (300,700), (900,700))
            pygame.draw.line(DISPLAYSURF, black, (300,800), (900,800))
  

def drawmap():
    global world, playerstate
    # use playerstate->camera, world
    cameraX = playerstate.cameraposition[0]
    cameraY = playerstate.cameraposition[1]
    
    for unit in world.units:
        positionX = unit.position[0] - cameraX
        positionY = unit.position[1] - cameraY
        
        sizeX = unit.size[0]
        sizeY = unit.size[1]
        img = pygame.image.load(unit.image)
        img = pygame.transform.scale(img, (sizeX, sizeY))
        DISPLAYSURF.blit(img, (positionX, positionY))
        
    for structrue in world.structures:
        positionX = structure.position[0] - cameraX
        positionY = structrue.position[1] - cameraY
        
        sizeX = structure.size[0]
        sizeY = structure.size[1]
        img = pygame.image.load(structure.image)
        img = pygame.transform.scale(img, (sizeX, sizeY))
        DISPLAYSURF.blit(img, (positionX, positionY))

def drawminimap():
    global world, playerstate
    # draw units and structure, and camera positon
    for unit in world.units:
        positionX = unit.position[0] * 300 / world.size[0]
        positionY = unit.position[1] * 300 / world.size[1] + 600
        
        sizeX = 3
        sizeY = 3
        pygame.draw.rect(DISPLAYSURF, green, (positionX, positionY, sizeX, sizeY))
    
    for structurein world.structures:
        positionX = structure.position[0] * 300 / world.size[0]
        positionY = structure.position[1] * 300 / world.size[1] + 600
        
        sizeX = 6
        sizeY = 6
        pygame.draw.rect(DISPLAYSURF, green, (positionX, positionY, sizeX, sizeY))

# testing. need to delete.
playerstate.controlunits.append(0)
playerstate.controlunits.append(1)
playerstate.controlunits.append(2)
playerstate.controlunits.append(3)
playerstate.controlunits.append(4)
playerstate.controlunits.append(5)
# testing. need to delete.
   
def drawinterface():
    global world, playerstate
    
    if playerstate.controlstate == 0:
        if len(playerstate.controlunits) == 0:
            pass
        elif len(playerstate.controlunits) == 1:
            # draw image
            unit = world.units[playerstate.controlunits[0]]
            
            img = pygame.image.load(unit.image)
            img = pygame.transform.scale(img, (140,140))
            DISPLAYSURF.blit(img, (305,605))
            # draw text
            # hp, sp, attack, armor
            hp = 'hp: ' + str(unit.hp[0]) + ' / ' + str(unit.hp[1])
            text = BASICFONT.render(hp, True, black)
            DISPLAYSURF.blit(text, (520, 620))
            
            sp = 'sp: ' + str(unit.sp[0]) + ' / ' + str(unit.sp[1])
            text = BASICFONT.render(sp, True, black)
            DISPLAYSURF.blit(text, (520, 650))
            
            attack = 'attack: ' + str(unit.attack)
            text = BASICFONT.render(attack, True, black)
            DISPLAYSURF.blit(text, (520, 680))
            
            armor = 'armor: ' + str(unit.armor)
            text = BASICFONT.render(armor, True, black)
            DISPLAYSURF.blit(text, (520, 710))
            
        elif len(playerstate.controlunits) >= 2:
            # draw character image. maximum 24.
            length = len(playerstate.controlunits)
            
            for i in range(length):
                x = i % 8
                y = i / 8
                unit = world.units[playerstate.controlunits[i]]
                img = pygame.image.load(unit.image)
                img = pygame.transform.scale(img, (69, 90)) # 75,100 - care about margin
                DISPLAYSURF.blit(img, (303 + x * 75, 605 + y * 100))
                # need to extend, when display unit state(especially hp state
    
    elif playerstate.controlstate == 1: # structure
        if len(playerstate.controlstructure) == 0:
            pass
        elif len(playerstate.controlstructure) == 1:
            # draw image
            structure = world.structures[playerstate.controlstructrues[0]]
            
            img = pygame.image.load(structure.image)
            img = pygame.transform.scale(img, (150,150))
            DISPLAYSURF.blit(img, (300,600))
            # draw text
            # hp, sp, attack, armor
            hp = 'hp: ' + str(structure.hp[0]) + ' / ' + str(structure.hp[1])
            text = BASICFONT.render(armor, True, black)
            DISPLAYSURF.blit(text,(520,710))
            
        elif len(playerstate.controlstructures) >= 2:
            # draw character image. maximum 24.
            length = len(playerstate.controlstructures)
            for i in range(length):
                x = i % 8
                y = i / 8
                structure = world.structures[playerstate.controlstructures[i]]
                img = pygame.image.load(unit.image)
                img = pygame.transform.scale(img, (69,90)) # 75,100 - care abour margin
                DISPLAYSURF.blit(img,(303 + x * 75, 605 + y * 100))
                # need to extend, when display unit state(especially hp state)

def drawcommand():
    pass

def render():
    drawbasic()
    drawmap()
    drawminimap()
    drawinterface()
    drawcommand()
    
    pygame.display.update()
    
def processinput():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
def modifygamestate():
    #final
    FPSCLOCK.tick(FPS)
    
    
def beginplay():
    global world, playerstate
    world.size = [12800,12800]
    # spawn
    townhall = Ctownhall([640,640])
    world.structures.append(copy.deepcopy(townhall))
    
    worker = Cworker([640,800], [640,800])
    world.units.append(copy.deepcopy(worker))
    
    worker = Cworker([672,800], [672,800])
    world.units.append(copy.deepcopy(worker))
    
    worker = Cworker([704,800], [704,800])
    world.units.append(copy.deepcopy(worker))
    
    worker = Cworker([736,800], [736,800])
    world.units.append(copy.deepcopy(worker))
    
    worker = Cworker([778,800], [778,800])
    world.units.append(copy.deepcopy(worker))
    
beginplay()

while True:
    render()
    processinput()
    modifygamestate()
