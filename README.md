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
<img width="2250" height="1250" alt="python_ipHO8ekrQK" src="https://github.com/user-attachments/assets/de1576fc-5a17-4528-a6c8-7bf2747be771" />
<img width="2250" height="1250" alt="python_R9Wn5yXeXP" src="https://github.com/user-attachments/assets/52792a5a-0320-49e2-b6ff-d31f62ac1d43" />

---

## Usage
- When you start the program, use the dropdown menu to select a drawing
- Use the sliders to manipulate the drawing
- Use the color checkboxes to draw the image in different themes
- Use the mousescroll wheel to zoom in and out
- Left click and drag pans the drawing around


## Installation
### Direct Download
- https://github.com/dylesi/LindenmayerSystem/archive/refs/heads/main.zip
### Dependencies
- You will need Pygame and Pygame-GUI
```.sh
pip install pygame
```

```.sh
pip install pygame_gui -U
```
## TODO
- Implement a system to draw the image in real time by set intervals
