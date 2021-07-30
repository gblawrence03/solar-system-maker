import databaseHandler
import hashlib
import datetime
import objectHandler as ob

import pygame
import userInterface as ui 
import eventListener
import sys

import math

version = "Alpha v1.0.1"

class data():
    userID = 0
    menuStages = []
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
        labelObjectDistance.setText("Distance: " + f"{round(parentDistance / 1000):,d}" + " km")
        labelObjectDistance.xpos = (self.xpos + self.parent.screen_x) / 2
        labelObjectDistance.ypos = (self.ypos + self.parent.screen_y) / 2

        #getting the velocity of the new object
        if data.choosingNewObjectVelocity:
            xvel = (pygame.mouse.get_pos()[0] - self.xpos) * data.velocityMultiplier
            yvel = (pygame.mouse.get_pos()[1] - self.ypos) * data.velocityMultiplier
            vel = math.sqrt(xvel**2 + yvel**2)
            #updating the velocity label
            labelObjectVelocity.setText("Velocity: " + f"{round(vel / 1000):,d}" + " km/s")
            labelObjectVelocity.xpos = (self.xpos + pygame.mouse.get_pos()[0]) / 2
            labelObjectVelocity.ypos = (self.ypos + pygame.mouse.get_pos()[1]) / 2

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
    buttonBack.show()
    labelTitle.show()
    labelTitle.setText("Register") 
    inputRegisterUsername.show()
    inputRegisterPassword1.show()
    inputRegisterPassword2.show()
    buttonCreateAccount.show()
    data.menuStages.append("Register")
    #show input boxes and buttons

#when the login button on the main menu is clicked
def loginClicked():
    ui.hideAll()
    buttonBack.show()
    labelTitle.show()
    labelTitle.setText("Login")
    inputLoginUsername.show()
    inputLoginPassword.show()
    buttonLoginAccount.show()
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
    buttonBack.show()
    labelTitle.show()
    buttonCreate.show()
    buttonLoad.show()
    labelTitle.setText("Create or load a solar system?")
    data.menuStages.append("CreateOrLoad")

def createAccountClicked():
    #get the input from the boxes
    username = inputRegisterUsername.getInput()
    password1 = inputRegisterPassword1.getInput()
    password2 = inputRegisterPassword2.getInput()
    error = registerAccount(username, password1, password2) #attempt to create an account
    labelRegisterError.show() #show the error message label
    #set the text of the error label according to the error
    if error == 0:
        #move to create or load screen if no error
        createOrLoad()
    elif error == 1:
        labelRegisterError.setText("Password is too short!")
    elif error == 2:
        labelRegisterError.setText("Unable to connect to the database")
    elif error == 3:
        labelRegisterError.setText("An account with this username already exists!")
    elif error == 4:
        labelRegisterError.setText("Username is too long!")
    elif error == 7:
        labelRegisterError.setText("Passwords do not match!")
    elif error == 8:
        labelRegisterError.setText("A username has not been entered!")
    elif error == 9:
        labelRegisterError.setText("You have not entered your password twice!")

def loginAccountClicked():
    #get the input from the boxes
    username = inputLoginUsername.getInput()
    password = inputLoginPassword.getInput()
    error = login(username, password) #attempt to login
    labelRegisterError.show() #show the error message label
    if error == 0:
        #move to create or load screen if no error
        createOrLoad()
    if error == 5 or error == 6:
        labelRegisterError.setText("Incorrect credentials!")
    if error == 8:
        labelRegisterError.setText("A username has not been entered!")
    if error == 9:
        labelRegisterError.setText("A password has not been entered!")

#when the Load button on the load / create screen is clicked
def loadClicked():
    #update the UI 
    ui.hideAll()
    buttonBack.show()
    labelTitle.show()
    labelTitle.setText("Pick a solar system to load.")
    #get the solar systems that the user has access to
    solarSystems = db.getUserSolarSystems(data.userID)
    #creating the array to be passed into the table
    solarSystemsFormat = [["Name", "Objects", "Last saved"]]
    #format: name, objectCount, date, solarsystemID
    for i in range(0, len(solarSystems)):
        solarSystemsFormat.append([str(solarSystems[i][1]), str(db.getNumberOfObjects(solarSystems[i][0])), 
                                   str(solarSystems[i][2].strftime("%d/%m/%y")), int(solarSystems[i][0])])
    #creating and showing the table
    loadTable = ui.table(data = solarSystemsFormat, xpos = WIDTH / 2 - 450, ypos = 200, width = 900, 
                         height = 400, textSize = 30, rowsPerPage = 4, selectButtons = True, 
                         buttonText = "Load", action = onLoadTableResult)
    loadTable.show()
    #finally, we update the menuStages 
    data.menuStages.append("Load")

