import pygame
from math import ceil
pygame.init()

def init(surface, arrayListeners):
    global screenSurface
    screenSurface = surface
    global uiListeners
    uiListeners = arrayListeners

def hideAll():
    for i in uiListeners:
        i.hide()

defaultColour = (255, 255, 255)
defaultInputColour = (64, 64, 64)
defaultFont = "courier"
defaultTextSize = 18
defaultTextColour = (255, 255, 255)
specialKeys = [pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE]

class element():
    def __init__(self, xpos, ypos, text, font, width, height, event, window, textColour, textBold, textItalics, drawPriority):
        if drawPriority == "Low":
            uiListeners.append(self)
        elif drawPriority == "High":
            uiListeners.insert(0, self)
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.text = text
        self.font = font 
        self.showing = False
        self.window = window
        self.event = event
        self.textColour = textColour
        self.textBold = textBold
        self.textItalics = textItalics
        #adding to a window
        if self.window != None:
            #updating coordinates 
            self.xpos += self.window.xpos
            self.ypos += self.window.ypos
            self.window.add(self)


    def show(self):
        self.showing = True

    def hide(self):
        self.showing = False

class actionButton(element):
    #constructor
    def __init__(self, font = defaultFont, xpos = 0, ypos = 0, width = None, height = None, colour = defaultColour, text = "Button", 
                textSize = defaultTextSize, outline = 1, xMargin = 0, yMargin = 0, action = None, window = None, 
                textColour = defaultTextColour, textBold = False, textItalics = False, ID = False, xAlign = "centre", yAlign = "centre", drawPriority = "Low"):
        super().__init__(xpos, ypos, text, font, width, height, self.detectClick, window, textColour, textBold, textItalics, drawPriority)
        self.id = ID
        self.action = action
        if self.action == "getID":
            self.action = self.getID
        self.event = self.detectClick
        self.fontObject = pygame.font.Font(pygame.font.match_font(font, self.textBold, self.textItalics), textSize)
        self.colour = colour
        self.outline = outline
        self.xMargin = xMargin
        self.yMargin = yMargin
        self.xAlign = xAlign
        self.yAlign = yAlign
        self.textSurface = self.fontObject.render(self.text, True, textColour)
        #setting the width and margins
        if self.width == None:
            self.width = self.textSurface.get_width() + self.xMargin * 2
        if self.height == None:
            self.height = self.textSurface.get_height() + self.yMargin * 2
        self.buttonRect = pygame.Rect(self.xpos - self.outline / 2, self.ypos - self.outline, self.width + self.outline, self.height + self.outline)
        self.textRect = self.textSurface.get_rect()
        #alignment of button
        if self.xAlign == "left":
            self.textRect.left = self.xpos
            self.buttonRect.left = self.xpos
        if self.xAlign == "centre": 
            self.textRect.left = self.xpos - self.textRect.width / 2
            self.buttonRect.left = self.xpos - self.buttonRect.width / 2
        if self.xAlign == "right":
            self.textRect.right = self.xpos
            self.buttonRect.right = self.xpos
        if self.yAlign == "top":
            self.textRect.top = self.ypos
            self.buttonRect.top = self.ypos
        if self.yAlign == "centre":
            self.textRect.top = self.ypos - self.textRect.height / 2
            self.buttonRect.top = self.ypos - self.buttonRect.height / 2
        if self.yAlign == "bottom":
            self.textRect.bottom = self.ypos
            self.buttonRect.bottom = self.ypos

    #draw function called every frame
    def draw(self):
        if self.showing:
            global screenSurface
            #self.textRect.center = self.buttonRect.center
            #self.buttonRect.center = (self.xpos, self.ypos)
            screenSurface.blit(self.textSurface, self.textRect)
            pygame.draw.rect(screenSurface, self.colour, self.buttonRect, self.outline)

    #event function called every frame
    def detectClick(self, event):
        if self.showing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttonRect.collidepoint(event.pos):
                    if self.action != None:
                        return self.action()
    
    def getID(self):
        return self.id

