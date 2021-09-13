from pygame.constants import FULLSCREEN

import databaseHandler
import hashlib
import datetime
import objectHandler as ob

import pygame
import userInterface as ui 
import eventListener
import sys
import os

import math

VERSION = "v1.0.4 Alpha"

class data():
    userID = 0
    menuStages = []
    currentMenu = "MainMenu"
    gConst = 6.674 * 10 ** -11
    velocityMultiplier = 200
    simulation = False
    choosingNewObjectVelocity = False
    objectPlaceMode = 0
    objectData = []
    objectCount = 0
    planetLabels = []
    selectedObject = None
    solarSystemID = 0
    creatingNewPlanet = False
    systemObjects = []
    simulationSpeed = 0
    systemSize = 1000000000000
    screenConversion = 0
    screenOffsetX = 0
    screenOffsetY = 0
    currentAction = None
    currentLesson = None
    lessonID = 0
    lessonStage = 0
    tickClock = None
    timeSinceLastTick = 0
    ghost_planet = None
    simDate = None

class ghostPlanet():
    def __init__(self, radius, colour):
        self.radius = radius
        self.colour = colour
        self.xpos = 0
        self.ypos = 0
        #by default, the parent is the sun
        self.parent = listener.objectListeners[0]

    def update(self):
        #get the coordinates of the planet
        if data.objectPlaceMode == 0 or data.choosingNewObjectVelocity == False:
            self.xpos = pygame.mouse.get_pos()[0]
            self.ypos = pygame.mouse.get_pos()[1]

        #convert the coordinates of the mouse into system coordinates

        systemX = self.xpos * data.screenConversion - data.screenOffsetX
        systemY = self.ypos * data.screenConversion - data.screenOffsetY
        
        #update the distance label
        parentDistance = math.sqrt((systemX - self.parent.x_pos)**2 + (systemY - self.parent.y_pos)**2)
        gui.labelObjectDistance.setText("Distance: " + f"{round(parentDistance / 1000):,d}" + " km")
        gui.labelObjectDistance.xpos = (self.xpos + self.parent.screen_x) / 2
        gui.labelObjectDistance.ypos = (self.ypos + self.parent.screen_y) / 2

        #getting the velocity of the new object
        if data.choosingNewObjectVelocity:
            xvel = (pygame.mouse.get_pos()[0] - self.xpos) * data.velocityMultiplier
            yvel = (pygame.mouse.get_pos()[1] - self.ypos) * data.velocityMultiplier
            vel = math.sqrt(xvel**2 + yvel**2)
            #updating the velocity label
            gui.labelObjectVelocity.setText("Velocity: " + f"{round(vel / 1000):,d}" + " km/s")
            gui.labelObjectVelocity.xpos = (self.xpos + pygame.mouse.get_pos()[0]) / 2
            gui.labelObjectVelocity.ypos = (self.ypos + pygame.mouse.get_pos()[1]) / 2

        closest = None
        parentClosest = None
        #for loop to find the object with the highest value of F/d^2
        for obj in listener.objectListeners:
            distanceSquared = (systemX - obj.x_pos) ** 2 + (systemY - obj.y_pos) ** 2
            if distanceSquared != 0:
                force = data.gConst * obj.mass / (distanceSquared)
                value = force / (distanceSquared)
                if closest == None:
                    closest = value
                    parentClosest = obj
                elif closest < value:
                    closest = value
                    parentClosest = obj
            else:
                parentClosest = obj

        #set parent to this object
        self.parent = parentClosest

    def draw(self):
        #draw circle representing new object
        pygame.draw.circle(SCREEN, self.colour, (self.xpos, self.ypos), self.radius)
        #draw line from parent to position
        pygame.draw.aaline(SCREEN, self.colour, (self.xpos, self.ypos), (int(self.parent.screen_x), int(self.parent.screen_y)))
        #draw velocity line if needed
        if data.objectPlaceMode == 1 and data.choosingNewObjectVelocity:
            pygame.draw.aaline(SCREEN, (255, 255, 255), (self.xpos, self.ypos), pygame.mouse.get_pos())

class Window():
    def __init__(self):
        self.SCREEN = pygame.display.set_mode((0, 0), FULLSCREEN)
        pygame.display.set_caption("SolarSystemMaker " + VERSION)
        self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()
        self.SAVED_WIDTH, self.SAVED_HEIGHT = 1280, 720
        self.FULLSCREEN = True

    def toggleFullscreen(self):
        if self.FULLSCREEN:
            self.SCREEN = pygame.display.set_mode((self.SAVED_WIDTH, self.SAVED_HEIGHT), pygame.RESIZABLE)
        else:
            self.SCREEN = pygame.display.set_mode((0, 0), FULLSCREEN)
        self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()
        self.FULLSCREEN = not self.FULLSCREEN
        gui.reloadUI()