def createClicked():
    ui.hideAll()
    buttonBack.show()
    labelTitle.show()
    buttonCreateSystem.show()
    if data.userID != 1: #if the user is not a guest, allow them to pick a name
        inputSystemName.show()
        labelTitle.setText("Choose the name")
    else:   #otherwise, don't allow them to pick a name
        labelRegisterError.setText("Warning: You are logged in as a Guest. Your solar system will not be saved.")
        labelRegisterError.show()
        labelTitle.setText("Guest create")
    data.menuStages.append("Create")

def createSystemClicked():
    #hide the user interface
    ui.hideAll()
    #create objectData for guests 
    data.objectData = []
    data.objectData.append([0, data.solarSystemID, 0, 0, "Sun", 0, 0, 0, 0, 1.989 * (10 ** 30), 255, 255, 0])
    if data.userID != 1:
        #if the user is not a guest, we upload the new solar system to the database, with the name
        createSolarSystem(inputSystemName.getInput())
        #to get the ID of the new solar system, we call getNewSolarSystem
        solarSystemID = db.getNewSolarSystem()
        data.solarSystemID = int(solarSystemID[0][0])

        data.objectData = []
        data.objectData.append([0, data.solarSystemID, 0, 0, "Sun", 0, 0, 0, 0, 1.989 * (10 ** 30), 255, 255, 0])
    
        #then we update the database with the new objectData
        db.updateObjectsDatabase(data.objectData)
    data.objectCount = 1
    data.systemSize = 1000000000000
    simulationSetup()

def mainMenu():
    ui.hideAll()
    buttonQuit.show()
    buttonRegister.show()
    buttonLogin.show()
    buttonGuest.show()
    labelTitle.show()
    labelTitle.setText("SolarSystemMaker")
    data.menuStages.append("MainMenu")

def onLoadTableResult(ID):
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
    data.screenConversion = data.systemSize / WIDTH 
    #calculates the offset values (as the star is at 
    #the center but 0,0 on the screen is top left)
    data.screenOffsetX = data.systemSize / 2
    data.screenOffsetY = (data.systemSize / 2) * (HEIGHT / WIDTH)
    ob.updateScreen(data.screenConversion, data.screenOffsetX, data.screenOffsetY)

    #load the objects from the database and create the systemObjects
    if data.userID != 1:
        data.objectData = db.loadObjects(data.solarSystemID)
    createSystemObjects()
    data.simulation = True

    ## Here we will update the user interface with all the relevant elements
    buttonTogglePlaceMode.show()
    buttonNewPlanet.show()
    sliderSimulationSpeed.show()
    labelSimulationSpeed.show()
    labelSimulationTime.show()
    buttonToggleLabels.show()
    sliderZoom.show()
    labelZoom.show()
    buttonSimulationExit.show()

    ## Planet labels will also be set up here

    #begin the tickClock in preparation for simulation
    data.tickClock.tick()
    data.timeSinceLastTick = 0

    data.ghost_planet = ghostPlanet(10, (128, 128, 128))

    if data.userID != 1:
        buttonSimulationSave.show()

    buttonLessons.show()

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
    labelUpdates.setText("Saving...")
    labelUpdates.show()
    labelUpdates.draw()
    pygame.display.update()
    data.objectData = createObjectData()
    db.updateObjectsDatabase(data.objectData)
    db.updateSolarSystem(datetime.date.today().strftime("%d-%b-%y").upper(), data.objectCount, data.solarSystemID, data.simDate)
    data.objectData = []
    labelUpdates.hide()
    simulationSaveSetup()

    pygame.display.update()

def simulationExitClicked():
    windowSimulationExit.show()

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

def simulationExitCancelled():
    windowSimulationExit.hide()

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
        labelObjectDistance.show()
    
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
    labelObjectDistance.hide()
    labelObjectVelocity.hide()

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
    
    labelObjectDistance.hide()
    labelObjectVelocity.hide()
    
