
import pygame
import math

window_height = 1000
window_width = 1800
screen = pygame.display.set_mode((window_width,window_height))
window_surface = pygame.Surface((window_width,window_height))

class LSystem:
    def __init__(self):
        self.iterations = 0
    
    #----------------------------------------------------------------------------------------
    def dragonCurve(self):
        print("DragonCurve")
        dragonCurveRuleKvp = {
            'F': "F+G",
            'G': "F-G"
            }
        return {'start': "F", 'rules': dragonCurveRuleKvp, 'turnAngle': 90,'startAngle': 270, 'isFractal': False}

    def sierpinski(self):
        print("Sierpinski")
        sierpinskikvp = {
            'F': "F-G+F+G-F",
            'G': "GG"
            }
        return {'start': "F-G-G", 'rules': sierpinskikvp, 'turnAngle': 120, 'startAngle': 270, 'isFractal': False}

    def kochCurve(self):
        print("Kochcurve")
        kochCurveKvp = {
            'F': "F+F-F-F+F"
            }
        return {'start': "F", 'rules': kochCurveKvp, 'turnAngle': 90, 'startAngle': 0, 'isFractal': False}
    
    def fractalTree(self):
        print("FractalTree")
        fractalTreeKvp = {
            '1': "11",
            '0': "1[0]0"
        }
        return {'start': "0", 'rules': fractalTreeKvp, 'turnAngle': 45, 'startAngle': 270, 'isFractal': True}
        
    def fractalPlant(self):
        print("FractalPlant")
        fractalPlantKvp = {
            'X': "F+[[X]-X]-F[-FX]+X",
            'F': "FF"
        }
        return {'start': "-X", 'rules': fractalPlantKvp, 'turnAngle': 25, 'startAngle': 270, 'isFractal': True}
    #-------------------------------------------------------------------------------------------
    
    def chooseDrawing(self, choice):
        self.curveList = [self.dragonCurve, self.sierpinski, self.kochCurve, self.fractalTree, self.fractalPlant]
        self.executable = self.curveList[choice]
        return self.executable()
    
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


    def generateCoordinates(self, screen, startPos, inputList, startAngle, turnAngle, drawLength, width, color = "White"):
        print(f"start: {startAngle}, turn: {turnAngle}")
        currentAngle = startAngle
        coordinateArray = []
        for move in inputList:
            if move == "+":
                currentAngle -= turnAngle
            if move == "-":
                currentAngle += turnAngle
            if move == "F" or move =="G":
                #print(f"currentturnAngle: {currentturnAngle}, turnAngle: {turnAngle}")
                #print(f"angle when adding coordinates: {turnAngle}")
                #print(startPos,startPos[0], startPos[1], currentAngle)
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)
                #pygame.draw.line(screen, color, start_pos, end_pos, width)
                #turtle.fd(drawLength)
                #print(f"Starpos: {start_pos} Endpos: {end_pos}")
                coordinateArray.append(endPos)
                startPos = endPos
        return coordinateArray

    def generateFractalCoordinates(self, screen, startPos, inputList, startAngle, turnAngle, drawLength, width, color = "White"):
        print(f"start: {startAngle}, turn: {turnAngle}")
        currentAngle = startAngle
        fractalStack = []
        coordinateArray = []
        cutStem = 0

        for move in inputList:
            if move == "[":
                fractalStack.append((startPos, currentAngle))
                currentAngle -= turnAngle
                print(f"now at first {fractalStack}")
            if move == "]":
                currentAngle = fractalStack[-1][1] + turnAngle
                startPos = fractalStack[-1][0]
                fractalStack.pop(-1)
                print(f"now at second {fractalStack}")
            if move == "+":
                currentAngle -= turnAngle
            if move == "-":
                currentAngle += turnAngle
            if move == "F" or move =="G" or move == "1" or move == "0":
                
                #print(f"currentturnAngle: {currentturnAngle}, turnAngle: {turnAngle}")
                #print(f"angle when adding coordinates: {turnAngle}")
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)
                #pygame.draw.line(screen, color, startPos, endPos, width)
                #turtle.fd(drawLength)
                #print(f"Starpos: {start_pos} Endpos: {end_pos}")
                coordinateArray.append((startPos, endPos))
                startPos = endPos
        
        return coordinateArray

    def newCoordinates(self, drawLength, x, y, angle):
        number = angle / 360 * (2 * math.pi)
        newY =  y + math.sin(number) * drawLength
        newX =  x + math.cos(number) * drawLength
        return(newX, newY)
