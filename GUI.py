import pygame
import pygame_gui

class GUIHandler:
    def __init__(self,manager, windowSize, mousePos):  
        self.mousePos = mousePos
        self.windowWidth, self.windowHeight = windowSize
        self.manager = manager
        self.surfacePaddingX = 300
        self.surfacePaddingY = 50
        self.elementPaddingY = 70
        self.elementPaddingX = 10
        self.elementOffSet = 80
        self.isIterationSliderRebuilt = False
        self.isReset = False
        self.outerPanelWidth = 230
        self.outerPanelHeight = self.windowHeight - self.surfacePaddingY
        self.safetyMargin = 30

    def generateGUI(self, options, choiceAngle, iterations, maxIterations, drawLength, drawWidth, drawingSpeed):
        self.outerPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(self.elementPaddingX, self.surfacePaddingY / 2, self.outerPanelWidth, self.windowHeight - self.surfacePaddingY), starting_height=1, manager=self.manager)
        self.innerPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(-3, 200, 230, 700 ), starting_height=0, manager=self.manager, parent_element=self.outerPanel, container=self.outerPanel)

        #Dropdown
        self.selectSystem = pygame_gui.elements.UIDropDownMenu(options_list=options, starting_option="Select", relative_rect=pygame.Rect((self.elementPaddingX, 60), (200, 35)), manager=self.manager, container=self.outerPanel)
        self.selectSystemTextBox = pygame_gui.elements.UITextBox(html_text="Select a system to draw!", relative_rect=pygame.Rect((self.elementPaddingX, 20), (200,35)), manager=self.manager, container=self.outerPanel)

        #Labels
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((self.elementPaddingX, -15), (200, 50)), text="Lindenmayer Systems",manager=self.manager, container=self.outerPanel)
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((self.elementPaddingX, 430), (200, 50)), text="Select Colour Style",manager=self.manager, container=self.innerPanel)

        #buttons
        self.generateButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX, self.innerPanel.get_relative_rect().height - self.elementPaddingY), (200, 50)), text='Generate!', manager=self.manager, container=self.innerPanel)
        self.resetButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX + 50, self.innerPanel.get_relative_rect().height - self.elementPaddingY - 30), (100, 25)), text='Reset', manager=self.manager, container=self.innerPanel)

        self.quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX + 50, self.innerPanel.get_relative_rect().height + 205), (100, 30)), text='Quit', manager=self.manager, container=self.outerPanel)
        self.rotateLeftButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX + 50, 50), (40, 30)), text='<', manager=self.manager, container=self.innerPanel)
        self.rotateRightButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.elementPaddingX + 110, 50), (40, 30)), text='>', manager=self.manager, container=self.innerPanel)

        #Sliders
        self.angleSliderTextBox = pygame_gui.elements.UITextBox(html_text="Rotation angle: " + str(choiceAngle), relative_rect=pygame.Rect((self.elementPaddingX, 10), (200,35)), manager=self.manager, container=self.innerPanel)

        self.iterationSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet), (200, 25)), start_value=iterations, value_range=(1, maxIterations), manager=self.manager, container=self.innerPanel)
        self.iterationSliderTextBox = pygame_gui.elements.UITextBox(html_text="Iterations " + str(iterations), relative_rect=pygame.Rect((self.elementPaddingX, 10 + self.elementOffSet), (200,35 )), manager=self.manager, container=self.innerPanel)

        self.drawLengthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet * 2), (200, 25)), start_value= drawLength, value_range=(1, 15), manager=self.manager, container=self.innerPanel)
        self.drawLengthSliderTextBox = pygame_gui.elements.UITextBox(html_text="Draw length " + str(drawLength), relative_rect=pygame.Rect((self.elementPaddingX, 10 + self.elementOffSet * 2), (200,35)), manager=self.manager, container=self.innerPanel)

        self.drawWidthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet * 3), (200, 25)), start_value=drawWidth, value_range=(1,5), manager=self.manager, container=self.innerPanel)
        self.drawWidthSliderTextBox = pygame_gui.elements.UITextBox(html_text="Draw width " + str(drawWidth), relative_rect=pygame.Rect((self.elementPaddingX, 10 + self.elementOffSet * 3), (200,35)), manager=self.manager, container=self.innerPanel)

        self.drawSpeedSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet * 4), (200, 25)), start_value=drawingSpeed, value_range=(0,100), manager=self.manager, container=self.innerPanel)
        self.drawSpeedTextBox = pygame_gui.elements.UITextBox(html_text=f"Draw speed {drawingSpeed} ms", relative_rect=pygame.Rect((self.elementPaddingX, 10 + self.elementOffSet * 4), (200,35)), manager=self.manager, container=self.innerPanel)

        #Checkboxes
        self.BrightCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX  , self.elementOffSet * 6), (25, 25)),text="Bright", manager=self.manager, container=self.innerPanel)
        self.PastelCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX, self.elementOffSet * 6.5), (25, 25)),text="Pastel", manager=self.manager, container=self.innerPanel)
        self.DarkCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX ,self.elementOffSet * 7), (25, 25)),text="Autumn", manager=self.manager, container=self.innerPanel)
        self.WarmCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX + 100,self.elementOffSet * 6), (25, 25)),text="Warm", manager=self.manager, container=self.innerPanel)
        self.MonochromeCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX + 100, self.elementOffSet * 6.5), (25, 25)),text="Ocean", manager=self.manager, container=self.innerPanel)
        self.DeepGreenCheckbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((self.elementPaddingX + 100, self.elementOffSet * 7), (25, 25)),text="Deep Green", manager=self.manager, container=self.innerPanel)

        #Checkboxes to be used to tick other checkboxes off if one is selected
        self.CheckBoxObjects = [
            self.BrightCheckbox,
            self.PastelCheckbox,
            self.DarkCheckbox,
            self.WarmCheckbox,
            self.MonochromeCheckbox,
            self.DeepGreenCheckbox,
        ]

        self.GUIElements = {
        "CheckBoxObjects": self.CheckBoxObjects,
        "outerPanel": self.outerPanel,
        "innerPanel": self.innerPanel,
        "selectSystem": self.selectSystem,
        "selectSystemTextBox": self.selectSystemTextBox,
        "generateButton": self.generateButton,
        "resetButton": self.resetButton,
        "quitButton": self.quitButton,
        "rotateLeftButton": self.rotateLeftButton,
        "rotateRightButton": self.rotateRightButton,
        "angleSliderTextBox": self.angleSliderTextBox,
        "iterationSlider": self.iterationSlider,
        "iterationSliderTextBox": self.iterationSliderTextBox,
        "drawLengthSlider": self.drawLengthSlider,
        "drawLengthSliderTextBox": self.drawLengthSliderTextBox,
        "drawWidthSlider": self.drawWidthSlider,
        "drawWidthSliderTextBox": self.drawWidthSliderTextBox,
        "drawSpeedSlider": self.drawSpeedSlider,
        "drawSpeedSliderTextBox": self.drawSpeedTextBox,
        "BrightCheckbox": self.BrightCheckbox,
        "PastelCheckbox": self.PastelCheckbox,
        "DarkCheckbox": self.DarkCheckbox,
        "WarmCheckbox": self.WarmCheckbox,
        "MonochromeCheckbox": self.MonochromeCheckbox,
        "DeepGreenCheckbox": self.DeepGreenCheckbox,
        }
        return self.GUIElements

    #Used to redraw the slider with a max value since Pygame_GUI does not have a way to set a max value after a slider has been created
    def rebuildIterationSlider(self, iterations, defaultIterations, maxIterations):

        self.GUIElements["iterationSlider"].kill()
        self.GUIElements["iterationSlider"] = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.elementPaddingX, 40 + self.elementOffSet), (200, 25)), start_value=defaultIterations, value_range=(1, maxIterations), manager=self.manager, container=self.innerPanel)
        self.GUIElements["iterationSliderTextBox"].set_text("Iterations " + str(defaultIterations))
        self.isIterationSliderRebuilt = True

    #Self explanatory
    def checkMouseNotOntopGUI(self):
        self.mousePos

        if self.mousePos.x < self.outerPanelWidth + self.safetyMargin and self.mousePos.y < self.outerPanelHeight + self.safetyMargin:
            return False
        else:
            return True