def onObjectClicked(obj):
    data.selectedObject = obj
    windowPlanetInfo.show()

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
    labelPlanetVelocity.setText("Velocity: " + f"{round(velocity):,d}" + " m/s")
    labelPlanetName.setText(data.selectedObject.name)
    #if the object is not the sun (i.e it is orbiting something)
    if data.selectedObject.solarSystemObjectID != 0:
        #update the orbing text and thedistance text
        labelPlanetParent.setText("Orbiting: " + str(data.selectedObject.parent.name))
        labelPlanetDistance.setText("Distance to " + str(data.selectedObject.parent.name) 
                                    + ": " + f"{round(distance / 1000):,d}" + " km")
    #otherwise, it is orbiting nothing
    else:
        labelPlanetParent.setText("Orbiting: None")
        labelPlanetDistance.setText("")

    sliderPlanetRed.setValue(data.selectedObject.red)
    sliderPlanetGreen.setValue(data.selectedObject.green)
    sliderPlanetBlue.setValue(data.selectedObject.blue)
    #inputPlanetName.defaultText = selectedObject.name

def sliderZoomMoved():
    #set system size logarithmically
    data.systemSize = 10**10 * 10**(4*(1-sliderZoom.getValue())) 
    screenConversion = data.systemSize / WIDTH  # calculates the scale multiplier
    screenOffsetX = data.systemSize / 2
    screenOffsetY = (data.systemSize / 2) * (HEIGHT / WIDTH)
    #update screen
    ob.updateScreen(screenConversion, screenOffsetX, screenOffsetY)

def sliderSimulationSpeedMoved():
    data.simulationSpeed = 10**sliderSimulationSpeed.getValue()

def planetColourChanged():
    data.selectedObject.setColour(int(sliderPlanetRed.getValue()), 
                             int(sliderPlanetGreen.getValue()), 
                             int(sliderPlanetBlue.getValue()))

#update the planet labels' names and coordinates.
def updateLabels():
    labelSimulationSpeed.setText("Simulation rate:\n" + getSimSpeedString(data.simulationSpeed))
    labelSimulationTime.setText("Date / Time:\n" + data.simDate.strftime("%d/%m/%Y, %H:%M:%S"))
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
    labelUpdates.setText("Loading...")
    labelUpdates.show()
    labelUpdates.draw()
    #force a display update so that the text is drawn
    pygame.display.update()
    Lessons = db.loadLessons()
    lessonsFormat = [["Name", "Description"]]
    #create the array of lesson data
    for i in range(0, len(Lessons)):
        lessonsFormat.append([str(Lessons[i][1]), str(Lessons[i][2]), int(Lessons[i][0])])
    #create the table
    loadTable = ui.table(data = lessonsFormat, xpos = 50, ypos = 110, 
                        width = windowLessonsInfo.width - 100, height = 350, textSize = 30, 
                        rowsPerPage = 4, selectButtons = True, buttonText = "Load", 
                        action = onLessonsTableResult, window = windowLessonsInfo)
    windowLessonsInfo.show()
    labelLessonsInfoTitle.show()
    labelUpdates.hide()

def onLessonsTableResult(ID):
    data.lessonStage = 0
    data.lessonID = ID
    data.objectData = []
    #load the array of lessons
    data.currentLesson = db.loadLessonStages(data.lessonID)
    #hide the window
    windowLessonsInfo.hide()
    labelLessonsInfoTitle.hide()
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
            windowLessonText.hide()
            data.currentLesson = None
        else: #otherwise, setup the new lesson stage
            labelLessonText.setText(str(data.currentLesson[data.lessonStage][2]))
            windowLessonText.height = labelLessonText.height + 20
            windowLessonText.show()
            data.currentAction = data.currentLesson[data.lessonStage][3]
        
def toggleLabelsClicked():
    if buttonToggleLabels.state == 1:
        for i in data.planetLabels:
            i.show()
    else:
        for i in data.planetLabels:
            i.hide() 

pygame.init()
db = databaseHandler.database()

WIDTH = 1280
HEIGHT = 720

#creating a pygame screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SolarSystemMaker v1.3 Alpha")

#creating a listener object
listener = eventListener.Listener()

