import lsystemClass
import json
import pygame
import pygame_gui
import sys
import random
import math

pygame.init()
pygame.display.set_caption("Lindenmayer System")

#Screen Related Variables
window_height = 1000
window_width = 1800
surfacePaddingX = 300
surfacePaddingY = 50


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

#TESTVARIABLES
drawInterval = 1000
lastTimeDrawn = pygame.time.get_ticks()


#Screen related variables
screen = pygame.display.set_mode((window_width,window_height))
screenFillColor = (26, 26, 26)
screen.fill(screenFillColor)
manager = pygame_gui.UIManager((window_width, window_height))
windowHeight = screen.get_height()
windowWidth = screen.get_width()
center = (windowWidth // 2), (windowHeight / 2)
fps = 60

#Main object
lSystemObject = lsystemClass.LSystem()
   


#Load the JSON file containing rules
with open ("lsystems.json", "r") as f:
    lsystems = json.load(f)

#Make a list with all the titles of systems
options = []
for name in lsystems:
    options.append(name)



# Main Drawing Function
def establishSystem():

    global drawMirrored
    global choice
    global iterations
    global drawLength
    global drawWidth
    global choiceAngle
    global returnedCoordinates
    global isFractal
    global maxIterations
    global colorTheme
    global defaultDrawingStartAngle

    jsonSystemChoice = lsystems[choice]
    maxIterations = jsonSystemChoice["maxIterations"]
    start = jsonSystemChoice["start"]
    rules = jsonSystemChoice["rules"]
    turnAngle = jsonSystemChoice["turnAngle"]
    defaultDrawingStartAngle = jsonSystemChoice["startAngle"]
    
    #print(f"startString: {start}, ruleDict: {rules}, turnAngle: {turnAngle} iterations: {iterations}")
    lSystemMoves = lSystemObject.lSystemRules(start,rules,iterations)

    ForwardMoveCount = 0
    for move in lSystemMoves:
        if move == "F":
            ForwardMoveCount += 1
    #print(f"Moves: {lSystemMoves}, MoveCount: {ForwardMoveCount}. Length: {len(lSystemMoves)})")
    returnedCoordinates = lSystemObject.generateCoordinates(center, lSystemMoves, defaultDrawingStartAngle, choiceAngle, turnAngle, drawLength, colorTheme)

zoomOffset = 1
zoomStep = 0.5
camera_offset = pygame.Vector2(0, 0)
dragging = False
isOnTopGUI = False
last_mousePos = pygame.Vector2(0, 0)


def drawSystem():
    global zoomStep
    global zoomOffset
    counter = 0
    counterTwo = 0
    howManyCounter = 0
    screen.fill(screenFillColor)
    for startPos, endPos,  isConnected, drawColor in returnedCoordinates:
        howManyCounter += 1
        counterTwo += 1
        newX = (pygame.math.Vector2(startPos) - center) * zoomOffset + center + camera_offset
        newY = (pygame.math.Vector2(endPos) - center) * zoomOffset + center + camera_offset
        #print(returnedCoordinates)
        if isConnected:
            #print(f"nth:{howManyCounter}, startX,Y: {round(startPos[0], 2)} || {round(startPos[1], 2)} | endX,Y:{round(endPos[0], 2)} || {round(startPos[1], 2)} \n")
            counter += 1
            pygame.draw.line(screen, drawColor, newX, newY, drawWidth)
    #print(f"Current lines: {counter}, Total Lines: {counterTwo}")
    howManyCounter = 0
    counterTwo = 0
    counter = 0



#Draw Panels, hide initially
elementPaddingY = 70
elementPaddingX = 10
elementOffSet = 80
panel_width = 220
outerPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(20, surfacePaddingY / 2, 230, window_height - surfacePaddingY), starting_height=1, manager=manager)
innerPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(-3, 200, 230, 700 ), starting_height=0, manager=manager, parent_element=outerPanel, container=outerPanel)


#Dropdown
selectSystem = pygame_gui.elements.UIDropDownMenu(options_list=options, starting_option="Select", relative_rect=pygame.Rect((elementPaddingX, 60), (200, 35)), manager=manager, container=outerPanel)
selectSystemTextBox = pygame_gui.elements.UITextBox(html_text="Select a system to draw!", relative_rect=pygame.Rect((elementPaddingX, 20), (200,35)), manager=manager, container=outerPanel)

