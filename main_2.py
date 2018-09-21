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
        if self.state == "normal":
            # make trigger in map
            mouseTrigger.append([0,0,1200,600,["clickMap"]])
            
            if len(self.troops) >= 1:
                ismoveable = True
                isstopable = True
                isattackable = True
                ispatrolable = True
                isholdable = True
                
                isgatherable = True
                isbuildable = True
                isphalanxable = True
                isunphalanxable = True
                
            for troop in self.troops:
                if self.ismoveable == False:
                    ismoveable = False
                if self.isstopable == False:
                    isstopable = False
                if self.isattackable == False:
                    isattackable = False
                if self.ispatrolable == False:
                    ispatrolable = False
                if self.isholdable == False:
                    isholdable = False
                if self.isgatherable == False:
                    isgatherable = False
                if self.isbuildable == False:
                    isbuildable = False
                if self.isphalanxable == False:
                    isphalanxable = False
                if self.isunphalanxable == False:
                    isunphalanxable = False
                
            if ismoveable == True:
                img = pygame.image.load("image/move.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(902,602))
                mouseTriggers.append([900,600,60,60,["move"]])
                keyboardTriggers.append(K_m, ["move"])
            if isstopable == True:
                img = pygame.image.load("image/stop.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(962,602))
                mouseTriggers.append([960,600,60,60,["stop"]])
                keyboardTriggers.append(K_s, ["stop"])
            if isattackable == True:
                img = pygame.image.load("image/attack.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(1022,602))
                mouseTriggers.append([1020,600,60,60,["attack"]])
                keyboardTriggers.append(K_a, ["attack"])
            if ispatrolable == True:
                img = pygame.image.load("image/patrol.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(1082,602))
                mouseTriggers.append([1080,600,60,60,["patrol"]])
                keyboardTriggers.append(K_p, ["patrol"])
            if isholdable == True:
                img = pygame.image.load("image/hold.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(1142,602))
                mouseTriggers.append([1140,600,60,60,["hold"]])
                keyboardTriggers.append(K_h, ["hold"])
            if isgatherable == True:
                img = pygame.image.load("image/gather.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(902,662))
                mouseTriggers.append([900,660,60,60,["gather"]])
                keyboardTriggers.append(K_g, ["gather"])
            if isbuildable == True:
                img = pygame.image.load("image/build.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(902,782))
                mouseTriggers.append([900,780,60,60,["build"]])
                keyboardTriggers.append(K_b, ["build"])
            if isphalanxable == True:
                img = pygame.image.load("image/phalanx.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(902,842))
                mouseTriggers.append([900,840,60,60,["phalanx"]])
                keyboardTriggers.append(K_z, ["phalanx"])
            if ismoveable == True:
                img = pygame.image.load("image/unphalanx.png")
                img = pygame.transform.scale(img,(56,56))
                DISPLAYSURF.blit(img,(962,842))
                mouseTriggers.append([960,840,60,60,["unphalanx"]])
                keyboardTriggers.append(K_x, ["unphalanx"])
            
        elif self.state == "move":
            # we also make trigger.
            text = BASICFONT.render('LMB: Select Target', True, black)
            DISPLAYSURF.blit(text, (920, 700))
            text = BASICFONT.render('RMB: Cancel', True, black)
            DISPLAYSURF.blit(text, (920, 750))
            
        elif self.state == "attack":
            # we also make trigger.
            text = BASICFONT.render('LMB: Select Target', True, black)
            DISPLAYSURF.blit(text, (920, 700))
            text = BASICFONT.render('RMB: Cancel', True, black)
            DISPLAYSURF.blit(text, (920, 750))
            
        elif self.state == "patrol":
            # we also make trigger.
            text = BASICFONT.render('LMB: Select Target', True, black)
            DISPLAYSURF.blit(text, (920, 700))
            text = BASICFONT.render('RMB: Cancel', True, black)
            DISPLAYSURF.blit(text, (920, 750))
            
        elif self.state == "gather":
            # we also make trigger.
            text = BASICFONT.render('LMB: Select Target', True, black)
            DISPLAYSURF.blit(text, (920, 700))
            text = BASICFONT.render('RMB: Cancel', True, black)
            DISPLAYSURF.blit(text, (920, 750))
            
        elif self.state == "buildtownhall":
            # we also make trigger.
            text = BASICFONT.render('LMB: Select Target', True, black)
            DISPLAYSURF.blit(text, (920, 700))
            text = BASICFONT.render('RMB: Cancel', True, black)
            DISPLAYSURF.blit(text, (920, 750))
            
        elif self.state == "buildhouse":
            # we also make trigger.
            text = BASICFONT.render('LMB: Select Target', True, black)
            DISPLAYSURF.blit(text, (920, 700))
            text = BASICFONT.render('RMB: Cancel', True, black)
            DISPLAYSURF.blit(text, (920, 750))
            
        elif self.state == "buildbarrack":
            # we also make trigger.
            text = BASICFONT.render('LMB: Select Target', True, black)
            DISPLAYSURF.blit(text, (920, 700))
            text = BASICFONT.render('RMB: Cancel', True, black)
            DISPLAYSURF.blit(text, (920, 750))
            
        elif self.state == "selectbuilding":
            img = pygame.image.load("image/buildtownhall.png")
            img = pygame.transform.scale(img, (56,56))
            DISPLAYSURF.blit(img, (902,602))
            mouseTriggers.append([900,600,60,60,["buildtownhall"]])
            keyboardTriggers.append(K_t, ["buildtownhall"])
            
            img = pygame.image.load("image/buildhouse.png")
            img = pygame.transform.scale(img, (56,56))
            DISPLAYSURF.blit(img, (962,602))
            mouseTriggers.append([960,600,60,60,["buildhouse"]])
            keyboardTriggers.append(K_s, ["buildhouse"])
            
            img = pygame.image.load("image/buildbarrack.png")
            img = pygame.transform.scale(img, (56,56))
            DISPLAYSURF.blit(img, (1022,602))
            mouseTriggers.append([1020,600,60,60,["buildbarrack"]])
            keyboardTriggers.append(K_b, ["buildbarrack"])
            
        # process input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.mouseDownX, self.mouseDownY = event.pos
            elif event.type == MOUSEBUTTONUP:
                self.mouseUpX, self.mouseUpY = event.pos
                
                for mouseTrigger in self.mouseTriggers:
                    if mouseTrigger[0] < self.mouseUpX and mouseTrigger[0] + mouseTrigger[2] > self.mouseUpX and mouseTrigger[1] < self.mouseUpY and moueTrigger[1] + mouseTrigger[3] > self.mouseUpY and mouseTrigger[0] < self.mouseDownX and mouseTrigger[0] + mouseTrigger[2] > self.mouseDownX and mouseTrigger[1] < self.mouseDownY and mouseTrigger[1] + mouseTrigger[3] > self.mouseDownY:
                        self.processTrigger(mouseTrigger[4], event.button, self.mouseDownX, self.mouseDownY, self.mouseUpX, self.mouseUpY)
                        

class Cactor:
    name = "" # worker, warrior, archer, townhall, house, barrack, food
    domain = "" # unit, structure, item, resource
    
    image = ""
    portrait = ""
    troopsicon = ""
    
    position = [0.0, 0.0]
    size = 0
    possession = 0 # player numbetr. 0 = neutral
    
    destination = [0.0, 0.0]
    target = 0
    source = [0.0, 0.0]
    patrolstate = 0 # 0-move to destination, 1-move to source
    
    size = 0
    
    hp = [0,0]
    sp = [0,0]
    damage = 0
    attackdelay = 0.f
    attackcool = 0.f # if attackcool >= attackdelay, actor can attack
    armor = 0
    reach = 0
    sight = 0
    agro = 0
    speed = 0.0
    
    food = 0 # for gathering
    maxfood = 0
    
    # command
    # idle, moveground, movetarget, stop, attackground, attacktarget, patrolground, patroltarget, hold
    # gather, buildtownhall, buildhouse, buildbarrack, phalanx, unphalanx
    # processworker, processwarrior, processarcher, processknight, rallypoint
    command = "idle
    
    # if domain == "unit"
    ismoveable = False
    isstopable = False
    isattackable = False
    ispatrolable = False
    isholdable = False
    
    isgatherable = False
    isbuildable = False
    
    isphalanxable = False
    isunphalanxable = False
    
    # if domain == "structure"
    isprocessworkerable = False
    isprocesswarriorable = False
    isprocessarcherable = False
    isprocessknightable = False
    israllypointable = False
    
    def distance(positionX, positionY):
        return math.sqrt((positionX[0]-positionY[0])**2 + (positionX[1]-positionY[1])**2)
    
    def idle():
        if self.domain == "unit":
            for actor in world.actors:
                if actor.possess != self.possess and distance(actor.position, self.position) <= self.reach:
                    if self.attackcool >= self.attackdelay:
                        if self.damage > actor.armor + 1:
                            actor.hp[0] -= self.damage - actor.armor
                        else:
                            actor.hp[0] -= 1
                    elif actor.possess != self.possess and distance(actor.position, self.position) <= self.agro:
                        deltaX = actor.position[0] - self.position[0]
                        deltaY = actor.position[1] - self.position[1]
                        hop = self.speed / FPS
                        
                        moveX = (deltaX**2 / (deltaX**2 + deltaY**2)) * hop
                        moveY = (deltaY**2 / (deltaX**2 + deltaY**2)) * hop
                        if deltaX > moveX:
                            self.position[0] += moveX
                            self.position[1] += moveY
                        else:
                            self.position[0] += deltaX
                            self.position[1] += deltaY
                        break
            elif self.domain == "structure":
                pass
    
    def moveground():
        pass
    
    def movetarget():
        pass
    
    def stop():
        pass
    
    def attackground():
        pass
    
    def attacktarget():
        pass
    
    def patrolground():
        pass
    
    def patroltarget():
        pass
    
    def hold():
        pass
    
    def gather():
        pass
    
    def buildtownhall():
        pass
    
    def buildhouse():
        pass
    
    def buildbarrack():
        pass
    
    def phalanx():
        pass
    
    def unphalanx():
        pass
    
    def processworker():
        pass
    
    def processwarrior():
        pass
    
    def processarcher():
        pass
    
    def processknight():
        pass
    
    def action():
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

            
