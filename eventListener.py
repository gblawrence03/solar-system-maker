class Listener:
    def __init__(self):
        self.uiListeners = []
        self.objectListeners = []

    def setObjects(self, objects):
        self.objectListeners = objects
    
    def pollUI(self, event): #function that checks for events in the UI elements
        for element in self.uiListeners:
            if element.event != None: 
                element.event(event)

    def pollObjects(self, event): #function that checks for events in the objects
        for element in self.objectListeners:
            if element.solarSystemObjectID != None:
                element.event(event)


                
            

