import pygame
import math
pygame.init()

def init(surface, arrayListeners, event):
    systemObject.screenSurface = surface
    systemObject.objectListeners = arrayListeners
    systemObject.gConst = 6.674 * 10 ** -11
    systemObject.eventClicked = event

def updateScreen(screenConv, screenOffX, screenOffY):
    systemObject.screenConversion = screenConv
    systemObject.screenOffsetX = screenOffX
    systemObject.screenOffsetY = screenOffY

class systemObject():
    def __init__(self, data):
        self.objectListeners.append(self)
        self.data = data
        self.objectID = data[0]
        self.solarSystemID = data[1]
        self.parentID = data[2]
        self.solarSystemObjectID = data[3]
        self.name = data[4]
        self.x_pos = data[5]
        self.y_pos = data[6]
        self.x_vel = data[7]
        self.y_vel = data[8]
        self.x_acc = 0
        self.y_acc = 0
        self.mass = data[9]
        self.red = data[10]
        self.green = data[11]
        self.blue = data[12]
        self.colour = (self.red, self.green, self.blue)
        self.radius = 10
        self.convertCoords()
        self.event = self.detectClick

    def init(self):
        for i in self.objectListeners:
            if i.solarSystemObjectID == self.parentID:
                self.parent = i
        if self.parent.solarSystemObjectID == 0:
            if self.solarSystemObjectID == 0:
                self.radius = 10
            else:
                self.radius = 10
        else:
            self.radius = 10
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.colour, (int(self.radius), int(self.radius)), self.radius)

    def getData(self):
        self.data = [self.objectID, self.solarSystemID, self.parentID,
                     self.solarSystemObjectID, self.name, self.x_pos,
                     self.y_pos, self.x_vel, self.y_vel, self.mass,
                     self.red, self.green, self.blue]
        return self.data

    def convertCoords(self):
        self.screen_x = (self.x_pos + self.screenOffsetX) / self.screenConversion
        self.screen_y = (self.y_pos + self.screenOffsetY) / self.screenConversion

    def draw(self):
        self.rect.center = (self.screen_x, self.screen_y)
        self.screenSurface.blit(self.image, self.rect)

    def setColour(self, r, g, b):
        #update colour variables
        self.red = r
        self.green = g
        self.blue = b
        self.colour = (self.red, self.green, self.blue)
        #redraw surface
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, self.colour, (int(self.radius), int(self.radius)), self.radius)

    #updating the object
    def tick(self, timeSinceLastTick):
        if self.solarSystemObjectID != 0: #if the object in question is not the sun
            #get distance to parent
            distance = math.sqrt((self.x_pos - self.parent.x_pos) ** 2 + (self.y_pos - self.parent.y_pos) ** 2)
            #calculate acceleration 
            self.x_acc = self.gConst * self.parent.mass * (self.parent.x_pos - self.x_pos) / distance ** 3
            self.y_acc = self.gConst * self.parent.mass * (self.parent.y_pos - self.y_pos) / distance ** 3
            self.x_acc += self.parent.x_acc
            self.y_acc += self.parent.y_acc
            #calcaulte new velocities
            self.x_vel = self.x_vel + self.x_acc * timeSinceLastTick / 1000
            self.y_vel = self.y_vel + self.y_acc * timeSinceLastTick / 1000
            #calculate new positions
            self.x_pos = self.x_pos + self.x_vel * timeSinceLastTick / 1000
            self.y_pos = self.y_pos + self.y_vel * timeSinceLastTick / 1000
            #convert position to screen coordinates
        #if it is the sun, no update needs to occur, as the sun remains in the centre
        else:
            self.parent = self
        self.convertCoords()
        
    def debug(self):
        print("MY ID:", self.solarSystemObjectID)
        print("-----")
        print("X ACCELERATION:", self.x_acc, "m/s^2 x")
        print("Y ACCELERATION:", self.y_acc, "m/s^2 y")
        print("-----")
        print("X VELOCITY:", round(self.x_vel), "m/s x")
        print("Y VELOCITY:", round(self.y_vel), "m/s y")
        print("-----")
        print("X POSITION:", round(self.x_pos), "m x")
        print("Y POSITION:", round(self.y_pos), "m y")

    def detectClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.eventClicked()

