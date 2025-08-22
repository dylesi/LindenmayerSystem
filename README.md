# Lindenmayer Systems

## Description 
An **L-system** or **Lindenmayer system** is a system that is used to generated different repeating and fractal patterns.
An L-system consists of:
- An **alphabet** of symbols that can be used to make strings
- A **collection of rules** that expand each symbol into some larger string of symbols  
- An initial **axiom** string from which to begin construction  
- A **mechanism for translating** the generated characters within a string to produce a pattern.

L-systems were introduced and developed in **1968** by *Aristid Lindenmayer*, a Hungarian theoretical biologist and botanist at the University of Utrecht. Lindenmayer used L-systems to describe the behaviour of plant cells and to model the growth processes of plant development.  

Beyond botany, L-systems have also been used to:
- Model the **morphology** of a variety of organisms  
- Generate **self-similar fractals**  

---

### Example: Quadratic Gosper

- **Axiom**:  
  `-YF`

- **Rules**:<br>
  `-X → XFX-YF-YF+FX+FX-YF-YFFX+YF+FXFXYF-FX+YF+FXFX+YF-FXYF-YF-FX+FX+YFYF-`<br>
  `Y → +FXFX-YF-YF+FX+FXYF+FX-YFYF-FX-YF+FXYFYF-FX-YFFX+FX+YF-YF-FX+FX+YFY`
- **Turn Angle**:  
  `90°`

- "-" decrease the turn angle amount
- "+" add the turn angle amount
- "F" draw forward
- "X" no actions taken, only used as a variable to generate more of the code
---

## Project Goals

- Learn different ways of implementing coding principles
- Explore and implement Lindenmayer systems  
- Visualize fractal and plant-like structures  
- Provide examples that the user can manipulate
- And mainly to learn more and have fun!

---

## Example Output
<img width="2250" height="1250" alt="python_Obg2HFVXPM" src="https://github.com/user-attachments/assets/5cc0c8db-a350-4812-875f-990c323a5182" />
<img src="https://i.imgur.com/y1votcB.gif" width="2250" height="1250" />

---

## Usage
- When you start the program, use the dropdown menu to select a drawing
- Use the sliders to manipulate the drawing
- Use the color checkboxes to draw the image in different themes
- Use the mousescroll wheel to zoom in and out
- Left click and drag pans the drawing around
- Use drawing speed to determine how fast the image generates (0 is instant)

## Installation
### Direct Download
- https://github.com/dylesi/LindenmayerSystem/archive/refs/heads/main.zip
### Dependencies
- You will need Pygame and Pygame-GUI and Python to be installed.
```.sh
pip install pygame
```

```.sh
pip install pygame_gui -U
```
## TODO
- Implement a system to draw the image in real time by set intervals
- Implement variables in a more robust way
- Try to make it an executable