class toggleButton(element):
    #constructor
    def __init__(self, font = defaultFont, xpos = 0, ypos = 0, width = None, height = None, colour1 = defaultColour, colour2 = defaultColour, text1 = "Button 1", text2 = "Button 2",
                textSize = defaultTextSize, outline = 1, xMargin = 0, yMargin = 0, action = None, window = None, 
                textColour = defaultTextColour, textBold = False, textItalics = False, ID = False, drawPriority = "Low"):
        super().__init__(xpos, ypos, text1, font, width, height, self.detectClick, window, textColour, textBold, textItalics, drawPriority)
        self.state = 1
        self.id = ID
        self.text2 = text2
        self.text1 = text1
        self.action = action
        self.event = self.detectClick
        self.fontObject = pygame.font.Font(pygame.font.match_font(font, self.textBold, self.textItalics), textSize)
        self.colour1 = colour1
        self.colour2 = colour2
        self.colour = self.colour1
        self.outline = outline
        self.xMargin = xMargin
        self.yMargin = yMargin
        self.textSurface = self.fontObject.render(self.text, True, textColour)
        #setting the width and margins
        if self.width == None:
            self.width = self.textSurface.get_width() + self.xMargin * 2
        if self.height == None:
            self.height = self.textSurface.get_height() + self.yMargin * 2
        self.buttonRect = pygame.Rect(self.xpos - self.outline / 2, self.ypos - self.outline, self.width + self.outline, self.height + self.outline)
        self.textRect = self.textSurface.get_rect()

    #draw function called every frame
    def draw(self):
        if self.showing:
            global screenSurface
            self.buttonRect.center = (self.xpos, self.ypos)
            self.textRect.center = self.buttonRect.center
            screenSurface.blit(self.textSurface, self.textRect)
            pygame.draw.rect(screenSurface, self.colour, self.buttonRect, self.outline)

    #event function called every frame
    def detectClick(self, event):
        if self.showing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttonRect.collidepoint(event.pos):
                    if self.state == 1:
                        self.state = 2
                        self.text = self.text2
                        self.colour = self.colour2
                    else:
                        self.state = 1
                        self.text = self.text1
                        self.colour = self.colour1
                    self.textSurface = self.fontObject.render(self.text, True, self.textColour)
                    #setting the width and margins
                    if self.width == None:
                        self.width = self.textSurface.get_width() + self.xMargin * 2
                    if self.height == None:
                        self.height = self.textSurface.get_height() + self.yMargin * 2
                    self.buttonRect = pygame.Rect(self.xpos - self.outline / 2, self.ypos - self.outline, self.width + self.outline, self.height + self.outline)
                    self.textRect = self.textSurface.get_rect()
                    if self.action != None:
                        return self.action()

class label(element):
    #constructor
    def __init__(self, font = defaultFont, xpos = 0, ypos = 0, colour = defaultColour, 
                 text = "Label", textSize = defaultTextSize, window = None, textColour = defaultTextColour, textBold = False, textItalics = False,
                 xAlign = "centre", yAlign = "centre", drawPriority = "Low"):
        super().__init__(xpos, ypos, text, font, None, None, None, window, textColour, textBold, textItalics, drawPriority)
        self.fontObject = pygame.font.Font(pygame.font.match_font(font, self.textBold, self.textItalics), textSize)
        self.colour = colour
        #width, surfaces and rects
        self.xAlign = xAlign
        self.yAlign = yAlign
        self.setText(text)
 
    #draw method
    def draw(self):
        if self.showing:
            global screenSurface
            screenSurface.blit(self.textSurface, self.textRect)

    def setText(self, text):
        self.text = text
        self.textSurface = self.fontObject.render(self.text, True, self.colour)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (self.xpos, self.ypos)
        #set the alignment
        if self.xAlign == "left":
            self.textRect.left = self.xpos
        if self.xAlign == "centre": 
            self.textRect.left = self.xpos - self.textRect.width / 2
        if self.xAlign == "right":
            self.textRect.right = self.xpos
        if self.yAlign == "top":
            self.textRect.top = self.ypos
        if self.yAlign == "centre":
            self.textRect.top = self.ypos - self.textRect.height / 2
        if self.yAlign == "bottom":
            self.textRect.bottom = self.ypos
    