#Titles
pygame_gui.elements.UILabel(relative_rect=pygame.Rect((elementPaddingX, -15), (200, 50)), text="Lindenmayer Systems",manager=manager, container=outerPanel)
pygame_gui.elements.UILabel(relative_rect=pygame.Rect((elementPaddingX, 310), (200, 50)), text="Select Colour Style",manager=manager, container=innerPanel)


#buttons
generateButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((elementPaddingX, innerPanel.get_relative_rect().height - elementPaddingY), (200, 50)), text='Generate!', manager=manager, container=innerPanel)
resetCamButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((elementPaddingX + 50, innerPanel.get_relative_rect().height - elementPaddingY - 30), (100, 25)), text='Reset Cam', manager=manager, container=innerPanel)
quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((elementPaddingX, innerPanel.get_relative_rect().height + 205), (100, 30)), text='Quit', manager=manager, container=outerPanel)

rotateLeftButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((elementPaddingX + 50, 50), (40, 30)), text='<', manager=manager, container=innerPanel)
rotateRightButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((elementPaddingX + 110, 50), (40, 30)), text='>', manager=manager, container=innerPanel)
#Slider
#angleSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40), (200, 25)), start_value= 1, value_range=(0,360), manager=manager, container=innerPanel, click_increment=40)
angleSliderTextBox = pygame_gui.elements.UITextBox(html_text="Rotation angle: " + str(choiceAngle), relative_rect=pygame.Rect((elementPaddingX, 10), (200,35)), manager=manager, container=innerPanel)

iterationSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40 + elementOffSet), (200, 25)), start_value=iterations, value_range=(1,maxIterations), manager=manager, container=innerPanel)
iterationSliderTextBox = pygame_gui.elements.UITextBox(html_text="Iterations " + str(iterations), relative_rect=pygame.Rect((elementPaddingX, 10 + elementOffSet), (200,35 )), manager=manager, container=innerPanel)

drawLengthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40 + elementOffSet * 2), (200, 25)), start_value= drawLength, value_range=(5, 15), manager=manager, container=innerPanel)
drawLengthSliderTextBox = pygame_gui.elements.UITextBox(html_text="Draw length " + str(drawLength), relative_rect=pygame.Rect((elementPaddingX, 10 + elementOffSet * 2), (200,35)), manager=manager, container=innerPanel)

drawWidthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40 + elementOffSet * 3), (200, 25)), start_value= drawWidth, value_range=(1,5), manager=manager, container=innerPanel)
drawWidthSliderTextBox = pygame_gui.elements.UITextBox(html_text="Draw width " + str(drawWidth), relative_rect=pygame.Rect((elementPaddingX, 10 + elementOffSet * 3), (200,35)), manager=manager, container=innerPanel)


#Checkboxes
BrightCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((elementPaddingX + 25 , 40 + elementOffSet * 4), (25, 25)),text="Bright", manager=manager, container=innerPanel)

PastelCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((elementPaddingX + 25, elementOffSet * 5), (25, 25)),text="Pastel", manager=manager, container=innerPanel)

DarkCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((elementPaddingX + 25, elementOffSet * 5.5), (25, 25)),text="Red + Green", manager=manager, container=innerPanel)

WarmCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((elementPaddingX + 25, elementOffSet * 6), (25, 25)),text="Fiery", manager=manager, container=innerPanel)

MonochromeCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((elementPaddingX + 25, elementOffSet * 6.5), (25, 25)),text="Green + Blue", manager=manager, container=innerPanel)

DeepGreenCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((elementPaddingX + 25, elementOffSet * 7), (25, 25)),text="Deep Green", manager=manager, container=innerPanel)

CheckBoxObjects = []
CheckBoxObjects.append(BrightCheckbox)
CheckBoxObjects.append(PastelCheckbox)
CheckBoxObjects.append(DarkCheckbox)
CheckBoxObjects.append(WarmCheckbox)
CheckBoxObjects.append(MonochromeCheckbox)
CheckBoxObjects.append(DeepGreenCheckbox)

innerPanel.hide()


outerPanelWidth = outerPanel.get_relative_rect().right
outerPanelHeight = outerPanel.get_abs_rect().bottom 

def checkMouseNotOntopGUI():
    global mousePos
    #print(f"outerpWidth: {outerPanelWidth}, mouseposx: {mousePos.x}, outerpheight: {outerPanelHeight} mouseposy: {mousePos.y}")
    if mousePos.x < outerPanelWidth and mousePos.y < outerPanelHeight:
        return False
    else:
        return True

