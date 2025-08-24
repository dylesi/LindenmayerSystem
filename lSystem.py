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
        self.cameraOffset = pygame.Vector2(0,0)

        #Drawing related variables
        self.isReadyToDraw = False
        self.drawingSpeed = 0
        self.drawingIndex = 0
        self.isDrawing = False
        self.mousePos = pygame.Vector2()

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


    