class multiLinelabel(element):
    #constructor
    def __init__(self, font = defaultFont, xpos = 0, ypos = 0, colour = defaultColour, 
                 text = "Label", textSize = defaultTextSize, window = None, textColour = defaultTextColour, textBold = False, textItalics = False,
                 xAlign = "centre", yAlign = "centre", drawPriority = "Low", maxWidth = 200):
        super().__init__(xpos, ypos, text, font, None, None, None, window, textColour, textBold, textItalics, drawPriority)
        self.fontObject = pygame.font.Font(pygame.font.match_font(font, self.textBold, self.textItalics), textSize)
        self.colour = colour
        #width, surfaces and rects
        self.xAlign = xAlign
        self.yAlign = yAlign
        self.textSize = textSize
        self.maxWidth = maxWidth
        self.setText(text)
        self.heigth = None

    #draw method
    def draw(self):
        if self.showing:
            global screenSurface
            screenSurface.blit(self.drawSurface, self.textRect)

    def setText(self, text):
        self.text = text
        self.drawSurface = pygame.Surface((self.maxWidth, 1000))
        self.drawSurface.set_colorkey((0, 0, 0))
        if self.xAlign == "centre":
            self.textRect = (self.xpos - self.maxWidth / 2, self.ypos, self.maxWidth, 1000)
        else:
            self.textRect = (self.xpos, self.ypos, self.maxWidth, 1000)
        words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
        space = self.fontObject.size(' ')[0]  # The width of a space.
        x = 0
        y = 0
        for line in words:
            line_surface = pygame.Surface((self.maxWidth, self.textSize))
            lineText = ""
            for word in line:
                word_surface = self.fontObject.render(word, 0, self.textColour)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.maxWidth:
                    line_surface = self.fontObject.render(lineText, 0, self.textColour)
                    if self.xAlign == "centre":
                        self.drawSurface.blit(line_surface, (self.maxWidth / 2 - line_surface.get_width() / 2, y))
                    else:
                        self.drawSurface.blit(line_surface, (0, y))
                    x = 0  # Reset the x.
                    y += word_height  # Start on new row.
                    lineText = ""
                    line_surface = pygame.Surface((self.maxWidth, self.textSize))
                    line_surface.blit(word_surface, (x, 0))
                    lineText += word
                    lineText += " "
                    x += word_width + space
                else:
                    line_surface.blit(word_surface, (x, 0))
                    lineText += word
                    lineText += " "
                    x += word_width + space
            line_surface = self.fontObject.render(lineText, 0, self.textColour)
            if self.xAlign == "centre":
                self.drawSurface.blit(line_surface, (self.maxWidth / 2 - line_surface.get_width() / 2, y))
            else:
                self.drawSurface.blit(line_surface, (0, y))
            lineText = word
            lineText += " "
            x = 0  # Reset the x.
            y += word_height  # Start on new row.
        self.height = y

