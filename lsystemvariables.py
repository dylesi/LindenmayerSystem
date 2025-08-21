import pygame
import json


#Screen related variables
screenFillColor = (26, 26, 26)
window_height = 1000
window_width = 1800
screen = pygame.display.set_mode((window_width,window_height))
windowHeight = screen.get_height()
windowWidth = screen.get_width()
screen.fill(screenFillColor)
center = (windowWidth // 2), (windowHeight / 2)
fps = 60

#Gui Variables
surfacePaddingX = 300
surfacePaddingY = 50
elementPaddingY = 70
elementPaddingX = 10
elementOffSet = 80

#Main variables
choice = ""
iterations = 4
drawLength = 5
drawWidth = 2
startAngle = 0
drawMirrored = False
returnedCoordinates = []
defaultDrawingStartAngle = 0
choiceAngle = 0
choiceAngleStep = 20
isFractal = None
maxIterations = 5
colorTheme = "Default"
mousePos = pygame.Vector2()
is_running = True
clock = pygame.time.Clock()

#Json Load variables
with open ("lsystems.json", "r") as f:
    lsystems = json.load(f)

#Make a list with all the titles of systems
options = []
for name in lsystems:
    options.append(name)