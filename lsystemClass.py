
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
    
    #----------------------------------------------------------------------------------------
    def dragonCurve(self):
        print("DragonCurve")
        kvp = {
            'F': "F+G",
            'G': "F-G"
            }
        return {'start': "F", 'rules': kvp, 'turnAngle': 90,'startAngle': 270}

    def sierpinski(self):
        print("Sierpinski")
        kvp = {
            'F': "F-G+F+G-F",
            'G': "GG"
            }
        return {'start': "F-G-G", 'rules': kvp, 'turnAngle': 120, 'startAngle':120}

    def SquareSierpinski(self):
        print("Square Sierpinski")
        kvp = {
            'X': "XF-F+F-XF+F+XF-F+F-X"
            }
        return {'start': "F+XF+F+XF", 'rules': kvp, 'turnAngle': 90, 'startAngle':120}

    def kochCurve(self):
        print("Kochcurve")
        kvp = {
            'F': "F+F-F-F+F"
            }
        return {'start': "F", 'rules': kvp, 'turnAngle': 90, 'startAngle': 0}
    
    def Cross(self):
        print("Cross")
        kvp = {
            'F': "F+F-F-FF+F+F-F",
        }
        return {'start': "F+F+F+F", 'rules': kvp, 'turnAngle': 90, 'startAngle': 0}

    def Square(self):
        print("Square")
        kvp = {
            'F': "FF+F-F+F+FF",
        }
        return {'start': "F+F+F+F", 'rules': kvp, 'turnAngle': 90, 'startAngle': 45}

    def Crystal(self):
        print("Crystal")
        kvp = {
            'F': "FF+F++F+F"
        }
        return {'start': "F+F+F+F", 'rules': kvp, 'turnAngle': 90, 'startAngle': 45}

    def Rings(self):
        print("Rings")
        kvp = {
            'F': "FF+F+F+F+F+F-F"
        }
        return {'start': "F+F+F+F", 'rules': kvp, 'turnAngle': 90, 'startAngle': 45}

    def PeanoCurve(self):
        print("Peano Curve")
        kvp = {
            'X': "XFYFX+F+YFXFY-F-XFYFX",
            'Y': "YFXFY-F-XFYFX+F+YFXFY"
        }
        return {'start': "X", 'rules': kvp, 'turnAngle': 90, 'startAngle': 45}
    
    def LevyCurve(self):
        print("Lévy Curve")
        kvp = {
            'F': "-F++F-"
        }
        return {'start': "F", 'rules': kvp, 'turnAngle': 45, 'startAngle': 45}

    def QuadraticGosper(self):
        print("QuadraticGosper")
        kvp = {
            'X': "XFX-YF-YF+FX+FX-YF-YFFX+YF+FXFXYF-FX+YF+FXFX+YF-FXYF-YF-FX+FX+YFYF-",
            'Y': "+FXFX-YF-YF+FX+FXYF+FX-YFYF-FX-YF+FXYFYF-FX-YFFX+FX+YF-YF-FX+FX+YFY"
        }
        return {'start': "-YF", 'rules': kvp, 'turnAngle': 90, 'startAngle': 45}


    def HexagonalGosper(self):
        print("Hexagonal Gosper")
        kvp = {
            'X': "X+YF++YF-FX--FXFX-YF+",
            'Y': "-FX+YFYF++YF+FX--FX-Y"
        }
        return {'start': "XF", 'rules': kvp, 'turnAngle': 60, 'startAngle': 45}
    

    def fractalTree(self):
        print("FractalTree")
        kvp = {
            '1': "11",
            '0': "1[0]0"
        }
        return {'start': "0", 'rules': kvp, 'turnAngle': 45, 'startAngle': 270}
        
    def fractalPlant(self):
        print("FractalPlant")
        kvp = {
            'X': "F+[[X]-X]-F[-FX]+X",
            'F': "FF"
        }
        return {'start': "-X", 'rules': kvp, 'turnAngle': 25, 'startAngle': 270}
    
    def fractalWheat(self):
        print("FractalWheat")
        kvp = {
            'F': "F[-F]F[+F][F]",
        }
        return {'start': "F", 'rules': kvp, 'turnAngle': 25, 'startAngle': 270}
    

    #-------------------------------------------------------------------------------------------



    def chooseDrawing(self, choice):
        self.curveList = [self.dragonCurve, self.sierpinski, self.SquareSierpinski, self.kochCurve, self.Cross, self.Square, self.Crystal, self.Rings, self.PeanoCurve, self.LevyCurve, self.QuadraticGosper, self.HexagonalGosper, self.fractalTree, self.fractalPlant, self.fractalWheat]

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
        fractalStack = []
        isConnected = True

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
            if move == "0":
                isConnected = False
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)
                coordinateArray.append((startPos, endPos, isConnected))
                startPos = endPos
                isConnected = True

            if move == "F" or move =="G" or move == "1":
                endPos = self.newCoordinates(drawLength, startPos[0], startPos[1], currentAngle)
                coordinateArray.append((startPos, endPos, isConnected))
                startPos = endPos

        return coordinateArray

    def newCoordinates(self, drawLength, x, y, angle):
        number = angle / 360 * (2 * math.pi)
        newY =  y + math.sin(number) * drawLength
        newX =  x + math.cos(number) * drawLength
        return(newX, newY)
