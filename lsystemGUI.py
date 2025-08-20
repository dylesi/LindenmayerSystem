import pygame_gui
import pygame
from lSystem_v3 import options, window_height, surfacePaddingX, surfacePaddingY, manager, choiceAngle, drawLength,iterations,drawWidth
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
#options = ["Dragon Curve", "Sierpinski Triangle", "Square Sierpinski", "Koch Curve", "Cross", "Square", "Crystal","Peano Curve","Levy Curve", "PentaPlexity" "Quadratic Gosper", "Hexagonal Gosper", "Fractal Tree", "Fractal Plant", "Fractal Wheat", "Select",]
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