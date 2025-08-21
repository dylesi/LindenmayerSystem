import pygame
import pygame_gui
from lsystemvariables import *



def redrawGUI(manager):
    #Draw Panels, hide initially

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

    #Sliders
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

    return CheckBoxObjects, outerPanel, innerPanel, selectSystem, selectSystemTextBox, generateButton, resetCamButton, quitButton, rotateLeftButton, rotateRightButton, angleSliderTextBox, iterationSlider, iterationSliderTextBox, drawLengthSlider, drawLengthSliderTextBox, drawWidthSlider, drawWidthSliderTextBox, BrightCheckbox, PastelCheckbox, DarkCheckbox, WarmCheckbox, MonochromeCheckbox, DeepGreenCheckbox