class UIElements():
    def __init__(self):
        ui.init(window.SCREEN, listener)
        self.createUI()

    def createUI(self):
        self.windowPlanetInfo = ui.window(text="", colour = (38, 38, 38), 
                            xpos = window.WIDTH - 480, ypos = 0, width=480, 
                            height = window.HEIGHT, outlineColour=(127, 127, 127))

        self.labelPlanetName = ui.label(text="", xAlign="centre", window = self.windowPlanetInfo, ypos = 30, xpos = 240, textBold=True, textSize = 32)
        self.labelPlanetVelocity = ui.label(text="", xAlign="left", window = self.windowPlanetInfo, ypos = 130, xpos = 20, textBold=True, textSize = 20)
        self.labelPlanetDistance = ui.label(text="", xAlign="left", window = self.windowPlanetInfo, ypos = 100, xpos = 20, textBold=True, textSize = 20)
        self.labelPlanetParent = ui.label(text="", xAlign="left", window = self.windowPlanetInfo, ypos = 70, xpos = 20, textBold=True, textSize = 20)

        self.buttonQuit = ui.actionButton(text="Quit", xpos=150, ypos=65, action=quitClicked, textBold=True, xMargin=60, textSize=32, outline=2, yMargin=2)
        self.buttonRegister = ui.actionButton(text="Register", xpos=window.WIDTH/2, ypos=window.HEIGHT/2-85, action=registerClicked, textBold=True, width=160, textSize=32, outline=2)
        self.buttonLogin = ui.actionButton(text="Login", xpos=window.WIDTH/2, ypos=window.HEIGHT/2, action=loginClicked, textBold=True, width=160, textSize=32, outline=2)
        self.buttonGuest = ui.actionButton(text="Guest", xpos=window.WIDTH/2, ypos=window.HEIGHT/2+85, action=guestClicked, textBold=True, width=160, textSize=32, outline=2)
        self.buttonBack = ui.actionButton(text="Back", xpos=150, ypos=65, action=backClicked, textBold=True, xMargin=60, textSize=32, outline=2, yMargin=2)

        self.buttonSimulationSave = ui.actionButton(text="Save", xpos = 48, xMargin = 15, ypos = 20, 
                                            action=simulationSaveClicked, textBold = True, yMargin = 8, outline = 1, textSize = 28)
        self.buttonLessons = ui.actionButton(text="Lessons", xpos = 172, xMargin = 15, ypos = 20, 
                                        action=lessonsClicked, textBold = True, yMargin = 8, outline = 1, textSize = 28)
        self.buttonSimulationExit = ui.actionButton(text="Exit", xpos = 295, xMargin = 15, 
                                            ypos = 20, action=simulationExitClicked, 
                                            textBold = True, yMargin = 8, outline = 1, textSize = 28)

        self.buttonNewPlanet = ui.actionButton(text="New object", xpos = 600, xMargin = 10, ypos = 80, 
                                            action=newPlanetClicked, textBold = True, 
                                            yMargin = 2, outline = 3, textSize = 32, drawPriority = "High")
        self.buttonTogglePlaceMode = ui.toggleButton(text1="Quick place", text2="Custom place", xpos = 355, 
                                                xMargin = 10, ypos = 80, action=togglePlaceModeClicked, 
                                                textBold = True, yMargin = 2, outline = 3, textSize = 32,
                                                colour1=(91, 155, 213), colour2=(237, 125, 49), drawPriority="High")
        self.buttonToggleLabels = ui.toggleButton(text1="Labels on", text2="Labels off", xpos = 120, 
                                                xMargin = 10, ypos = 80, action=toggleLabelsClicked, 
                                                textBold = True, yMargin = 2, outline = 3, textSize = 32,
                                                colour1=(91, 155, 213), colour2=(237, 125, 49), drawPriority="High")

        self.sliderZoom = ui.slider(xpos = 400, ypos = window.HEIGHT - 40, leftValue=0, rightValue=1, action=sliderZoomMoved, defaultValue=0.5, 
                            lineColour=(166, 166, 166), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200, drawPriority="High")

        self.sliderSimulationSpeed = ui.slider(xpos = 100, ypos = window.HEIGHT - 40, leftValue=0, rightValue=8, action=sliderSimulationSpeedMoved, defaultValue=0, 
                            lineColour=(166, 166, 166), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200, drawPriority="High")

        self.labelSimulationTime = ui.multiLinelabel(xpos = 800, xAlign = "centre", yAlign = "centre", textBold=False, ypos = window.HEIGHT - 40, textSize = 22, maxWidth = 300, drawPriority = "High")
        self.labelSimulationSpeed = ui.multiLinelabel(xpos = 200, xAlign = "centre", textBold=False, ypos = self.sliderSimulationSpeed.ypos - 50, textSize = 22, maxWidth = 300, drawPriority="High")
        self.labelZoom = ui.multiLinelabel(xpos = self.sliderZoom.xpos + self.sliderZoom.width / 2, xAlign = "centre", textBold=False, ypos = self.sliderZoom.ypos - 30, textSize = 22, maxWidth = 300, text = "Zoom", drawPriority="High")

        self.sliderPlanetRed = ui.slider(xpos = 20, ypos = 170, leftValue=0, rightValue=255, action=planetColourChanged, defaultValue=0.5, 
                            lineColour=(255, 0, 0), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200, window=self.windowPlanetInfo)
        self.sliderPlanetGreen = ui.slider(xpos = 20, ypos = 210, leftValue=0, rightValue=255, action=planetColourChanged, defaultValue=0.5, 
                            lineColour=(0, 176, 80), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200, window=self.windowPlanetInfo)
        self.sliderPlanetBlue = ui.slider(xpos = 20, ypos = 250, leftValue=0, rightValue=255, action=planetColourChanged, defaultValue=0.5, 
                            lineColour=(0, 112, 192), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200, window=self.windowPlanetInfo)


        self.labelUpdates = ui.label(text="", xpos=window.WIDTH/2, ypos=window.HEIGHT/2 + 100, textSize=32, textBold=True)
        self.labelTitle = ui.label(text="SolarSystemMaker " + VERSION, xpos=window.WIDTH/2, ypos=140, textSize=48)
        self.labelRegisterError = ui.label(text="", xpos=window.WIDTH/2, ypos=window.HEIGHT/2+230, textSize=24, textBold=True)

        self.inputRegisterUsername = ui.inputBox(text="Enter username...", xpos=window.WIDTH/2, ypos=window.HEIGHT/2-70, textItalics=True, textBold=True, 
                                            asterisks=False, textSize=24, outline=2)
        self.inputRegisterPassword1 = ui.inputBox(text="Enter password...", xpos=window.WIDTH/2, ypos=window.HEIGHT/2, textItalics=True, textBold=True, 
                                            asterisks=True, textSize=24, outline=2)
        self.inputRegisterPassword2 = ui.inputBox(text="Enter password again...", xpos=window.WIDTH/2, ypos=window.HEIGHT/2+70, textItalics=True, textBold=True, 
                                            asterisks=True, textSize=24, outline=2)

        self.inputLoginUsername = ui.inputBox(text="Enter username...", xpos=window.WIDTH/2, ypos=window.HEIGHT/2-70, textItalics=True, textBold=True, 
                                            asterisks=False, textSize=24, outline=2)
        self.inputLoginPassword = ui.inputBox(text="Enter password...", xpos=window.WIDTH/2, ypos=window.HEIGHT/2, textItalics=True, textBold=True, 
                                            asterisks=True, textSize=24, outline=2)

        self.inputSystemName = ui.inputBox(text="Enter the name...", xpos=window.WIDTH/2, ypos=window.HEIGHT/2-70, textItalics=True, textBold=True, 
                                    asterisks=False, textSize=24, outline=2, inactiveColour=(255,255,255))

        self.inputPlanetName = ui.inputBox(text="Enter the name...", xpos = 170, ypos=320, textItalics=True, textBold=True, 
                                    asterisks=False, textSize=24, outline=2, window=self.windowPlanetInfo, width = 300)
        self.inputPlanetMass = ui.inputBox(text="Enter the mass...", xpos = 170, ypos=360, textItalics=True, textBold=True, 
                                    asterisks=False, textSize=24, outline=2, window=self.windowPlanetInfo, width = 300)

        self.buttonCreateSystem = ui.actionButton(text="Create!", xpos=window.WIDTH/2, ypos=window.HEIGHT/2 + 40, action=createSystemClicked, textBold=True, 
                                            xMargin=60, textSize=32, outline=2, yMargin=2)

        self.buttonCreate = ui.actionButton(text="Create a solar system", xpos=window.WIDTH/2, ypos=window.HEIGHT/2 + 40, action=createClicked, textBold=True, 
                                            width = 300, textSize=20, outline=2, yMargin=3)
        self.buttonLoad = ui.actionButton(text="Load a solar system", xpos=window.WIDTH/2, ypos=window.HEIGHT/2-40, action=loadClicked, textBold=True, 
                                            width = 300, textSize=20, outline=2, yMargin=3)


        self.buttonCreateAccount = ui.actionButton(text="Register", xpos=window.WIDTH/2, ypos=window.HEIGHT/2+140, action=createAccountClicked, textBold=True, 
                                            xMargin=60, textSize=32, outline=2, yMargin=2)
        self.buttonLoginAccount = ui.actionButton(text="Login", xpos=window.WIDTH/2, ypos=window.HEIGHT/2+70, action=loginAccountClicked, textBold=True, 
                                            xMargin=60, textSize=32, outline=2, yMargin=2)

        self.labelObjectDistance = ui.label(text = "")
        self.labelObjectVelocity = ui.label(text = "")

        self.windowLessonsInfo = ui.window(text="", colour = (38, 38, 38), xpos = 100, 
                                    ypos = 100, width=window.WIDTH - 200, height=window.HEIGHT - 200, 
                                    drawPriority = "Low", outlineColour=(127, 127, 127))
        self.labelLessonsInfoTitle = ui.label(text="Start a lesson", xpos=window.WIDTH/2, ypos=self.windowLessonsInfo.ypos + 50, textSize=48)
        self.windowLessonText = ui.window(text = "", colour = (38, 38, 38), xpos = 50, 
                                    ypos = 120, width=400, height=400, drawPriority = "Low", 
                                    outlineColour = (127, 127, 127))
        self.labelLessonText = ui.multiLinelabel(text = "", 
                                    xpos = 10, ypos = 10, maxWidth = self.windowLessonText.width - 20, 
                                    xAlign = "left", yAlign = "top", window=self.windowLessonText, textSize=24)

        self.windowSimulationExit = ui.window(text = "", colour = (38, 38, 38), 
                                        xpos = window.WIDTH / 2 - 200, ypos = window.HEIGHT / 2 - 50, 
                                        width = 400, height = 100, drawPriority = "Low", 
                                        outlineColour = (127, 127, 127))

        self.buttonConfirmExit = ui.actionButton(text="Exit without saving", xpos = 10, ypos = 75, 
                                            action=simulationExitConfirmed, textBold=True, 
                                            textSize=20, outline=2, yMargin=3,  
                                            window = self.windowSimulationExit, xAlign = "left")

        self.buttonCancelExit = ui.actionButton(text="Cancel", xpos = self.windowSimulationExit.width - 10, 
                                        ypos = 75, action=simulationExitCancelled, textBold=True, 
                                        textSize=20, outline=2, yMargin=3, 
                                        window = self.windowSimulationExit, xAlign = "right")

        self.labelConfirmExit = ui.multiLinelabel(text = "Are you sure you want to exit?\nChanges may not be saved.", 
                                            xpos = self.windowSimulationExit.width / 2, ypos = 10, 
                                            textBold=True, maxWidth = self.windowSimulationExit.width,
                                            xAlign = "centre", yAlign = "top", window=self.windowSimulationExit)

        self.loadTable = None
        self.lessonLoadTable = None
                    
    def reloadUI(self):
        data.screenConversion = data.systemSize / window.WIDTH  # calculates the scale multiplier
        data.screenOffsetX = data.systemSize / 2
        data.screenOffsetY = (data.systemSize / 2) * (window.HEIGHT / window.WIDTH)
        #update screen
        ob.updateScreen(data.screenConversion, data.screenOffsetX, data.screenOffsetY)

        self.windowPlanetInfo.updateRect(window.WIDTH - 480, 0, 480, window.HEIGHT)

        self.labelPlanetName.updateRect(240, 30)
        self.labelPlanetVelocity.updateRect(10, 130)
        self.labelPlanetDistance.updateRect(10, 100)
        self.labelPlanetParent.updateRect(10, 70)

        self.buttonRegister.updateRect(window.WIDTH/2, window.HEIGHT/2-85, 160, None)
        self.buttonLogin.updateRect(window.WIDTH/2, window.HEIGHT/2, 160, None)
        self.buttonGuest.updateRect(window.WIDTH/2, window.HEIGHT/2+85, 160, None)

        self.sliderZoom.updateRect(400, window.HEIGHT - 40, 200, 30)
        self.sliderSimulationSpeed.updateRect(100, window.HEIGHT - 40, 200, 30)

        self.labelSimulationTime.updateRect(800, window.HEIGHT - 40)
        self.labelSimulationSpeed.updateRect(200, self.sliderSimulationSpeed.ypos - 50)
        self.labelZoom.updateRect(self.sliderZoom.xpos + self.sliderZoom.width / 2, self.sliderZoom.ypos - 30)

        self.sliderPlanetRed.updateRect(20, 170, 200, 30)
        self.sliderPlanetGreen.updateRect(20, 210, 200, 30)
        self.sliderPlanetBlue.updateRect(20, 250, 200, 30)

        self.labelUpdates.updateRect(window.WIDTH/2, window.HEIGHT/2 + 100)
        self.labelTitle.updateRect(window.WIDTH/2, 140)
        self.labelRegisterError.updateRect(window.WIDTH/2, window.HEIGHT/2+230)

        self.inputRegisterUsername.updateRect(window.WIDTH/2, window.HEIGHT/2-70, None, None)
        self.inputRegisterPassword1.updateRect(window.WIDTH/2, window.HEIGHT/2, None, None)
        self.inputRegisterPassword2.updateRect(window.WIDTH/2, window.HEIGHT/2+70, None, None)

        self.inputLoginUsername.updateRect(window.WIDTH/2, window.HEIGHT/2-70, None, None)
        self.inputLoginPassword.updateRect(window.WIDTH/2, window.HEIGHT/2, None, None)

        self.inputSystemName.updateRect(window.WIDTH/2, window.HEIGHT/2-70, None, None)

        self.inputPlanetName.updateRect(170, 320, 300, None)
        self.inputPlanetMass.updateRect(170, 360, 300, None)

        self.buttonCreateSystem.updateRect(window.WIDTH/2, window.HEIGHT/2 + 40, self.buttonCreateSystem.width, None)
        self.buttonCreate.updateRect(window.WIDTH/2, window.HEIGHT/2 + 40, self.buttonCreate.width, None)
        self.buttonLoad.updateRect(window.WIDTH/2, window.HEIGHT/2-40, self.buttonLoad.width, None)

        self.buttonCreateAccount.updateRect(window.WIDTH/2, window.HEIGHT/2+140, self.buttonCreateAccount.width, None)
        self.buttonLoginAccount.updateRect(window.WIDTH/2, window.HEIGHT/2+70, self.buttonLoginAccount.width, None)

        self.windowLessonsInfo.updateRect(100, 100, window.WIDTH - 200, window.HEIGHT - 200)
        self.labelLessonsInfoTitle.updateRect(window.WIDTH/2, self.windowLessonsInfo.ypos + 50)
        self.labelLessonText.updateRect(10, 10)

        self.windowSimulationExit.updateRect(window.WIDTH / 2 - 200, window.HEIGHT / 2 - 50, 400, 100)
        self.buttonConfirmExit.updateRect(10, 75, None, None)
        self.buttonCancelExit.updateRect(self.windowSimulationExit.width - 10, 75, None, None)
        self.labelConfirmExit.updateRect(self.windowSimulationExit.width / 2, 10)

        if self.loadTable:
            self.loadTable.updateRect(90, 200, window.WIDTH - 90 * 2, 400)
        if self.lessonLoadTable:
            self.lessonLoadTable.updateRect(50, 110, gui.windowLessonsInfo.width - 50 * 2, 350)

