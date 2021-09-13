import pygame
from math import ceil
pygame.init()

def init(surface, listener):
    element.screenSurface = surface
    element.listener = listener

def hideAll():
    element.listener.hideUI()

defaultColour = (255, 255, 255)
defaultInputColour = (64, 64, 64)
defaultFont = "courier"
defaultTextSize = 18
defaultTextColour = (255, 255, 255)
#keys that should be ignored by input boxes
specialKeys = [pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE]

class element():
    def __init__(self, xpos, ypos, text, font, width, height, event, window, textColour, textBold, textItalics, drawPriority):
        self.listener.addUIElement(self, drawPriority)
        self.text = text
        self.font = font 
        self.showing = False
        self.window = window
        self.event = event
        self.textColour = textColour
        self.textBold = textBold
        self.textItalics = textItalics
        self.setRect(xpos, ypos, width, height)
        if self.window != None:
            self.window.add(self)

    def show(self):
        self.showing = True

    def hide(self):
        self.showing = False

    def setRect(self, x, y, w, h):
        self.width = w
        self.height = h
        self.xpos = x
        self.ypos = y
        if self.window != None:
            #updating coordinates 
            self.xpos += self.window.xpos
            self.ypos += self.window.ypos

class actionButton(element):
    def __init__(self, font = defaultFont, xpos = 0, ypos = 0, width = None, height = None, colour = defaultColour, text = "Button", 
                textSize = defaultTextSize, outline = 1, xMargin = 0, yMargin = 0, action = None, window = None, 
                textColour = defaultTextColour, textBold = False, textItalics = False, ID = False, xAlign = "centre", yAlign = "centre", drawPriority = "Low"):
        super().__init__(xpos, ypos, text, font, width, height, self.detectClick, window, textColour, textBold, textItalics, drawPriority)
        self.id = ID
        self.action = action
        # this is for tables - "select" buttons in tables must return their ID 
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
        self.updateRect(xpos, ypos, self.width, self.height)

    #draw function called every frame
    def draw(self):
        if self.showing:
            self.screenSurface.blit(self.textSurface, self.textRect)
            pygame.draw.rect(self.screenSurface, self.colour, self.buttonRect, self.outline)

    #event function called every frame
    def detectClick(self, event):
        if self.showing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttonRect.collidepoint(event.pos):
                    if self.action != None:
                        return self.action()

    def updateRect(self, xpos, ypos, width, height):
        self.setRect(xpos, ypos, width, height)
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
            self.buttonRect.center = (self.xpos, self.ypos)
            self.textRect.center = self.buttonRect.center
            self.screenSurface.blit(self.textSurface, self.textRect)
            pygame.draw.rect(self.screenSurface, self.colour, self.buttonRect, self.outline)

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
            self.screenSurface.blit(self.textSurface, self.textRect)

    def updateRect(self, xpos, ypos):
        self.setRect(xpos, ypos, None, None)
        self.setText(self.text)

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
        self.height = 0
        self.setText(text)
        self.yOffset = 0

    #draw method
    def draw(self):
        if self.showing:
            self.screenSurface.blit(self.drawSurface, self.textRect)

    def updateRect(self, xpos, ypos):
        self.setRect(xpos, ypos, None, None)
        self.setText(self.text)

    def setText(self, text):
        self.text = text
        self.drawSurface = pygame.Surface((self.maxWidth, 1000))
        self.drawSurface.set_colorkey((0, 0, 0))

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
                        self.drawSurface.blit(line_surface, (self.maxWidth / 2 - line_surface.get_width() / 2))
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
        if self.xAlign == "centre":
            self.textRect = pygame.Rect(self.xpos - self.maxWidth / 2, self.ypos, self.maxWidth, 1000)
        else:
            self.textRect = pygame.Rect(self.xpos, self.ypos, self.maxWidth, 1000)
        if self.yAlign == "centre":
            self.textRect.top -= self.height / 2
        

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
        self.asterisks = asterisks
        self.active = False
        self.outline = outline
        self.updateRect(xpos, ypos, self.width, self.height)
        self.displayText = self.text #the text to be displayed, may be different 

    def updateRect(self, xpos, ypos, width, height):
        self.setRect(xpos, ypos, width, height)
        self.textSurface = self.fontObject.render(self.defaultText, True, self.textColour)
        if self.width == None:
            self.width = self.textSurface.get_width()
        if self.height == None:
            self.height = self.textSurface.get_height()
        self.boxRect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
        self.textRect = self.boxRect

    def draw(self):
        place = 0
        if self.showing:
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
            self.screenSurface.blit(self.textSurface, self.textRect)
            if self.active:
                pygame.draw.rect(self.screenSurface, self.activeColour, self.boxRect, self.outline)
            else:
                pygame.draw.rect(self.screenSurface, self.inactiveColour, self.boxRect, self.outline)


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
        self.rowsPerPage = rowsPerPage
        self.textSize = textSize
        self.data = data
        self.page = 0 #represents which page of the table 
        self.selectButtonText = buttonText
        self.selectButtons = selectButtons
        self.selectButtonList = []
        self.labels = []
        #maxPage is the last page number
        self.maxPage = ceil((len(self.data) - 1) / (self.rowsPerPage) - 1)
        self.buttonNextPage = None
        self.buttonPreviousPage = None
        self.updateRect(xpos, ypos, width, height)

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
        for i in self.labels:
            self.listener.removeUIElement(i)
            del i 
        self.labels.clear()
        self.labels = []
        #update the next and previous page buttons
        self.updatePageButtons()
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
        #show all the labels if shwoign
        if self.showing:
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

    def updateRect(self, xpos, ypos, width, height):
        self.setRect(xpos, ypos, width, height)
        self.textSurface = self.fontObject.render(self.text, True, self.textColour)
        self.rect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
        self.rect.center = (self.xpos, self.ypos)
        self.textRect = self.textSurface.get_rect()
        self.widthPerCell = self.width / len(self.data[0])
        self.heightPerCell = self.height / (self.rowsPerPage + 1)
        #the two buttons to go to the next page and the previous page 
        if self.buttonNextPage:
            self.listener.removeUIElement(self.buttonNextPage)
        if self.buttonPreviousPage:
            self.listener.removeUIElement(self.buttonPreviousPage)
        self.buttonNextPage = actionButton(xpos = self.xpos + self.width, ypos = self.ypos + height + self.heightPerCell / 2, text = "Next page", 
                                           action = self.nextPage, outline = 2, textSize=self.textSize, textBold=True, xAlign = "right")
        self.buttonPreviousPage = actionButton(xpos = self.xpos, ypos = self.ypos + height + self.heightPerCell / 2, text = "Previous page", 
                                               action = self.prevPage, outline = 2, textSize=self.textSize, textBold=True, xAlign = "left")
        for i in self.selectButtonList:
            self.listener.removeUIElement(i)
            del i
        self.selectButtonList.clear()
        #if buttons are on, we create a button for each line of data
        if self.selectButtons:
            self.event = self.getInput
            self.selectButtonList = []
            for row in range(1, len(self.data)):
                self.selectButtonList.append(actionButton(xpos = self.xpos + self.width, 
                                                          ypos = self.ypos + ((row - 1) % self.rowsPerPage + 1) * self.heightPerCell + self.heightPerCell / 2, 
                                                          action="getID", text=self.selectButtonText, ID=self.data[row][len(self.data[1]) - 1], 
                                                          textSize=self.textSize, textBold=True, xAlign = "right"))
        self.updateLabels()

    def updatePageButtons(self):
        if self.showing:
            if self.page == 0:
                self.buttonPreviousPage.hide()
            else:
                self.buttonPreviousPage.show()
            if self.page >= self.maxPage:
                self.buttonNextPage.hide()
            else:
                self.buttonNextPage.show()

    def show(self):
        self.showing = True
        if self.selectButtons:
            for i in self.selectButtonList:
                i.show()
        self.updatePageButtons()
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
            #self.buttonNextPage.draw()
            self.boxRect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
            #draw lines separating the rows
            for line in range(self.rowsPerPage + 2):
                pygame.draw.line(self.screenSurface, (255, 255, 255), (self.xpos, self.ypos + self.heightPerCell * (line)), 
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
            self.textRect.center = self.WindowRect.center
            self.screenSurface.blit(self.textSurface, self.textRect)
            pygame.draw.rect(self.screenSurface, self.colour, self.WindowRect)
            pygame.draw.rect(self.screenSurface, self.outlineColour, self.OutlineRect, self.outlineWidth)

    #function used by elements to add themselves to the window
    def add(self, obj):
        self.childElements.append(obj)

    def updateRect(self, xpos, ypos, width, height):
        self.setRect(xpos, ypos, width, height)

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
                 btnColour = (255, 255, 255), btnWidth = 5, leftValue = 0, rightValue = 100, defaultValue = 0, action = None, 
                 xAlign = "centre", yAlign = "centre", drawPriority = "Low"):
        super().__init__(xpos, ypos, None, None, width, height, None, window, None, None, None, drawPriority)
        self.lineColour = lineColour
        self.btnColour = btnColour
        self.btnWidth = btnWidth
        self.leftValue = leftValue
        self.rightValue = rightValue
        self.defaultValue = defaultValue
        self.value = self.defaultValue
        self.clicked = False
        self.buttonXpos = self.xpos + self.defaultValue / (self.rightValue - self.leftValue) * self.width
        self.event = self.detectClick 
        self.action = action
        self.yAlign = yAlign
        self.xAlign = xAlign
        self.updateRect(xpos, ypos, width, height)
    
    def setValue(self, value):
        self.value = value
        if self.value < self.leftValue:
            self.value = self.leftValue
        if self.value > self.rightValue:
            self.value = self.rightValue
        self.buttonXpos = self.xpos - self.leftValue + self.value * (self.width - self.btnWidth) / (self.rightValue - self.leftValue)

    def detectClick(self, event):
        btnRect = self.drawButtonSurface.get_rect()
        btnRect.topleft = (self.buttonXpos, self.yActual)
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

    def updateRect(self, xpos, ypos, width, height):
        self.setRect(xpos, ypos, width, height)
        self.drawSurface = pygame.Surface((self.width + self.btnWidth, self.height))
        self.drawSurface.set_colorkey((0, 0, 0))
        pygame.draw.line(self.drawSurface, self.lineColour, (0, self.height / 2), (self.width - 1, self.height / 2), self.btnWidth)
        self.drawButtonSurface = pygame.Surface((self.btnWidth, self.height))
        self.drawButtonSurface.fill(self.btnColour)
        if self.yAlign == "centre":
            self.yActual = self.ypos - self.height / 2
        else:
            self.yActual = self.ypos

    def draw(self):
        if self.showing:
            self.screenSurface.blit(self.drawSurface, (self.xpos, self.yActual))
            self.screenSurface.blit(self.drawButtonSurface, (self.buttonXpos, self.yActual))

    