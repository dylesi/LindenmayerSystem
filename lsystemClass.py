import pygame
import math
import random
import json
import pygame_gui

window_height = 1000
window_width = 1800
screen = pygame.display.set_mode((window_width,window_height))
window_surface = pygame.Surface((window_width,window_height))

class LSystem:
    def __init__(self, manager, windowSize):
        self.manager = manager
        self.iterations = 3
        self.maxIterations = 5
        self.windowWidth, self.windowHeight = windowSize
        self.center = (self.windowWidth / 2), (self.windowHeight / 2)
        self.fps = 60
        self.options = ""
        self.dragging = False
        
        #camera related vars
        self.zoom = 1
        self.zoomOffset = 1
        self.zoomStep = 0.3
        self.last_mousePos = pygame.Vector2(0, 0)

        #Gui Variables
        self.surfacePaddingX = 300
        self.surfacePaddingY = 50
        self.elementPaddingY = 70
        self.elementPaddingX = 10
        self.elementOffSet = 80
        self.isIterationSliderRebuilt = False
        self.isReset = False
        self.outerPanelWidth = 230
        self.outerPanelHeight = self.windowHeight - self.surfacePaddingY
        self.safetyMargin = 30

        #Drawing related variables
        self.isReadyToDraw = False
        self.drawingSpeed = 0
        self.drawingIndex = 0
        self.isDrawing = False

        #Main variables
        self.choice = "Select"
        self.defaultIterations = 3
        self.iterations = self.defaultIterations
        self.drawLength = 5
        self.drawWidth = 2
        self.startAngle = 0
        self.returnedCoordinates = []
        self.defaultDrawingStartAngle = 0
        self.choiceAngle = 0
        self.choiceAngleStep = 10
        self.colorTheme = "Default"
        self.mousePos = pygame.Vector2()
        self.is_running = True
        self.clock = pygame.time.Clock()

    #Load the ruleset from JSON and create coordinates for the graphic to draw
    def loadSystem(self):
        with open ("lsystems.json", "r") as f:
            lsystems = json.load(f)

        #Make a list with all the titles of systems in JSON
        self.options = []
        for name in lsystems:
            self.options.append(name)

        jsonSystemChoice = lsystems[self.choice]
        self.maxIterations = jsonSystemChoice["maxIterations"]
        self.axiom = jsonSystemChoice["axiom"]
        self.rules = jsonSystemChoice["rules"]
        self.turnAngle = jsonSystemChoice["turnAngle"]
        self.defaultDrawingStartAngle = jsonSystemChoice["startAngle"]

        self.lSystemMoves = self.lSystemRules(self.axiom,self.rules,self.iterations)
        self.returnedCoordinates = self.generateCoordinates(self.center, self.lSystemMoves, self.defaultDrawingStartAngle, self.choiceAngle, self.turnAngle, self.drawLength, self.colorTheme)
        #print(f"Moves: {len(self.lSystemMoves)}, coordinateData: {self.returnedCoordinates}")


    #Function for creating the movelist
    def lSystemRules(self, axiom, ruleDict, iterations):
        result = []
        if iterations < 1:
            return axiom
        else:               
            for char in axiom:
                if char in ruleDict:
                    result.append(ruleDict[char])
                else:
                    result.append(char)
        return self.lSystemRules("".join(result), ruleDict, iterations - 1)
    

    #Colour themes
    def colorSelector(self, choice):
        colorKvp = {
                'Default': [(255, 255), (255,255), (255, 255)],
                'Bright': [(100, 225), (100,255), (100, 255)],
                'Pastel': [(180, 225), (180,255), (180, 255)],
                'Dark': [(0, 100), (0,100), (0, 100)],
                'Warm': [(150, 225), (50,180), (0, 100)],
                'Ocean': [(0, 10), (175,255), (150, 225)],
                'Autumn': [(175, 255), (150,225), (0, 10)],
                'Deep Green': [(0, 10), (130,255), (50, 100)],
        }
        r = colorKvp[choice][0]
        g = colorKvp[choice][1]
        b = colorKvp[choice][2]
        
        return((random.randint(r[0], r[1]), random.randint(g[0], g[1]), random.randint(b[0], b[1])))

    #Create a tuple with start x,y coordinates, endpoint x,y coordinates and colour values
    #Todo:
    #Implement a proper way of handling unnecessary drawing with the "isconnected" flag
    def generateCoordinates(self, startPos, inputList:str, defaultStartDrawingAngle, startDrawingAngle:float, turnAngle:float, drawLength:float, colorTheme):

        defaultDrawingAngle = defaultStartDrawingAngle
        currentAngle = defaultDrawingAngle + startDrawingAngle
        returnedCoordinates = []
        fractalStack = []
        isConnected = True
        drawColor = self.colorSelector(colorTheme)

        for move in (inputList):
            if move == "[":
                fractalStack.append((startPos, currentAngle))

            elif move == "]":
                #isConnected = False
                currentAngle = fractalStack[-1][-1] 
                startPos = fractalStack[-1][0]
                fractalStack.pop(-1)

            elif move == "+":
                currentAngle += turnAngle
                if colorTheme != "Default":
                    drawColor = self.colorSelector(colorTheme)

            elif move == "-":
                currentAngle -= turnAngle
                if colorTheme != "Default":
                    drawColor = self.colorSelector(colorTheme)

            elif move in  ["0"]:
                isConnected = False
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)
                returnedCoordinates.append((startPos, endPos, isConnected, drawColor))
                startPos = endPos
                isConnected = True

            elif move in ["F","G","1"]:
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)
                returnedCoordinates.append((startPos, endPos, isConnected, drawColor))
                startPos = endPos
                isConnected = True

        return returnedCoordinates

    #calculating the new endpoint for the start x, y coordinates
    def newCoordinates(self, drawLength, x, y, angle):
        number = angle / 360 * (2 * math.pi)
        newY =  y + math.sin(number) * drawLength
        newX =  x + math.cos(number) * drawLength
        return(newX, newY)

    #Self explanatory
    def checkMouseNotOntopGUI(self):
        self.mousePos

        if self.mousePos.x < self.outerPanelWidth + self.safetyMargin and self.mousePos.y < self.outerPanelHeight + self.safetyMargin:
            return False
        else:
            return True
    
    #Generate the GUI
    #Maybe make a separate class out of this later????
    def generateGUI(self):
        self.outerPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(20, self.surfacePaddingY / 2, 230, self.windowHeight - self.surfacePaddingY), starting_height=1, manager=self.manager)
        self.innerPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(-3, 200, 230, 700 ), starting_height=0, manager=self.manager, parent_element=self.outerPanel, container=self.outerPanel)

        #Dropdown
        self.selectSystem = pygame_gui.elements.UIDropDownMenu(options_list=self.options, starting_option="Select", relative_rect=pygame.Rect((self.elementPaddingX, 60), (200, 35)), manager=self.manager, container=self.outerPanel)
        self.selectSystemTextBox = pygame_gui.elements.UITextBox(html_text="Select a system to draw!", relative_rect=pygame.Rect((self.elementPaddingX, 20), (200,35)), manager=self.manager, container=self.outerPanel)

        #Labels
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((self.elementPaddingX, -15), (200, 50)), text="Lindenmayer Systems",manager=self.manager, container=self.outerPanel)
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((self.elementPaddingX, 430), (200, 50)), text="Select Colour Style",manager=self.manager, container=self.innerPanel)

        #buttons
        self.generateButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX, self.innerPanel.get_relative_rect().height - self.elementPaddingY), (200, 50)), text='Generate!', manager=self.manager, container=self.innerPanel)
        self.resetButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX + 50, self.innerPanel.get_relative_rect().height - self.elementPaddingY - 30), (100, 25)), text='Reset', manager=self.manager, container=self.innerPanel)

        self.quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX + 50, self.innerPanel.get_relative_rect().height + 205), (100, 30)), text='Quit', manager=self.manager, container=self.outerPanel)
        self.rotateLeftButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX + 50, 50), (40, 30)), text='<', manager=self.manager, container=self.innerPanel)
        self.rotateRightButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX + 110, 50), (40, 30)), text='>', manager=self.manager, container=self.innerPanel)

        #Sliders
        self.angleSliderTextBox = pygame_gui.elements.UITextBox(html_text="Rotation angle: " + str(self.choiceAngle), relative_rect=pygame.Rect((self.elementPaddingX, 10), (200,35)), manager=self.manager, container=self.innerPanel)

        self.iterationSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet), (200, 25)), start_value=self.iterations, value_range=(1, 5), manager=self.manager, container=self.innerPanel)
        self.iterationSliderTextBox = pygame_gui.elements.UITextBox(html_text="Iterations " + str(self.iterations), relative_rect=pygame.Rect((self.elementPaddingX, 10 + self.elementOffSet), (200,35 )), manager=self.manager, container=self.innerPanel)

        self.drawLengthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet * 2), (200, 25)), start_value= self.drawLength, value_range=(5, 15), manager=self.manager, container=self.innerPanel)
        self.drawLengthSliderTextBox = pygame_gui.elements.UITextBox(html_text="Draw length " + str(self.drawLength), relative_rect=pygame.Rect((self.elementPaddingX, 10 + self.elementOffSet * 2), (200,35)), manager=self.manager, container=self.innerPanel)

        self.drawWidthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet * 3), (200, 25)), start_value=self.drawWidth, value_range=(1,5), manager=self.manager, container=self.innerPanel)
        self.drawWidthSliderTextBox = pygame_gui.elements.UITextBox(html_text="Draw width " + str(self.drawWidth), relative_rect=pygame.Rect((self.elementPaddingX, 10 + self.elementOffSet * 3), (200,35)), manager=self.manager, container=self.innerPanel)

        self.drawSpeedSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet * 4), (200, 25)), start_value= self.drawingSpeed, value_range=(0,100), manager=self.manager, container=self.innerPanel)
        self.drawSpeedTextBox = pygame_gui.elements.UITextBox(html_text=f"Draw speed {self.drawingSpeed} ms", relative_rect=pygame.Rect((self.elementPaddingX, 10 + self.elementOffSet * 4), (200,35)), manager=self.manager, container=self.innerPanel)

        #Checkboxes
        self.BrightCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX  , self.elementOffSet * 6), (25, 25)),text="Bright", manager=self.manager, container=self.innerPanel)
        self.PastelCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX, self.elementOffSet * 6.5), (25, 25)),text="Pastel", manager=self.manager, container=self.innerPanel)
        self.DarkCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX ,self.elementOffSet * 7), (25, 25)),text="Autumn", manager=self.manager, container=self.innerPanel)
        self.WarmCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX + 100,self.elementOffSet * 6), (25, 25)),text="Warm", manager=self.manager, container=self.innerPanel)
        self.MonochromeCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX + 100, self.elementOffSet * 6.5), (25, 25)),text="Ocean", manager=self.manager, container=self.innerPanel)
        self.DeepGreenCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX + 100, self.elementOffSet * 7), (25, 25)),text="Deep Green", manager=self.manager, container=self.innerPanel)

        #Checkboxes to be used to tick other checkboxes off if one is selected
        self.CheckBoxObjects = [
            self.BrightCheckbox,
            self.PastelCheckbox,
            self.DarkCheckbox,
            self.WarmCheckbox,
            self.MonochromeCheckbox,
            self.DeepGreenCheckbox,
        ]

        self.GUIElements = {
        "CheckBoxObjects": self.CheckBoxObjects,
        "outerPanel": self.outerPanel,
        "innerPanel": self.innerPanel,
        "selectSystem": self.selectSystem,
        "selectSystemTextBox": self.selectSystemTextBox,
        "generateButton": self.generateButton,
        "resetButton": self.resetButton,
        "quitButton": self.quitButton,
        "rotateLeftButton": self.rotateLeftButton,
        "rotateRightButton": self.rotateRightButton,
        "angleSliderTextBox": self.angleSliderTextBox,
        "iterationSlider": self.iterationSlider,
        "iterationSliderTextBox": self.iterationSliderTextBox,
        "drawLengthSlider": self.drawLengthSlider,
        "drawLengthSliderTextBox": self.drawLengthSliderTextBox,
        "drawWidthSlider": self.drawWidthSlider,
        "drawWidthSliderTextBox": self.drawWidthSliderTextBox,
        "drawSpeedSlider": self.drawSpeedSlider,
        "drawSpeedSliderTextBox": self.drawSpeedTextBox,
        "BrightCheckbox": self.BrightCheckbox,
        "PastelCheckbox": self.PastelCheckbox,
        "DarkCheckbox": self.DarkCheckbox,
        "WarmCheckbox": self.WarmCheckbox,
        "MonochromeCheckbox": self.MonochromeCheckbox,
        "DeepGreenCheckbox": self.DeepGreenCheckbox,
        }
        return self.GUIElements
    
    #Used to redraw the slider with a max value since Pygame_GUI does not have a way to set a max value after a slider has been created
    def rebuildIterationSlider(self, maxIterations=None):

        if maxIterations == None:
            maxIterations = self.maxIterations

        self.GUIElements["iterationSlider"].kill()
        self.iterations = self.defaultIterations
        self.GUIElements["iterationSlider"] = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet), (200, 25)), start_value=self.iterations, value_range=(1, maxIterations), manager=self.manager, container=self.innerPanel)
        self.GUIElements["iterationSliderTextBox"].set_text("Iterations " + str(self.iterations))
        self.isIterationSliderRebuilt = True