def registerAccount(username, password1, password2):
    if username == False:
        return 8
    if password1 == False or password2 == False:
        return 9
    if password1 != password2: # check both passwords match
        return 7
    password = password1
    if len(username) > 64: # check username length
        return 4
    if len(password) > 4: # check password length
        passwordHash = hashlib.sha256(password.encode()).hexdigest() # hash pword
    else:
        return 1
    accounts = db.loadAccounts(username) # load accounts with same username
    if len(accounts) == 0: # if there isn't one then create the account 
        db.createAccount(username, passwordHash)
        login(username, password)
        return 0
    else:
        return 3

def login(username, password):
    if username == False:
        return 8
    if password == False:
        return 9
    password = hashlib.sha256(password.encode()).hexdigest() 
    # hash the password so it can be compared
    accounts = db.loadAccounts(username) #search for accounts with
    # requested username
    if len(accounts) == 0:
        return 5 #if none exist return 5
    else:
        if str(accounts[0][2]) == str(password):
            data.userID = accounts[0][0]
            return 0 #if the password is correct, login
        else:
            return 6 #otherwise return 6

def createSolarSystem(name):
    data.systemObjects = []
    date = datetime.date.today().strftime("%d-%b-%y").upper()
    data.objectCount = 1
    data.simDate = datetime.datetime.today()
    db.insertSolarSystem(name, date, data.objectCount, data.userID, data.simDate)