class inputBox(element):
    def __init__(self, font = defaultFont, xpos = 0, ypos = 0, width = None, height = None, inactiveColour = defaultInputColour, 
                 text = "Input Box", textSize = defaultTextSize, window = None, textColour = defaultTextColour, 
                 textBold = False, textItalics = True, asterisks = False, outline = 1, activeColour = defaultColour, drawPriority = "Low"):
        #constructor for the input box
        super().__init__(xpos, ypos, text, font, width, height, None, window, textColour, textBold, textItalics, drawPriority)
        self.fontObject = pygame.font.Font(pygame.font.match_font(font, self.textBold, self.textItalics), textSize)
        self.inactiveColour = inactiveColour
        self.activeColour = activeColour
        self.inputText = "" #user input text set to empty string
        self.defaultText = str(text) #the default text to be displayed
        self.text = self.defaultText
        self.showing = False
        self.event = self.update
        self.textSurface = self.fontObject.render(self.defaultText, True, self.textColour)
        if self.width == None:
            self.width = self.textSurface.get_width()
        if self.height == None:
            self.height = self.textSurface.get_height()
        self.boxRect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
        self.textRect = self.boxRect
        self.displayText = self.text #the text to be displayed, may be different 
        self.asterisks = asterisks
        self.active = False
        self.outline = outline

    def draw(self):
        place = 0
        if self.showing:
            global screenSurface
            if self.active:
                self.text = self.inputText
                if self.asterisks: # if its obfuscated, replace the text with asterisks
                    self.text = ""
                    for i in range(len(self.inputText)):
                        self.text += "*"
            else:
                if self.inputText == "":
                    self.text = self.defaultText
            # draw new button frame
            self.textSurface = self.fontObject.render(self.text, False, self.textColour)
            self.textRect = self.textSurface.get_rect()
            self.textRect.center = (self.xpos, self.ypos)
            self.boxRect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
            self.boxRect.center = (self.xpos, self.ypos)
            if self.textRect.width > self.width: # we must deal with the rendering differently if the text does not fit the box
                self.textRect.topright = ((self.xpos + self.width / 2), self.ypos)
                self.textRect.topleft = (self.xpos - self.width / 2, self.ypos - self.boxRect.h / 2)
                self.found = False
                for i in range(0, len(self.inputText)): # test different lengths of text until one fits the screen
                    self.test = self.fontObject.render(self.inputText[len(self.inputText) - i:], False, self.textColour)
                    self.testRect = self.test.get_rect()
                    if self.testRect.width > self.width and self.found == False:
                        place = i - 1
                        self.found = True 
                self.displayText = self.text[-place:]
            else: # if it does, just draw normally 
                self.textRect = self.textSurface.get_rect()
                self.textRect.topleft = (self.xpos - self.width / 2, self.ypos - self.boxRect.h / 2)
                self.displayText = self.text
            self.textSurface = self.fontObject.render(self.displayText, True, self.textColour)
            screenSurface.blit(self.textSurface, self.textRect)
            if self.active:
                pygame.draw.rect(screenSurface, self.activeColour, self.boxRect, self.outline)
            else:
                pygame.draw.rect(screenSurface, self.inactiveColour, self.boxRect, self.outline)


    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.detectClick(event)
        elif event.type == pygame.KEYDOWN: 
            self.typeInput(event)

    def detectClick(self, event):
        if self.showing:
            self.active = self.boxRect.collidepoint(event.pos)
                    
    def typeInput(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.inputText = self.inputText[:-1]
            else:
                if event.key not in specialKeys:
                    self.inputText += event.unicode

    def getInput(self):
        self.returnText = self.inputText
        self.inputText = ""
        if self.returnText == "":
            return False
        else:
            return (self.returnText)
    
    def show(self):
        self.showing = True
        self.active = False

class table(element):
    def __init__(self, font = defaultFont, xpos = 0, ypos = 0, width = None, height = None, colour = defaultColour, 
                 text = "Label", textSize = defaultTextSize, window = None, textColour = defaultTextColour, 
                 textBold = False, textItalics = False, data = [[]], rowsPerPage = 4, selectButtons = False, 
                 buttonText = "Select", action = None, drawPriority = "Low"):
        super().__init__(xpos, ypos, text, font, width, height, None, window, textColour, textBold, textItalics, drawPriority)
        self.action = action
        self.fontObject = pygame.font.Font(pygame.font.match_font(font, self.textBold, self.textItalics), textSize)
        self.colour = colour
        #width, surfaces and rects
        self.textSurface = self.fontObject.render(self.text, True, textColour)
        self.rect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
        self.rect.center = (self.xpos, self.ypos)
        self.textRect = self.textSurface.get_rect()
        self.rowsPerPage = rowsPerPage
        self.textSize = textSize
        self.data = data
        self.page = 0 #represents which page of the table 
        self.selectButtons = selectButtons
        #maxPage is the last page number
        self.maxPage = ceil((len(self.data) - 1) / (self.rowsPerPage) - 1)
        self.widthPerCell = self.width / len(self.data[0])
        self.heightPerCell = self.height / (self.rowsPerPage + 1)
        #the two buttons to go to the next page and the previous page 
        self.buttonNextPage = actionButton(xpos = self.xpos + self.width, ypos = self.ypos + height + self.heightPerCell / 2, text = "Next page", 
                                           action = self.nextPage, outline = 2, textSize=self.textSize, textBold=True, xAlign = "right")
        self.buttonPreviousPage = actionButton(xpos = self.xpos, ypos = self.ypos + height + self.heightPerCell / 2, text = "Previous page", 
                                               action = self.prevPage, outline = 2, textSize=self.textSize, textBold=True, xAlign = "left")
        self.labels = []
        #if buttons are on, we create a button for each line of data
        if selectButtons:
            self.event = self.getInput
            self.selectButtonList = []
            for row in range(1, len(self.data)):
                self.selectButtonList.append(actionButton(xpos = self.xpos + self.width, 
                                                          ypos = self.ypos + ((row - 1) % self.rowsPerPage + 1) * self.heightPerCell + self.heightPerCell / 2, 
                                                          action="getID", text=buttonText, ID=self.data[row][len(self.data[1]) - 1], 
                                                          textSize=self.textSize, textBold=True, xAlign = "right"))
        #update labels is called to create and show all of the labels relevant to the current page
        self.updateLabels()

    #when next page button is clicked
    def nextPage(self):
        self.page += 1
        self.updateLabels()

    #when previous page button is clicked
    def prevPage(self):
        self.page -= 1
        self.updateLabels()
    
    def updateLabels(self):
        #reset all the labels and buttons
        for i in self.labels:
            i.hide()
        for i in self.selectButtonList:
            i.hide()
        self.labels = []
        #update the next and previous page buttons
        if self.page == 0:
            self.buttonPreviousPage.hide()
        else:
            self.buttonPreviousPage.show()
        if self.page >= self.maxPage:
            self.buttonNextPage.hide()
        else:
            self.buttonNextPage.show()
        #no matter what page we are on, we create the column headers in self.data[0]
        for column in range(len(self.data[0])):
            self.labels.append(label(xpos = self.xpos + column * self.widthPerCell, 
                                     ypos = self.ypos + self.heightPerCell / 2, text = self.data[0][column], 
                                     textBold=True, textSize=self.textSize, xAlign = "left")) 
        xrow = 1
        for row in range(1 + (self.rowsPerPage) * self.page, 1 + (self.rowsPerPage) * self.page + (self.rowsPerPage)):
            if row >= len(self.data):
                break
            #if we have selectButtons on, the last row of Data is the IDs that we 
            #pass to the buttons and do not want displayed on the screen.
            if self.selectButtons:
                for column in range(len(self.data[row]) - 1):
                    self.labels.append(label(xpos = self.xpos + column * self.widthPerCell, 
                                             ypos = self.ypos + xrow * self.heightPerCell + self.heightPerCell / 2, text = self.data[row][column], 
                                             textSize = self.textSize, xAlign = "left"))
            else:
            #otherwise we create labels for all data
                for column in range(len(self.data[row])):
                    self.labels.append(label(xpos = self.xpos + column * self.widthPerCell, 
                                             ypos = self.ypos + xrow * self.heightPerCell + self.heightPerCell / 2, 
                                             text = self.data[row][column], textSize = self.textSize, xAlign = "left"))
            xrow += 1
        #show all the labels
        for i in self.labels: 
            i.show()
        #if each button belongs on the current page, show it
        start = self.page * self.rowsPerPage + 1 
        end = (self.page + 1) * self.rowsPerPage
        for i in range(start -1, end):
            #this exception handles the case that the last page is not filled
            try:
                self.selectButtonList[i].show()
            except:
                pass

    def getInput(self, event):
        #if the user clicks anywhere on the table, run its event function
        if event.type == pygame.MOUSEBUTTONDOWN:
            #event checks for every select button
            for i in self.selectButtonList:
                #returning ID of button
                result = i.detectClick(event)
                if result:
                    #run the table's action function
                    self.action(result)

    def show(self):
        self.showing = True
        for i in self.labels:
            i.show()
    
    def hide(self):
        self.showing = False
        if self.selectButtons:
            for i in self.selectButtonList:
                i.hide()
        self.buttonNextPage.hide()
        self.buttonPreviousPage.hide()
        for i in self.labels:
            i.hide()

    def draw(self):
        if self.showing:
            #draw all labels
            for i in self.labels:
                i.draw()
            self.buttonNextPage.draw()
            self.boxRect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
            #draw lines separating the rows
            for line in range(self.rowsPerPage + 2):
                pygame.draw.line(screenSurface, (255, 255, 255), (self.xpos, self.ypos + self.heightPerCell * (line)), 
                                 (self.xpos + self.width, self.ypos + self.heightPerCell * (line)))


class window(element):
    def __init__(self, font = defaultFont, xpos = 0, ypos = 0, width = 100, height = 100, colour = defaultColour, 
                 text = "Label", textSize = defaultTextSize, window = None, textColour = defaultTextColour, textBold = False, textItalics = False, drawPriority = "Low", outlineColour = (255, 255, 255), outlineWidth = 4):
        super().__init__(xpos, ypos, text, font, width, height, None, window, textColour, textBold, textItalics, drawPriority)
        self.childElements = []
        self.fontObject = pygame.font.Font(pygame.font.match_font(font, self.textBold, self.textItalics), textSize)
        self.colour = colour
        if self.text != None:
            self.textSurface = self.fontObject.render(self.text, True, textColour)
        #setting the width and margins
        self.textRect = self.textSurface.get_rect()
        self.outlineColour = outlineColour
        self.outlineWidth = outlineWidth

    #draw function called every frame
    def draw(self):
        if self.showing:
            self.WindowRect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
            self.OutlineRect = pygame.Rect(self.xpos, self.ypos, self.width + self.outlineWidth / 2, self.height + self.outlineWidth / 2)
            global screenSurface
            self.textRect.center = self.WindowRect.center
            screenSurface.blit(self.textSurface, self.textRect)
            pygame.draw.rect(screenSurface, self.colour, self.WindowRect)
            pygame.draw.rect(screenSurface, self.outlineColour, self.OutlineRect, self.outlineWidth)

    #function used by elements to add themselves to the window
    def add(self, obj):
        self.childElements.append(obj)

    #shows every element in the window
    def show(self):
        self.showing = True
        for obj in self.childElements:
            obj.show()

    #hides every element in the window
    def hide(self):
        self.showing = False
        for obj in self.childElements:
            obj.hide()

class slider(element):
    def __init__(self, xpos = 0, ypos = 0, width = 100, height = 20, window = None, lineColour = (255, 255, 255), 
                 btnColour = (255, 255, 255), btnWidth = 5, leftValue = 0, rightValue = 100, defaultValue = 0, action = None, drawPriority = "Low"):
        super().__init__(xpos, ypos, None, None, width, height, None, window, None, None, None, drawPriority)
        self.lineColour = lineColour
        self.btnColour = btnColour
        self.btnWidth = btnWidth
        self.leftValue = leftValue
        self.rightValue = rightValue
        self.defaultValue = defaultValue
        self.drawSurface = pygame.Surface((self.width + self.btnWidth, self.height))
        self.drawSurface.set_colorkey((0, 0, 0))
        pygame.draw.line(self.drawSurface, self.lineColour, (0, self.height / 2), (self.width - 1, self.height / 2), btnWidth)
        self.drawButtonSurface = pygame.Surface((self.btnWidth, self.height))
        self.drawButtonSurface.fill(btnColour)
        self.buttonXpos = self.xpos + self.defaultValue / (self.rightValue - self.leftValue) * self.width
        self.clicked = False
        self.event = self.detectClick 
        self.action = action
        self.value = self.defaultValue
    
    def setValue(self, value):
        self.value = value
        self.buttonXpos = self.xpos + self.value / (self.rightValue - self.leftValue) * self.width

    def detectClick(self, event):
        btnRect = self.drawButtonSurface.get_rect()
        btnRect.topleft = (self.buttonXpos, self.ypos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btnRect.collidepoint(event.pos):
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
        if self.clicked:
            mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
            mouse_pos[0] -= self.btnWidth / 2
            if mouse_pos[0] >= self.xpos and mouse_pos[0] <= self.xpos + self.width - self.btnWidth:
                self.buttonXpos = mouse_pos[0]
                self.value = self.leftValue + ((self.buttonXpos - self.xpos) / (self.width - self.btnWidth)) * (self.rightValue - self.leftValue)
                self.action()

    def getValue(self):
        return self.value

    def draw(self):
        if self.showing:
            global screenSurface
            screenSurface.blit(self.drawSurface, (self.xpos, self.ypos))
            screenSurface.blit(self.drawButtonSurface, (self.buttonXpos, self.ypos))

    