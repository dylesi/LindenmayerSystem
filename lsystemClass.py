
import pygame
import json
import math

window_height = 1000
window_width = 1800
screen = pygame.display.set_mode((window_width,window_height))
window_surface = pygame.Surface((window_width,window_height))

class LSystem:
    def __init__(self):
        self.iterations = 0

    
    def lSystemRules(self, startString, ruleDict, iterations):
        newString = ""
        #print(f"startString: {startString}, ruleDict: {ruleDict}, iterations: {iterations}")
        if iterations < 1:
            return startString
        else:               
            for char in startString:
                for key, value in ruleDict.items():
                    #print(f"key: {key}. value: {value}")
                    if char not in ruleDict:
                        newString += char
                        break
                    elif char == key:
                        newString += value
        return self.lSystemRules(newString, ruleDict, iterations - 1)
    
    #Variable true/false for drawing coordinates


    def generateCoordinates(self, screen, startPos, inputList:str, startAngle:float, turnAngle:float, drawLength:float, width, color = "White"):
        currentAngle = startAngle
        coordinateArray = []
        fractalStack = []
        isConnected = True

        for move in inputList:

            if move == "[":
                fractalStack.append((startPos, currentAngle))

            elif move == "]":
                currentAngle = fractalStack[-1][-1] 
                startPos = fractalStack[-1][0]
                fractalStack.pop(-1)

            elif move == "+":
                currentAngle -= turnAngle

            elif move == "-":
                currentAngle += turnAngle
                
            elif move == "0":
                isConnected = False
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)
                coordinateArray.append((startPos, endPos, isConnected))
                startPos = endPos
                isConnected = True

            elif move in ["F","G","1"]:
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)
                coordinateArray.append((startPos, endPos, isConnected))
                startPos = endPos

        return coordinateArray

    def newCoordinates(self, drawLength, x, y, angle):
        number = angle / 360 * (2 * math.pi)
        newY =  y + math.sin(number) * drawLength
        newX =  x + math.cos(number) * drawLength
        return(newX, newY)