#initialising userInterface and objectHandler
ui.init(SCREEN, listener.uiListeners)
ob.init(SCREEN, listener.objectListeners, onObjectClicked)

windowPlanetInfo = ui.window(text="", colour = (38, 38, 38), 
                            xpos = WIDTH - 480, ypos = 0, width=480, 
                            height=HEIGHT, outlineColour=(127, 127, 127))

labelPlanetName = ui.label(text="", xAlign="centre", window = windowPlanetInfo, ypos = 30, xpos = 240, textBold=True, textSize = 32)
labelPlanetVelocity = ui.label(text="", xAlign="left", window = windowPlanetInfo, ypos = 130, xpos = 10, textBold=True, textSize = 20)
labelPlanetDistance = ui.label(text="", xAlign="left", window = windowPlanetInfo, ypos = 100, xpos = 10, textBold=True, textSize = 20)
labelPlanetParent = ui.label(text="", xAlign="left", window = windowPlanetInfo, ypos = 70, xpos = 10, textBold=True, textSize = 20)


buttonQuit = ui.actionButton(text="Quit", xpos=150, ypos=65, action=quitClicked, textBold=True, xMargin=60, textSize=32, outline=2, yMargin=2)
buttonRegister = ui.actionButton(text="Register", xpos=WIDTH/2, ypos=HEIGHT/2-85, action=registerClicked, textBold=True, width=160, textSize=32, outline=2)
buttonLogin = ui.actionButton(text="Login", xpos=WIDTH/2, ypos=HEIGHT/2, action=loginClicked, textBold=True, width=160, textSize=32, outline=2)
buttonGuest = ui.actionButton(text="Guest", xpos=WIDTH/2, ypos=HEIGHT/2+85, action=guestClicked, textBold=True, width=160, textSize=32, outline=2)
buttonBack = ui.actionButton(text="Back", xpos=150, ypos=65, action=backClicked, textBold=True, xMargin=60, textSize=32, outline=2, yMargin=2)

buttonSimulationSave = ui.actionButton(text="Save", xpos = 48, xMargin = 15, ypos = 20, 
                                       action = simulationSaveClicked, textBold = True, yMargin = 8, outline = 1, textSize = 28)
buttonLessons = ui.actionButton(text="Lessons", xpos = 172, xMargin = 15, ypos = 20, 
                                action = lessonsClicked, textBold = True, yMargin = 8, outline = 1, textSize = 28)
buttonSimulationExit = ui.actionButton(text="Exit", xpos = 295, xMargin = 15, 
                                       ypos = 20, action = simulationExitClicked, 
                                       textBold = True, yMargin = 8, outline = 1, textSize = 28)

buttonNewPlanet = ui.actionButton(text="New object", xpos = 600, xMargin = 10, ypos = 80, 
                                    action = newPlanetClicked, textBold = True, 
                                    yMargin = 2, outline = 3, textSize = 32)
buttonTogglePlaceMode = ui.toggleButton(text1="Quick place", text2="Custom place", xpos = 355, 
                                        xMargin = 10, ypos = 80, action = togglePlaceModeClicked, 
                                        textBold = True, yMargin = 2, outline = 3, textSize = 32,
                                        colour1=(91, 155, 213), colour2=(237, 125, 49))
buttonToggleLabels = ui.toggleButton(text1="Labels on", text2="Labels off", xpos = 120, 
                                        xMargin = 10, ypos = 80, action = toggleLabelsClicked, 
                                        textBold = True, yMargin = 2, outline = 3, textSize = 32,
                                        colour1=(91, 155, 213), colour2=(237, 125, 49))

sliderZoom = ui.slider(xpos = 400, ypos = HEIGHT - 40, leftValue=0, rightValue=1, action=sliderZoomMoved, defaultValue=0.5, 
                       lineColour=(166, 166, 166), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200)

sliderSimulationSpeed = ui.slider(xpos = 100, ypos = HEIGHT - 40, leftValue=0, rightValue=8, action=sliderSimulationSpeedMoved, defaultValue=0, 
                       lineColour=(166, 166, 166), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200)

