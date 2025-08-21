import lsystemClass
import json
import pygame
import pygame_gui
import sys
from lsystemvariables import *
from drawSystemGUI import redrawGUI
import random
import math

pygame.init()
pygame.display.set_caption("Lindenmayer System")
manager = pygame_gui.UIManager((window_width, window_height))

#Main object
lSystemObject = lsystemClass.LSystem()
   
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
    
    lSystemMoves = lSystemObject.lSystemRules(start,rules,iterations)

    ForwardMoveCount = 0
    for move in lSystemMoves:
        if move == "F":
            ForwardMoveCount += 1
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
    screen.fill(screenFillColor)
    for startPos, endPos,  isConnected, drawColor in returnedCoordinates:

        newX = (pygame.math.Vector2(startPos) - center) * zoomOffset + center + camera_offset
        newY = (pygame.math.Vector2(endPos) - center) * zoomOffset + center + camera_offset

        if isConnected:
            pygame.draw.line(screen, drawColor, newX, newY, drawWidth)


# Import GUI elements from external file
CheckBoxObjects,outerPanel, innerPanel, selectSystem, selectSystemTextBox, generateButton, resetCamButton, quitButton, rotateLeftButton, rotateRightButton, angleSliderTextBox, iterationSlider, iterationSliderTextBox, drawLengthSlider, drawLengthSliderTextBox, drawWidthSlider, drawWidthSliderTextBox, BrightCheckbox, PastelCheckbox, DarkCheckbox, WarmCheckbox, MonochromeCheckbox, DeepGreenCheckbox = redrawGUI(manager)


innerPanel.hide()
outerPanelWidth = outerPanel.get_relative_rect().right
outerPanelHeight = outerPanel.get_abs_rect().bottom 

def checkMouseNotOntopGUI():
    global mousePos

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
            mousePos = pygame.Vector2(event.pos)
            if checkMouseNotOntopGUI():
                changeInMouseMov = mousePos - last_mousePos
                camera_offset += changeInMouseMov
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