def rebuildIterationSlider():
    global iterationSlider
    iterationSlider.kill()
    iterations = 4
    iterationSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40 + elementOffSet), (200, 25)), start_value=iterations, value_range=(1,maxIterations), manager=manager, container=innerPanel)
    iterationSliderTextBox.set_text("Iterations " + str(iterations))



while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():

        
        manager.process_events(event)
            #ui_manager.process_events(event)

        if event.type == pygame.QUIT:
            is_running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
                sys.exit()

            if event.key == pygame.K_RIGHT:
                choiceAngle = (choiceAngle - choiceAngleStep) % 360
                angleSliderTextBox.set_text("Rotation angle: " + str(choiceAngle))
                establishSystem()
                drawSystem()

            if event.key == pygame.K_LEFT:
                choiceAngle = (choiceAngle + choiceAngleStep) % 360
                angleSliderTextBox.set_text("Rotation angle: " + str(choiceAngle))
                establishSystem()
                drawSystem()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == generateButton:
                establishSystem()
                drawSystem()

            if event.ui_element == quitButton:
                is_running = False
                sys.exit()
            
            if event.ui_element == resetCamButton:
                screen.fill(screenFillColor)
                camera_offset = pygame.Vector2()
                zoomOffset = 1
                zoom = 1.0
                establishSystem()
                drawSystem()

            if event.ui_element == rotateRightButton:
                choiceAngle = (choiceAngle - choiceAngleStep) % 360
                angleSliderTextBox.set_text("Rotation angle: " + str(choiceAngle))
                establishSystem()
                drawSystem()

            if event.ui_element == rotateLeftButton:
                choiceAngle = (choiceAngle + choiceAngleStep) % 360
                angleSliderTextBox.set_text("Rotation angle: " + str(choiceAngle))
                establishSystem()
                drawSystem()
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                zoomOffset += zoomStep
            else:            
                zoomOffset = max(0.1, zoomOffset - zoomStep)  
            drawSystem()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                dragging = True
                last_mousePos = pygame.Vector2(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                isOnTopGUI = False

        if event.type == pygame.MOUSEMOTION and dragging:
            #print(f"outerpWidth: {outerPanelWidth}, mouseposx: {mousePos.x}, outerpheight: {outerPanelHeight} mouseposy: {mousePos.y}")
            mousePos = pygame.Vector2(event.pos)
            if checkMouseNotOntopGUI():
                changeInMouseMov = mousePos - last_mousePos
                camera_offset += changeInMouseMov
                #print(f"mousePos: {mousePos} lastMousePos: {last_mousePos}, cOffset: {camera_offset}")
                last_mousePos = mousePos
                drawSystem()


        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:    
            if event.ui_element == iterationSlider: 
                iterationSlider.set_current_value(event.value)
                iterationSliderTextBox.set_text("Iterations " + str(event.value))
                iterations = event.value

            if event.ui_element == drawLengthSlider:    
                drawLengthSlider.set_current_value(event.value)
                drawLengthSliderTextBox.set_text("Draw length " + str(event.value))
                drawLength = event.value

            if event.ui_element == drawWidthSlider:    
                drawWidthSlider.set_current_value(event.value)
                drawWidthSliderTextBox.set_text("Draw width " + str(event.value))
                drawWidth = event.value

        if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:

            colorTheme = event.ui_element.text
            checkedBox = event.ui_element

            for checkBoxObj in CheckBoxObjects:
                if checkBoxObj != checkedBox:
                    checkBoxObj.set_state(False)

            # if event.ui_element == randomColorCheckbox:
            #     randomizeColors = True
        # if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:

        #     colorTheme = "Default"
        #     # if event.ui_element == randomColorCheckbox:
        #     #     randomizeColors = False

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:

            iterations = 4
            choiceAngle = defaultDrawingStartAngle
            angleSliderTextBox.set_text("Rotation angle:  " + str(choiceAngle))
            zoomOffset = 1
            camera_offset = pygame.Vector2(0, 0)
            
            screen.fill((screenFillColor))
            if event.ui_element == selectSystem:
                selected_option = event.text
                if selected_option != "Select":
                    innerPanel.show()
                if selected_option == "Select":
                    innerPanel.hide()
                else:
                    print(event.text)
                    choice = event.text
            establishSystem()
            rebuildIterationSlider()

    manager.update(time_delta)    


    #------Updates, drawing and refreshes-------
    
    clock.tick(fps)
    manager.draw_ui(screen)
    pygame.display.update()