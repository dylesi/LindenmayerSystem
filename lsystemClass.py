import pygame
import math
import random

window_height = 1000
window_width = 1800
screen = pygame.display.set_mode((window_width,window_height))
window_surface = pygame.Surface((window_width,window_height))

class LSystem:
    def __init__(self):
        self.iterations = 0

    def lSystemRules(self, startString, ruleDict, iterations):
        newString = ""
        if iterations < 1:
            return startString
        else:               
            for char in startString:
                for key, value in ruleDict.items():
                    if char not in ruleDict:
                        newString += char
                        break
                    elif char == key:
                        newString += value
        return self.lSystemRules(newString, ruleDict, iterations - 1)
    

    def colorSelector(self, choice):
        colorKvp = {
                'Default': [(255, 255), (255,255), (255, 255)],
                'Bright': [(100, 225), (100,255), (100, 255)],
                'Pastel': [(180, 225), (180,255), (180, 255)],
                'Dark': [(0, 100), (0,100), (0, 100)],
                'Fiery': [(150, 225), (50,180), (0, 100)],
                'Green + Blue': [(0, 10), (175,255), (150, 225)],
                'Red + Green': [(175, 255), (150,225), (0, 10)],
                'Deep Green': [(0, 10), (130,255), (50, 100)],
        }
        r = colorKvp[choice][0]
        g = colorKvp[choice][1]
        b = colorKvp[choice][2]
        
        return((random.randint(r[0], r[1]), random.randint(g[0], g[1]), random.randint(b[0], b[1])))


    def generateCoordinates(self, startPos, inputList:str, defaultStartDrawingAngle, startDrawingAngle:float, turnAngle:float, drawLength:float, colorTheme):

        defaultDrawingAngle = defaultStartDrawingAngle
        currentAngle = defaultDrawingAngle + startDrawingAngle
        coordinateArray = []
        fractalStack = []
        isConnected = True
        drawColor = self.colorSelector(colorTheme)

        for move in (inputList):
            if move == "[":
                fractalStack.append((startPos, currentAngle))

            elif move == "]":
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
                coordinateArray.append((startPos, endPos, isConnected, drawColor))
                startPos = endPos
                isConnected = True

            elif move in ["F","G","1"]:
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)

                if startPos == endPos:
                    isConnected = False
                coordinateArray.append((startPos, endPos, isConnected, drawColor))

                startPos = endPos
                isConnected = True

        return coordinateArray

    def newCoordinates(self, drawLength, x, y, angle):
        number = angle / 360 * (2 * math.pi)
        newY =  y + math.sin(number) * drawLength
        newX =  x + math.cos(number) * drawLength
        return(newX, newY)