labelSimulationTime = ui.multiLinelabel(xpos = 800, xAlign = "centre", yAlign = "centre", textBold=False, ypos = HEIGHT - 40, textSize = 22, maxWidth = 300)
labelSimulationSpeed = ui.multiLinelabel(xpos = 200, xAlign = "centre", textBold=False, ypos = sliderSimulationSpeed.ypos - 50, textSize = 22, maxWidth = 300)
labelZoom = ui.multiLinelabel(xpos = sliderZoom.xpos + sliderZoom.width / 2, xAlign = "centre", textBold=False, ypos = sliderZoom.ypos - 30, textSize = 22, maxWidth = 300, text = "Zoom")

sliderPlanetRed = ui.slider(xpos = 20, ypos = 170, leftValue=0, rightValue=255, action=planetColourChanged, defaultValue=0.5, 
                       lineColour=(255, 0, 0), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200, window=windowPlanetInfo)
sliderPlanetGreen = ui.slider(xpos = 20, ypos = 210, leftValue=0, rightValue=255, action=planetColourChanged, defaultValue=0.5, 
                       lineColour=(0, 176, 80), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200, window=windowPlanetInfo)
sliderPlanetBlue = ui.slider(xpos = 20, ypos = 250, leftValue=0, rightValue=255, action=planetColourChanged, defaultValue=0.5, 
                       lineColour=(0, 112, 192), btnColour=(91, 155, 213), height=30, btnWidth=8, width = 200, window=windowPlanetInfo)


labelUpdates = ui.label(text="", xpos=WIDTH/2, ypos=HEIGHT/2 + 100, textSize=32, textBold=True)
labelTitle = ui.label(text="SolarSystemMaker v1.1 Alpha", xpos=WIDTH/2, ypos=140, textSize=48)
labelRegisterError = ui.label(text="", xpos=WIDTH/2, ypos=HEIGHT/2+230, textSize=24, textBold=True)

inputRegisterUsername = ui.inputBox(text="Enter username...", xpos=WIDTH/2, ypos=HEIGHT/2-70, textItalics=True, textBold=True, 
                                    asterisks=False, textSize=24, outline=2)
inputRegisterPassword1 = ui.inputBox(text="Enter password...", xpos=WIDTH/2, ypos=HEIGHT/2, textItalics=True, textBold=True, 
                                     asterisks=True, textSize=24, outline=2)
inputRegisterPassword2 = ui.inputBox(text="Enter password again...", xpos=WIDTH/2, ypos=HEIGHT/2+70, textItalics=True, textBold=True, 
                                     asterisks=True, textSize=24, outline=2)

inputLoginUsername = ui.inputBox(text="Enter username...", xpos=WIDTH/2, ypos=HEIGHT/2-70, textItalics=True, textBold=True, 
                                    asterisks=False, textSize=24, outline=2)
inputLoginPassword = ui.inputBox(text="Enter password...", xpos=WIDTH/2, ypos=HEIGHT/2, textItalics=True, textBold=True, 
                                     asterisks=True, textSize=24, outline=2)

inputSystemName = ui.inputBox(text="Enter the name...", xpos=WIDTH/2, ypos=HEIGHT/2-70, textItalics=True, textBold=True, 
                              asterisks=False, textSize=24, outline=2, inactiveColour=(255,255,255))

inputPlanetName = ui.inputBox(text="Enter the name...", xpos = 170, ypos=320, textItalics=True, textBold=True, 
                              asterisks=False, textSize=24, outline=2, window=windowPlanetInfo, width = 300)
inputPlanetMass = ui.inputBox(text="Enter the mass...", xpos = 170, ypos=360, textItalics=True, textBold=True, 
                              asterisks=False, textSize=24, outline=2, window=windowPlanetInfo, width = 300)

buttonCreateSystem = ui.actionButton(text="Create!", xpos=WIDTH/2, ypos=HEIGHT/2 + 40, action=createSystemClicked, textBold=True, 
                                      xMargin=60, textSize=32, outline=2, yMargin=2)

buttonCreate = ui.actionButton(text="Create a solar system", xpos=WIDTH/2, ypos=HEIGHT/2 + 40, action=createClicked, textBold=True, 
                                      width = 300, textSize=20, outline=2, yMargin=3)
buttonLoad = ui.actionButton(text="Load a solar system", xpos=WIDTH/2, ypos=HEIGHT/2-40, action=loadClicked, textBold=True, 
                                      width = 300, textSize=20, outline=2, yMargin=3)