def loadSolarSystemList():
    choices = db.getUserSolarSystems(data.userID)
    return choices 

#creates all the instances of systemObject 
def createSystemObjects():
    data.systemObjects = []
    for i in data.objectData:
        data.systemObjects.append(ob.systemObject(i))
    listener.setObjects(data.systemObjects)
    for i in listener.objectListeners:
        i.init()

#creates the objectData array 
def createObjectData():
    objectData = []
    for i in listener.objectListeners:
        objectData.append(i.getData())
    return objectData

def setupLesson(lessonID):
    lessonStages = db.loadLessonStages(lessonID)
    lessonStagesSorted = sorted(lessonStages, key = lambda x: x[4])
    return lessonStagesSorted

def quitClicked():
    sys.exit()

#when the register button on the main menu is clicked
def registerClicked():
    ui.hideAll()
    gui.buttonBack.show()
    gui.labelTitle.show()
    gui.labelTitle.setText("Register") 
    gui.inputRegisterUsername.show()
    gui.inputRegisterPassword1.show()
    gui.inputRegisterPassword2.show()
    gui.buttonCreateAccount.show()
    data.menuStages.append("Register")
    #show input boxes and buttons

#when the login button on the main menu is clicked
def loginClicked():
    ui.hideAll()
    gui.buttonBack.show()
    gui.labelTitle.show()
    gui.labelTitle.setText("Login")
    gui.inputLoginUsername.show()
    gui.inputLoginPassword.show()
    gui.buttonLoginAccount.show()
    data.menuStages.append("Login")
    #show input boxes and buttons

