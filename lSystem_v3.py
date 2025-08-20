import lsystemClass
import pygame
import pygame_gui
import sys
import random
pygame.init()
pygame.display.set_caption("Lindenmayer System")

#Screen Related Variables
window_height = 1000
window_width = 1800
surfacePaddingX = 300
surfacePaddingY = 50


#Main variables
choice = None
iterations = 2
drawLength = 2
drawWidth = 2
startAngle = 0
drawMirrored = False
returnedCoordinates = []
choiceAngle = 0
isFractal = None
randomizeColors = False

#Screen
screen = pygame.display.set_mode((window_width,window_height))
screen.fill((26, 26, 26))

#Surface for the drawing
#window_surface = pygame.Surface((window_width - surfacePaddingX, window_height - surfacePaddingY))
#window_surface.fill("Black")
#surface_center = (window_surface.get_width() /2), (window_surface.get_height() / 2)

# #Gui surface
# gui_surface = pygame.Surface((200, window_height - surfacePaddingY))
# gui_surface.fill((135, 134, 134))

manager = pygame_gui.UIManager((window_width, window_height))


#Font and text
font_size = 20
font = pygame.font.SysFont('arial', font_size, bold=True) 
title_text = "Lindenmayer Systems"
text_color = (255, 255, 255)  # white
text_surface = font.render(title_text, True, text_color)
text_rect = text_surface.get_rect(center=(135, 10))


is_running = True
windowHeight = screen.get_height()
windowWidth = screen.get_width()
center = (windowWidth // 2), (windowHeight / 2)

fps = 60
clock = pygame.time.Clock()
lSystemObject = lsystemClass.LSystem()
   



#------------------------------------------------------------------------------
#GUI DRAWING
#Default values
elementPaddingY = 70
elementPaddingX = 10
elementOffSet = 80


#Draw Panels, hide initially
panel_width = 220
outerPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(20, surfacePaddingY / 2, 230, window_height - surfacePaddingY), starting_height=1, manager=manager)
innerPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(-3, 200, 230, 700 ), starting_height=0, manager=manager, parent_element=outerPanel, container=outerPanel)
innerPanel.border_width = 0

#Dropdown
options = ["Dragon Curve", "Sierpinski Triangle", "Square Sierpinski", "Koch Curve", "Cross", "Square", "Crystal","Peano Curve","Levy Curve", "Quadratic Gosper", "Hexagonal Gosper", "Fractal Tree", "Fractal Plant", "Fractal Wheat", "Select",]
selectSystem = pygame_gui.elements.UIDropDownMenu(options_list=options, starting_option=options[-1], relative_rect=pygame.Rect((elementPaddingX, 60), (200, 35)), manager=manager, container=outerPanel)
selectSystemTextBox = pygame_gui.elements.UITextBox(html_text="Select a system to draw!", relative_rect=pygame.Rect((elementPaddingX, 20), (200,35)), manager=manager, container=outerPanel)

#Title
title_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((elementPaddingX, -15), (200, 50)), text="Lindenmayer Systems",manager=manager, container=outerPanel)
#buttons
generate_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((elementPaddingX, innerPanel.get_relative_rect().height - elementPaddingY), (200, 50)), text='Generate!', manager=manager, container=innerPanel)
quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((elementPaddingX, innerPanel.get_relative_rect().height + 205), (100, 30)), text='Quit', manager=manager, container=outerPanel)

#Sliders
angleSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40), (200, 25)), start_value= 1, value_range=(0,360), manager=manager, container=innerPanel)
angleSliderTextBox = pygame_gui.elements.UITextBox(html_text="Start angle " + str(choiceAngle), relative_rect=pygame.Rect((elementPaddingX, 10), (200,35)), manager=manager, container=innerPanel)

iterationSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40 + elementOffSet), (200, 25)), start_value=2, value_range=(1,30), manager=manager, container=innerPanel)
iterationSliderTextBox = pygame_gui.elements.UITextBox(html_text="Iterations " + str(iterations), relative_rect=pygame.Rect((elementPaddingX, 10 + elementOffSet), (200,35 )), manager=manager, container=innerPanel)

drawLengthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40 + elementOffSet * 2), (200, 25)), start_value= drawLength, value_range=(0.1,30.0), manager=manager, container=innerPanel)
drawLengthSliderTextBox = pygame_gui.elements.UITextBox(html_text="Draw Length " + str(drawLength), relative_rect=pygame.Rect((elementPaddingX, 10 + elementOffSet * 2), (200,35)), manager=manager, container=innerPanel)

drawWidthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((elementPaddingX, 40 + elementOffSet * 3), (200, 25)), start_value= drawWidth, value_range=(1,10), manager=manager, container=innerPanel)
drawWidthSliderTextBox = pygame_gui.elements.UITextBox(html_text="Draw Width " + str(drawWidth), relative_rect=pygame.Rect((elementPaddingX, 10 + elementOffSet * 3), (200,35)), manager=manager, container=innerPanel)

randomColorCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((elementPaddingX + 25 , 40 + elementOffSet * 4), (25, 25)),text="Randomize colors?", manager=manager, container=innerPanel)
#randomColorTextBox = pygame_gui.elements.UITextBox(html_text="Randomize colors?", relative_rect=pygame.Rect((elementPaddingX, 10 + elementOffSet * 4), (200,35)), manager=manager, container=innerPanel)


innerPanel.hide()



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

    inputRules = lSystemObject.chooseDrawing(choice)
    start = inputRules.get("start")
    rules = inputRules.get("rules")
    turnAngle = inputRules.get("turnAngle")
    startAngle = inputRules.get("startAngle")
    isFractal = inputRules.get("isFractal")


    print(f"startString: {start}, ruleDict: {rules}, turnAngle: {turnAngle} iterations: {iterations}")
    lSystemMoves = lSystemObject.lSystemRules(start,rules,iterations)
    #print(f"MOVET: {lSystemMoves}")
    
    returnedCoordinates = lSystemObject.generateCoordinates(screen, center, lSystemMoves, startAngle, turnAngle, drawLength, drawWidth)

zoomOffset = 1
zoomStep = 0.1

def randomColor():
    return((random.randint(0,255), random.randint(0,255), random.randint(0, 255)))

def drawSystem():
    global zoomStep
    global zoomOffset
    screen.fill((30,30,30))
    defaultDrawColor = "white"
    #scaled_points = transform_points(returnedCoordinates, zoom, offset)
    for x, y, isConnected in returnedCoordinates:

        newX = (pygame.math.Vector2(x) - center) * zoomOffset + center
        newY = (pygame.math.Vector2(y) - center) * zoomOffset + center

        #print(newX, newY, zoomOffset)
        if isConnected:
            if randomizeColors:
                defaultDrawColor = randomColor()
            pygame.draw.line(screen,defaultDrawColor, newX, newY, drawWidth)


while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
                sys.exit()
            if event.key == pygame.K_SPACE:
                zoom = 1.0
                zoomOffset = 0
                establishSystem()
                drawSystem()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == generate_button:
                screen.fill((30,30,30))
                zoom = 1.0
                establishSystem()
                drawSystem()
            if event.ui_element == quitButton:
                is_running = False
                sys.exit()
    
        if event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if event.y > 0:  # zoom in
                zoomOffset += zoomStep

            else:            # zoom out
                zoomOffset = max(zoomStep, zoomOffset - zoomStep)  
            drawSystem()

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:  
            if event.ui_element == angleSlider:    
                angleSlider.set_current_value(event.value)
                angleSliderTextBox.set_text("Start angle " + str(event.value))
                startAngle = event.value

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
            if event.ui_element == randomColorCheckbox:
                randomizeColors = True
        if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == randomColorCheckbox:
                randomizeColors = False

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == selectSystem:
                selected_option = event.text
                if selected_option != "Select":
                    innerPanel.show()
                if selected_option == "Select":
                    innerPanel.hide()
                else:
                    choice = options.index(event.text)
        manager.process_events(event)
    manager.update(time_delta)    



    #------Updates, drawing and refreshes-------
    

    clock.tick(fps)
    manager.draw_ui(screen)
    pygame.display.update()