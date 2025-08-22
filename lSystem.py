import lsystemClass
import pygame
import pygame_gui
import sys

pygame.init()
pygame.display.set_caption("Lindenmayer System")

#Initial setup for screen, clock, and manager
screenFillColor = (26, 26, 26)
windowHeight = 1000
windowWidth = 1800
screen = pygame.display.set_mode((windowWidth,windowHeight))
center = (windowWidth // 2), (windowHeight / 2)
fps = 60
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((windowWidth, windowHeight))

#Main object
lSystemObject = lsystemClass.LSystem(manager, screen.get_size())
lSystemObject.loadSystem()
GUIElements = lSystemObject.generateGUI()
GUIElements["innerPanel"].hide()

#Custom event to be used for timing the drawing
DRAW_EVENT = pygame.event.custom_type()
is_running = True


def drawSystem(drawingIndex):
    startPos = lSystemObject.returnedCoordinates[lSystemObject.drawingIndex][0]
    endPos = lSystemObject.returnedCoordinates[lSystemObject.drawingIndex][1]
    isConnected = lSystemObject.returnedCoordinates[lSystemObject.drawingIndex][2]
    drawColor = lSystemObject.returnedCoordinates[lSystemObject.drawingIndex][3]

    newX = (pygame.math.Vector2(startPos) - center) * lSystemObject.zoomOffset + center + lSystemObject.camera_offset
    newY = (pygame.math.Vector2(endPos) - center) * lSystemObject.zoomOffset + center + lSystemObject.camera_offset

    if isConnected:
        pygame.draw.line(screen, drawColor, newX, newY, lSystemObject.drawWidth)

def drawSystemInstant():

    screen.fill(screenFillColor)
    for startPos, endPos,  isConnected, drawColor in lSystemObject.returnedCoordinates:

        newX = (pygame.math.Vector2(startPos) - center) * lSystemObject.zoomOffset + center + lSystemObject.camera_offset
        newY = (pygame.math.Vector2(endPos) - center) * lSystemObject.zoomOffset + center + lSystemObject.camera_offset

        if isConnected:
            pygame.draw.line(screen, drawColor, newX, newY, lSystemObject.drawWidth)


def establishDrawing():

    lSystemObject.isDrawing = False
    if lSystemObject.drawingSpeed == 0:
        lSystemObject.loadSystem()
        drawSystemInstant()

    else:
        lSystemObject.drawingIndex = 0
        screen.fill(screenFillColor)
        pygame.time.set_timer(DRAW_EVENT, 0)
        lSystemObject.loadSystem()
        pygame.time.set_timer(DRAW_EVENT, lSystemObject.drawingSpeed)
        lSystemObject.isDrawing = True
        #print("Drawing Established")



while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():

        manager.process_events(event)

        if event.type == pygame.QUIT:
            is_running = False
            sys.exit()

        if event.type == DRAW_EVENT and lSystemObject.isDrawing:

            tempReturnedCoordinates = lSystemObject.returnedCoordinates
            xres = sum(len(x[0]) for x in tempReturnedCoordinates) / 2

            if lSystemObject.drawingIndex >= int(xres):
                lSystemObject.isDrawing = False

            else:
                drawSystem(lSystemObject.drawingIndex)
                lSystemObject.drawingIndex += 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
                sys.exit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == GUIElements["generateButton"]:
                
                lSystemObject.isReset = False
                lSystemObject.isReadyToDraw = True
                establishDrawing()

            if event.ui_element == GUIElements["quitButton"]:
                lSystemObject.running = False
                sys.exit()

            if event.ui_element == GUIElements["resetButton"]:
                screen.fill(screenFillColor)
                lSystemObject.isReset = True
                lSystemObject.isDrawing = False
                lSystemObject.camera_offset = pygame.Vector2()
                lSystemObject.zoomOffset = 1
                lSystemObject.zoom = 1.0

            if event.ui_element == GUIElements["rotateRightButton"] and lSystemObject.isReadyToDraw and not lSystemObject.isReset:
                lSystemObject.choiceAngle = (lSystemObject.choiceAngle - lSystemObject.choiceAngleStep) % 360
                GUIElements["angleSliderTextBox"].set_text("Rotation angle: " + str(lSystemObject.choiceAngle))
                establishDrawing()

            if event.ui_element == GUIElements["rotateLeftButton"] and lSystemObject.isReadyToDraw and not lSystemObject.isReset:
                lSystemObject.choiceAngle = (lSystemObject.choiceAngle + lSystemObject.choiceAngleStep) % 360
                GUIElements["angleSliderTextBox"].set_text("Rotation angle: " + str(lSystemObject.choiceAngle))
                establishDrawing()

        if event.type == pygame.MOUSEWHEEL and lSystemObject.isReadyToDraw and not lSystemObject.isReset:
            if event.y > 0:
                lSystemObject.zoomOffset += lSystemObject.zoomStep
            else:            
                lSystemObject.zoomOffset = max(0.1, lSystemObject.zoomOffset - lSystemObject.zoomStep)  
            establishDrawing()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                lSystemObject.dragging = True
                lSystemObject.last_mousePos = pygame.Vector2(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                lSystemObject.dragging = False

        if event.type == pygame.MOUSEMOTION and lSystemObject.dragging and lSystemObject.isReadyToDraw and not lSystemObject.isReset:
            lSystemObject.mousePos = pygame.Vector2(event.pos)
            if lSystemObject.checkMouseNotOntopGUI():
                lSystemObject.changeInMouseMov = lSystemObject.mousePos - lSystemObject.last_mousePos
                lSystemObject.camera_offset += lSystemObject.changeInMouseMov
                lSystemObject.last_mousePos = lSystemObject.mousePos
                establishDrawing()

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:    
            if event.ui_element == GUIElements["iterationSlider"]: 
                GUIElements["iterationSlider"].set_current_value(event.value)
                GUIElements["iterationSliderTextBox"].set_text("Iterations " + str(event.value))
                lSystemObject.iterations = event.value

            if event.ui_element == GUIElements["drawLengthSlider"]:    
                GUIElements["drawLengthSlider"].set_current_value(event.value)
                GUIElements["drawLengthSliderTextBox"].set_text("Draw length " + str(event.value))
                lSystemObject.drawLength = event.value

            if event.ui_element == GUIElements["drawWidthSlider"]:    
                GUIElements["drawWidthSlider"].set_current_value(event.value)
                GUIElements["drawWidthSliderTextBox"].set_text("Draw width " + str(event.value))
                lSystemObject.drawWidth = event.value

            if event.ui_element == GUIElements["drawSpeedSlider"]:    
                GUIElements["drawSpeedSlider"].set_current_value(event.value)
                GUIElements["drawSpeedSliderTextBox"].set_text(f"Draw speed {event.value} ms")
                lSystemObject.drawingSpeed = event.value

        if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:

            lSystemObject.colorTheme = event.ui_element.text
            checkedBox = event.ui_element

            for checkBoxObj in GUIElements["CheckBoxObjects"]:
                if checkBoxObj != checkedBox:
                    checkBoxObj.set_state(False)


        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:

            lSystemObject.rebuildIterationSlider()
            screen.fill((screenFillColor))
            lSystemObject.isReadyToDraw = False
            lSystemObject.isIterationSliderRebuilt = False
            lSystemObject.isDrawing = False
            lSystemObject.iterations = lSystemObject.defaultIterations
            lSystemObject.choiceAngle = lSystemObject.defaultDrawingStartAngle
            GUIElements["angleSliderTextBox"].set_text("Rotation angle:  " + str(lSystemObject.choiceAngle))
            GUIElements["iterationSlider"].set_current_value(lSystemObject.defaultIterations)
            lSystemObject.zoomOffset = 1
            lSystemObject.camera_offset = pygame.Vector2(0, 0)
            
            if event.ui_element == GUIElements["selectSystem"]:
                selected_option = event.text
                if selected_option != "Select":
                    GUIElements["innerPanel"].show()
                if selected_option == "Select":
                    GUIElements["innerPanel"].hide()
                else:
                    lSystemObject.choice = event.text
            lSystemObject.loadSystem()

    manager.update(fps)    

    if lSystemObject.drawingSpeed == 0 and not lSystemObject.isIterationSliderRebuilt:
        lSystemObject.rebuildIterationSlider()
        lSystemObject.isIterationSliderRebuilt = True
        
    elif lSystemObject.drawingSpeed >= 1 and lSystemObject.isIterationSliderRebuilt:
        InstantMaxIterations = lSystemObject.maxIterations - round(lSystemObject.maxIterations / 3)
        lSystemObject.rebuildIterationSlider(InstantMaxIterations)
        lSystemObject.isIterationSliderRebuilt = False

    #------Updates, drawing and refreshes-------
    
    manager.draw_ui(screen)
    pygame.display.update()