#when the guest button on the main menu is clicked
def guestClicked():
    ui.hideAll()
    # guest ID is 1
    data.userID = 1
    createOrLoad()
    #show input boxes and buttons

def backClicked():
    #we must pop twice - once to remove the
    #stage the user is leaving, and once to
    #remove the stage that will be readded
    data.menuStages.pop()
    newStage = data.menuStages.pop()
    if newStage == "MainMenu":
        mainMenu()
    elif newStage == "Login":
        loginClicked()
    elif newStage == "Register":
        registerClicked()
    elif newStage == "CreateOrLoad":
        createOrLoad()

def createOrLoad():
    #setting up the create or load screen 
    ui.hideAll()
    gui.buttonBack.show()
    gui.labelTitle.show()
    gui.buttonCreate.show()
    gui.buttonLoad.show()
    gui.labelTitle.setText("Create or load a solar system?")
    data.menuStages.append("CreateOrLoad")

def createAccountClicked():
    #get the input from the boxes
    username = gui.inputRegisterUsername.getInput()
    password1 = gui.inputRegisterPassword1.getInput()
    password2 = gui.inputRegisterPassword2.getInput()
    error = registerAccount(username, password1, password2) #attempt to create an account
    gui.labelRegisterError.show() #show the error message label
    #set the text of the error label according to the error
    if error == 0:
        #move to create or load screen if no error
        createOrLoad()
    elif error == 1:
        gui.labelRegisterError.setText("Password is too short!")
    elif error == 2:
        gui.labelRegisterError.setText("Unable to connect to the database")
    elif error == 3:
        gui.labelRegisterError.setText("An account with this username already exists!")
    elif error == 4:
        gui.labelRegisterError.setText("Username is too long!")
    elif error == 7:
        gui.labelRegisterError.setText("Passwords do not match!")
    elif error == 8:
        gui.labelRegisterError.setText("A username has not been entered!")
    elif error == 9:
        gui.labelRegisterError.setText("You have not entered your password twice!")

def loginAccountClicked():
    #get the input from the boxes
    username = gui.inputLoginUsername.getInput()
    password = gui.inputLoginPassword.getInput()
    error = login(username, password) #attempt to login
    gui.labelRegisterError.show() #show the error message label
    if error == 0:
        #move to create or load screen if no error
        createOrLoad()
    if error == 5 or error == 6:
        gui.labelRegisterError.setText("Incorrect credentials!")
    if error == 8:
        gui.labelRegisterError.setText("A username has not been entered!")
    if error == 9:
        gui.labelRegisterError.setText("A password has not been entered!")

#when the Load button on the load / create screen is clicked
def loadClicked():
    #update the UI 
    ui.hideAll()
    gui.buttonBack.show()
    gui.labelTitle.show()
    gui.labelTitle.setText("Pick a solar system to load.")
    #get the solar systems that the user has access to
    solarSystems = db.getUserSolarSystems(data.userID)
    #creating the array to be passed into the table
    solarSystemsFormat = [["Name", "Objects", "Last saved"]]
    #format: name, objectCount, date, solarsystemID
    for i in range(0, len(solarSystems)):
        solarSystemsFormat.append([str(solarSystems[i][1]), str(db.getNumberOfObjects(solarSystems[i][0])), 
                                   str(solarSystems[i][2].strftime("%d/%m/%y")), int(solarSystems[i][0])])
    #creating and showing the table
    gui.loadTable = ui.table(data = solarSystemsFormat, xpos = 90, ypos = 200, width = window.WIDTH - 90 * 2, 
                         height = 400, textSize = 30, rowsPerPage = 4, selectButtons = True, 
                         buttonText = "Load", action = onLoadTableResult)
    gui.loadTable.show()
    #finally, we update the menuStages 
    data.menuStages.append("Load")

def createClicked():
    ui.hideAll()
    gui.buttonBack.show()
    gui.labelTitle.show()
    gui.buttonCreateSystem.show()
    if data.userID != 1: #if the user is not a guest, allow them to pick a name
        gui.inputSystemName.show()
        gui.labelTitle.setText("Choose the name")
    else:   #otherwise, don't allow them to pick a name
        gui.labelRegisterError.setText("Warning: You are logged in as a Guest. Your solar system will not be saved.")
        gui.labelRegisterError.show()
        gui.labelTitle.setText("Guest create")
    data.menuStages.append("Create")

def createSystemClicked():
    #hide the user interface
    ui.hideAll()
    #create objectData for guests 
    data.objectData = []
    data.objectData.append([0, data.solarSystemID, 0, 0, "Sun", 0, 0, 0, 0, 1.989 * (10 ** 30), 255, 255, 0])
    if data.userID != 1:
        #if the user is not a guest, we upload the new solar system to the database, with the name
        createSolarSystem(gui.inputSystemName.getInput())
        #to get the ID of the new solar system, we call getNewSolarSystem
        solarSystemID = db.getNewSolarSystem()
        data.solarSystemID = int(solarSystemID[0][0])

        data.objectData = []
        data.objectData.append([0, data.solarSystemID, 0, 0, "Sun", 0, 0, 0, 0, 1.989 * (10 ** 30), 255, 255, 0])
    
        #then we update the database with the new objectData
        db.updateObjectsDatabase(data.objectData)
    else:
        data.simDate = datetime.datetime.today()
    data.objectCount = 1
    data.systemSize = 1000000000000
    simulationSetup()

def mainMenu():
    ui.hideAll()
    gui.buttonQuit.show()
    gui.buttonRegister.show()
    gui.buttonLogin.show()
    gui.buttonGuest.show()
    gui.labelTitle.show()
    gui.labelTitle.setText("SolarSystemMaker")
    data.menuStages.append("MainMenu")

def onLoadTableResult(ID):
    gui.loadTable.hide()
    data.solarSystemID = ID
    ui.hideAll()
    data.objectData = []
    #getting the solar system information from the database
    solarSystem = db.getSolarSystem(data.solarSystemID)
    data.objectCount = solarSystem[0][3]
    data.systemSize = 1000000000000
    data.objectData = db.loadObjects(data.solarSystemID)
    data.simDate = solarSystem[0][4]
    if not data.simDate:
        data.simDate = datetime.datetime.today()
    #running simulationSetup to complete the rest of setup
    simulationSetup()