buttonCreateAccount = ui.actionButton(text="Register", xpos=WIDTH/2, ypos=HEIGHT/2+140, action=createAccountClicked, textBold=True, 
                                      xMargin=60, textSize=32, outline=2, yMargin=2)
buttonLoginAccount = ui.actionButton(text="Login", xpos=WIDTH/2, ypos=HEIGHT/2+70, action=loginAccountClicked, textBold=True, 
                                      xMargin=60, textSize=32, outline=2, yMargin=2)

labelObjectDistance = ui.label(text = "")
labelObjectVelocity = ui.label(text = "")

windowLessonsInfo = ui.window(text="", colour = (38, 38, 38), xpos = 100, 
                              ypos = 100, width=WIDTH - 200, height=HEIGHT - 200, 
                              drawPriority = "Low", outlineColour=(127, 127, 127))
labelLessonsInfoTitle = ui.label(text="Start a lesson", xpos=WIDTH/2, ypos=windowLessonsInfo.ypos + 50, textSize=48)
windowLessonText = ui.window(text = "", colour = (38, 38, 38), xpos = 50, 
                            ypos = 120, width=400, height=400, drawPriority = "Low", 
                            outlineColour = (127, 127, 127))
labelLessonText = ui.multiLinelabel(text = "", 
                               xpos = 10, ypos = 10, maxWidth = windowLessonText.width - 20, 
                               xAlign = "left", yAlign = "top", window=windowLessonText, textSize=24)

windowSimulationExit = ui.window(text = "", colour = (38, 38, 38), 
                                xpos = WIDTH / 2 - 200, ypos = HEIGHT / 2 - 50, 
                                width = 400, height = 100, drawPriority = "Low", 
                                outlineColour = (127, 127, 127))

buttonConfirmExit = ui.actionButton(text="Exit without saving", xpos = 10, ypos = 75, 
                                    action=simulationExitConfirmed, textBold=True, 
                                    textSize=20, outline=2, yMargin=3, 
                                    window = windowSimulationExit, xAlign = "left")

buttonCancelExit = ui.actionButton(text="Cancel", xpos = windowSimulationExit.width - 10, 
                                   ypos = 75, action=simulationExitCancelled, textBold=True, 
                                   textSize=20, outline=2, yMargin=3, 
                                   window = windowSimulationExit, xAlign = "right")

labelConfirmExit = ui.multiLinelabel(text = "Are you sure you want to exit?\nChanges may not be saved.", 
                                    xpos = windowSimulationExit.width / 2, ypos = 10, 
                                    textBold=True, maxWidth = windowSimulationExit.width,
                                    xAlign = "centre", yAlign = "top", window=windowSimulationExit)

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
                    labelObjectDistance.hide()
                else: #if we are using custom place
                    if data.choosingNewObjectVelocity == False:
                        data.choosingNewObjectVelocity = True
                        labelObjectVelocity.show()
                    else:
                        createNewPlanetCustom()
                        labelObjectVelocity.hide()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                checkLessonAction("spacePressed")
            #if the object window is active, close it when escape pressed
            if event.key == pygame.K_ESCAPE:
                if data.selectedObject:
                    data.selectedObject = None
                    windowPlanetInfo.hide()
            if event.key == pygame.K_RETURN:
                #if the name box is active, update the name
                if inputPlanetName.active:
                    data.selectedObject.name = inputPlanetName.getInput()
                    updatePlanetInfo()
                #if the mass box is active update the mass
                if inputPlanetMass.active:
                    #this try / except handles the case where the user does not enter an integer
                    try:
                        data.selectedObject.mass = int(inputPlanetMass.getInput())
                        updatePlanetInfo()
                    except:
                        pass
        
        listener.pollUI(event) #use event listener to poll the elements
        listener.pollObjects(event)

    #if a frame's period of time has passed, we draw everything + update display
    if timeSinceLastFrame > frame_every_ms:
        SCREEN.fill((0, 0, 0)) #fill the screen black
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
            pygame.draw.circle(SCREEN, (int(sliderPlanetRed.getValue()), int(sliderPlanetGreen.getValue()), int(sliderPlanetBlue.getValue())), (sliderPlanetGreen.xpos + 280, int(sliderPlanetGreen.ypos + sliderPlanetGreen.height / 2)), 40)
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