def simulationSetup():
    #calculates the scale multiplier
    data.screenConversion = data.systemSize / window.WIDTH 
    #calculates the offset values (as the star is at 
    #the center but 0,0 on the screen is top left)
    data.screenOffsetX = data.systemSize / 2
    data.screenOffsetY = (data.systemSize / 2) * (window.HEIGHT / window.WIDTH)
    ob.updateScreen(data.screenConversion, data.screenOffsetX, data.screenOffsetY)

    #load the objects from the database and create the systemObjects
    if data.userID != 1:
        data.objectData = db.loadObjects(data.solarSystemID)
    createSystemObjects()
    data.simulation = True

    ## Here we will update the user interface with all the relevant elements
    gui.buttonTogglePlaceMode.show()
    gui.buttonNewPlanet.show()
    gui.sliderSimulationSpeed.show()
    gui.labelSimulationSpeed.show()
    gui.labelSimulationTime.show()
    gui.buttonToggleLabels.show()
    gui.sliderZoom.show()
    gui.labelZoom.show()
    gui.buttonSimulationExit.show()

    ## Planet labels will also be set up here

    #begin the tickClock in preparation for simulation
    data.tickClock.tick()
    data.timeSinceLastTick = 0

    data.ghost_planet = ghostPlanet(10, (128, 128, 128))

    if data.userID != 1:
        gui.buttonSimulationSave.show()

    gui.buttonLessons.show()

    #fixes a crash caused when reloading solar sysems
    data.planetLabels.clear()

    for i in listener.objectListeners:
        data.planetLabels.append(ui.label(text = i.name, textBold = True, xAlign="left", yAlign="bottom", drawPriority="High"))
    for i in data.planetLabels:
        i.show()

def simulationSaveSetup():
    data.objectData = db.loadObjects(data.solarSystemID)
    createSystemObjects()
    data.simulation = True
    data.tickClock.tick()
    data.timeSinceLastTick = 0

def simulationSaveClicked():
    gui.labelUpdates.setText("Saving...")
    gui.labelUpdates.show()
    gui.labelUpdates.draw()
    pygame.display.update()
    data.objectData = createObjectData()
    db.updateObjectsDatabase(data.objectData)
    db.updateSolarSystem(datetime.date.today().strftime("%d-%b-%y").upper(), data.objectCount, data.solarSystemID, data.simDate)
    data.objectData = []
    gui.labelUpdates.hide()
    simulationSaveSetup()

    pygame.display.update()

def simulationExitClicked():
    gui.windowSimulationExit.show()

#function to run when the user confirms to exit
def simulationExitConfirmed():
    #return to the create or load screen
    while data.menuStages[len(data.menuStages) - 1] != "CreateOrLoad":
        data.menuStages.pop()
    data.menuStages.pop()
    createOrLoad()
    #reset variables
    data.simulation = False
    data.solarSystemID = 0
    data.objectData = []
    listener.objectListeners = []
    data.objectCount = 0
    data.creatingNewPlanet = False
    data.selectedObject = None

def simulationExitCancelled():
    gui.windowSimulationExit.hide()

#function to update place mode when toggleButton clicked
def togglePlaceModeClicked():
    if data.objectPlaceMode == 0:
        data.objectPlaceMode = 1
    elif data.objectPlaceMode == 1:
        data.objectPlaceMode = 0

#when the new planet button is clicked, begin creating a new planet 
#if not already
def newPlanetClicked():
    if data.creatingNewPlanet == False:
        data.creatingNewPlanet = True
        gui.labelObjectDistance.show()
    
def createNewPlanetCustom():
    #get the parent, position and velocity from the ghost planet. 
    parent = data.ghost_planet.parent
    xpos = data.ghost_planet.xpos
    ypos = data.ghost_planet.ypos
    xvel = (pygame.mouse.get_pos()[0] - xpos) * data.velocityMultiplier
    yvel = (pygame.mouse.get_pos()[1] - ypos) * data.velocityMultiplier
    xpos = xpos * data.screenConversion - data.screenOffsetX
    ypos = ypos * data.screenConversion - data.screenOffsetY
    data.objectCount += 1
    #register as listener 
    listener.objectListeners.append(ob.systemObject([0, data.solarSystemID, parent.solarSystemObjectID, 
                                                    data.objectCount, "Planet " + str(data.objectCount - 1), xpos, 
                                                    ypos, xvel, yvel, 1.89 * 10 ** 24, 230, 130, 130]))
    i=listener.objectListeners[len(listener.objectListeners)-1]
    i.init()
    #reset variables, hide label
    data.creatingNewPlanet = False
    data.choosingNewObjectVelocity = False
    gui.labelObjectDistance.hide()
    gui.labelObjectVelocity.hide()

    data.planetLabels.append(ui.label(text = i.name, textBold = True, xAlign="left", yAlign="bottom", drawPriority="High"))
    data.planetLabels[len(data.planetLabels)-1].show()

def createNewPlanetQuick():
    parent = data.ghost_planet.parent #get the ghost planet
    #get planet coordinates by converting mouse coordinates
    xpos = pygame.mouse.get_pos()[0] * data.screenConversion - data.screenOffsetX
    ypos = pygame.mouse.get_pos()[1] * data.screenConversion - data.screenOffsetY

    #calculate velocities needed for circular orbit
    vel = math.sqrt(data.gConst * parent.mass / math.sqrt((xpos - parent.x_pos)**2 + (ypos - parent.y_pos)**2))
    xvelRelative = 1 / (math.sqrt(1 + ((xpos - parent.x_pos) / (ypos - parent.y_pos))**2)) * vel
    yvelRelative = (xpos - parent.x_pos) / (ypos - parent.y_pos) / (math.sqrt(1 + ((xpos - parent.x_pos) / (ypos - parent.y_pos))**2)) * vel
    #adjust velocities depending on quadrant
    if ypos > parent.y_pos:
        xvelRelative = -xvelRelative
    if ypos < parent.y_pos:
        yvelRelative = -yvelRelative
    #add parent velocity if needed
    xvel = xvelRelative + parent.x_vel
    yvel = yvelRelative + parent.y_vel

    #create new object
    data.objectCount += 1
    listener.objectListeners.append(ob.systemObject([0, data.solarSystemID, parent.solarSystemObjectID, 
                                                    data.objectCount, "Planet " + str(data.objectCount - 1), xpos, ypos, 
                                                    xvel, yvel, 1.89 * 10 ** 24, 230, 130, 130]))
    i=listener.objectListeners[len(listener.objectListeners)-1]
    i.init()

    #object has been created so this variable can now be reset
    data.creatingNewPlanet = False

    #here we will also create the label for the new object
    data.planetLabels.append(ui.label(text = i.name, textBold = True, xAlign="left", yAlign="bottom", drawPriority="High"))
    data.planetLabels[len(data.planetLabels)-1].show()
    
    gui.labelObjectDistance.hide()
    gui.labelObjectVelocity.hide()
    
def onObjectClicked(obj):
    data.selectedObject = obj
    gui.windowPlanetInfo.show()

    #labelPlanetName.setText(selectedObject.name)

def updatePlanetInfo():
    #get the object velocity and position
    xvel = data.selectedObject.x_vel
    yvel = data.selectedObject.y_vel
    velocity = math.sqrt(xvel ** 2 + yvel ** 2)
    xpos = data.selectedObject.x_pos
    ypos = data.selectedObject.y_pos
    #get the distance to the parent object
    distance = math.sqrt((xpos - data.selectedObject.parent.x_pos)** 2 + (ypos - data.selectedObject.parent.y_pos) ** 2)
    gui.labelPlanetVelocity.setText("Velocity: " + f"{round(velocity):,d}" + " m/s")
    gui.labelPlanetName.setText(data.selectedObject.name)
    #if the object is not the sun (i.e it is orbiting something)
    if data.selectedObject.solarSystemObjectID != 0:
        #update the orbing text and thedistance text
        gui.labelPlanetParent.setText("Orbiting: " + str(data.selectedObject.parent.name))
        gui.labelPlanetDistance.setText("Distance to " + str(data.selectedObject.parent.name) 
                                    + ": " + f"{round(distance / 1000):,d}" + " km")
    #otherwise, it is orbiting nothing
    else:
        gui.labelPlanetParent.setText("Orbiting: None")
        gui.labelPlanetDistance.setText("")

    gui.sliderPlanetRed.setValue(data.selectedObject.red)
    gui.sliderPlanetGreen.setValue(data.selectedObject.green)
    gui.sliderPlanetBlue.setValue(data.selectedObject.blue)
    #inputPlanetName.defaultText = selectedObject.name

def sliderZoomMoved():
    #set system size logarithmically
    data.systemSize = 10**10 * 10**(4*(1-gui.sliderZoom.getValue())) 
    systemZoom()

def mouseWheelZoom(value):
    gui.sliderZoom.setValue(gui.sliderZoom.getValue() + value)
    sliderZoomMoved()

def systemZoom():
    data.screenConversion = data.systemSize / window.WIDTH  # calculates the scale multiplier
    data.screenOffsetX = data.systemSize / 2
    data.screenOffsetY = (data.systemSize / 2) * (window.HEIGHT / window.WIDTH)
    #update screen
    ob.updateScreen(data.screenConversion, data.screenOffsetX, data.screenOffsetY)

def sliderSimulationSpeedMoved():
    data.simulationSpeed = 10**gui.sliderSimulationSpeed.getValue()

def planetColourChanged():
    data.selectedObject.setColour(int(gui.sliderPlanetRed.getValue()), 
                             int(gui.sliderPlanetGreen.getValue()), 
                             int(gui.sliderPlanetBlue.getValue()))

#update the planet labels' names and coordinates.
def updateLabels():
    gui.labelSimulationSpeed.setText("Simulation rate:\n" + getSimSpeedString(data.simulationSpeed))
    gui.labelSimulationTime.setText("Date / Time:\n" + data.simDate.strftime("%d/%m/%Y, %H:%M:%S"))
    #update the planet labels
    for i in range(0, len(data.planetLabels)):
        data.planetLabels[i].xpos = listener.objectListeners[i].screen_x
        data.planetLabels[i].ypos = listener.objectListeners[i].screen_y - listener.objectListeners[i].radius / 2 - 5
        data.planetLabels[i].setText(listener.objectListeners[i].name)

#simplify the simulation speed label
def getSimSpeedString(simulationSpeed):
    default = "1 second = "
    if simulationSpeed < 60:
        seconds = simulationSpeed
        return default + str(round(seconds)) + " seconds"
    elif simulationSpeed < 3600:
        minutes = simulationSpeed / 60
        return default + str(round(minutes)) + " minutes"
    elif simulationSpeed < 86400:
        hours = simulationSpeed / 3600
        return default + str(round(hours)) + " hours"
    elif simulationSpeed < 604800:
        days = simulationSpeed / 86400
        return default + str(round(days)) + " days"
    elif simulationSpeed < 2628288:
        weeks = simulationSpeed / 604800
        return default + str(round(weeks)) + " weeks"
    elif simulationSpeed < 31536000:
        months = simulationSpeed / 2628288
        return default + str(round(months)) + " months"
    else:
        years = simulationSpeed / 31536000
        return default + str(round(years)) + " years"

def lessonsClicked():
    #show the updates text
    gui.labelUpdates.setText("Loading...")
    gui.labelUpdates.show()
    gui.labelUpdates.draw()
    #force a display update so that the text is drawn
    pygame.display.update()
    Lessons = db.loadLessons()
    lessonsFormat = [["Name", "Description"]]
    #create the array of lesson data
    for i in range(0, len(Lessons)):
        lessonsFormat.append([str(Lessons[i][1]), str(Lessons[i][2]), int(Lessons[i][0])])
    #create the table
    gui.lessonLoadTable = ui.table(data = lessonsFormat, xpos = 50, ypos = 110, 
                        width = gui.windowLessonsInfo.width - 100, height = 350, textSize = 30, 
                        rowsPerPage = 4, selectButtons = True, buttonText = "Load", 
                        action = onLessonsTableResult, window = gui.windowLessonsInfo)
    gui.lessonLoadTable.show()
    gui.windowLessonsInfo.show()
    gui.labelLessonsInfoTitle.show()
    gui.labelUpdates.hide()

def onLessonsTableResult(ID):
    data.lessonStage = 0
    data.lessonID = ID
    data.objectData = []
    #load the array of lessons
    data.currentLesson = db.loadLessonStages(data.lessonID)
    #hide the window
    gui.windowLessonsInfo.hide()
    gui.labelLessonsInfoTitle.hide()
    #set the currrent action
    data.currentAction = data.currentLesson[data.lessonStage][3]
    nextLessonStage()

def checkLessonAction(action):
    #if the required action has been completed,
    if data.currentAction == action:
        data.lessonStage += 1
        #start the next lesson stage
        nextLessonStage()

def nextLessonStage(): #start the lesson stage 
    if data.currentLesson:
        #if the lesson is finished, hide the window
        if data.lessonStage >= len(data.currentLesson):
            gui.windowLessonText.hide()
            data.currentLesson = None
        else: #otherwise, setup the new lesson stage
            gui.labelLessonText.setText(str(data.currentLesson[data.lessonStage][2]))
            gui.windowLessonText.height = gui.labelLessonText.height + 20
            gui.windowLessonText.show()
            data.currentAction = data.currentLesson[data.lessonStage][3]
        
def toggleLabelsClicked():
    if gui.buttonToggleLabels.state == 1:
        for i in data.planetLabels:
            i.show()
    else:
        for i in data.planetLabels:
            i.hide() 

pygame.init()
db = databaseHandler.database()

#creating a pygame screen
window = Window()
SCREEN = window.SCREEN

WIDTH, HEIGHT = window.WIDTH, window.HEIGHT

#creating a listener object
listener = eventListener.Listener()

#initialising userInterface and objectHandler
#ui.init(SCREEN, listener)
ob.init(SCREEN, listener.objectListeners, onObjectClicked)

gui = UIElements()

paused = False

frameClock = pygame.time.Clock()
data.tickClock = pygame.time.Clock()

FPS = 60
frame_every_ms = 1000 / FPS
timeSinceLastFrame = 0

data.simulationSpeed = 1

mainMenu()
while True:
    for event in pygame.event.get(): #iterate the pygame event queue
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  #quit pygame if the user quits

        if event.type == pygame.MOUSEBUTTONDOWN: #if the user has clicked
            if data.creatingNewPlanet: #check if we are currently creating an object
                if data.objectPlaceMode == 0: #if using quick place, create new object
                    createNewPlanetQuick()
                    gui.labelObjectDistance.hide()
                else: #if we are using custom place
                    if data.choosingNewObjectVelocity == False:
                        data.choosingNewObjectVelocity = True
                        gui.labelObjectVelocity.show()
                    else:
                        createNewPlanetCustom()
                        gui.labelObjectVelocity.hide()
            if event.button == 4:
                mouseWheelZoom(0.02)
            if event.button == 5:
                mouseWheelZoom(-0.02)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                checkLessonAction("spacePressed")
            #if the object window is active, close it when escape pressed
            if event.key == pygame.K_ESCAPE:
                if data.selectedObject:
                    data.selectedObject = None
                    gui.windowPlanetInfo.hide()
            if event.key == pygame.K_RETURN:
                #if the name box is active, update the name
                if gui.inputPlanetName.active:
                    data.selectedObject.name = gui.inputPlanetName.getInput()
                    updatePlanetInfo()
                #if the mass box is active update the mass
                if gui.inputPlanetMass.active:
                    #this try / except handles the case where the user does not enter an integer
                    try:
                        data.selectedObject.mass = int(gui.inputPlanetMass.getInput())
                        updatePlanetInfo()
                    except:
                        pass
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] and keys[pygame.K_ESCAPE]:
                window.toggleFullscreen()
        
        listener.pollUI(event) #use event listener to poll the elements         
        listener.pollObjects(event)

        if event.type == pygame.VIDEORESIZE:
            window.SCREEN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            window.WIDTH = event.w
            window.HEIGHT = event.h
            gui.reloadUI()
            data.tickClock.tick()
            data.timeSinceLastTick = 0
        
    #if a frame's period of time has passed, we draw everything + update display
    if timeSinceLastFrame > frame_every_ms:
        SCREEN.fill((0, 0, 0)) #fill the screen black
        print(data.systemSize)
        #draw all the objects if we are in the simulation
        if data.simulation:
            for element in listener.objectListeners:
                element.draw()
            #draw and update the ghost planet if a new planet is being created 
            if data.creatingNewPlanet:
                data.ghost_planet.update()
                data.ghost_planet.draw()
            updateLabels()
            #if an object is selected, update its information
            if data.selectedObject:
                updatePlanetInfo()

        for element in listener.uiListeners:
            element.draw() #draw all the UI elements
        if data.selectedObject:
            pygame.draw.circle(SCREEN, (int(gui.sliderPlanetRed.getValue()), int(gui.sliderPlanetGreen.getValue()), int(gui.sliderPlanetBlue.getValue())), (gui.sliderPlanetGreen.xpos + 280, int(gui.sliderPlanetGreen.ypos + gui.sliderPlanetGreen.height / 2)), 40)
        pygame.display.update() #update the display
        timeSinceLastFrame = timeSinceLastFrame - frame_every_ms

    #if we are in the simulation we update all the systemObjects
    if data.simulation:
        for element in listener.objectListeners:
            element.tick(data.timeSinceLastTick * data.simulationSpeed)
        data.simDate = data.simDate + datetime.timedelta(milliseconds=data.timeSinceLastTick * data.simulationSpeed)
    
    #updating the clocks
    timeSinceLastFrame = timeSinceLastFrame + frameClock.tick()
    if data.simulation:
        data.timeSinceLastTick = data.tickClock.tick()