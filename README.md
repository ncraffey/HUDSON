# The HUDSON Project

## Objective:

Utilize the  FPGA on the Xilinx Pynqboard to detect and draw a dynamic outline around enemies in a video game, alerting the player to their presense

## Inputs/Outputs

- HDMI input max 1080p60FPS
- HDMI output ideally same as input

## Possible Limitations

- If input framerate is too high
    - dropped frames
    - dropped player highlighting
    - latency could be too high

## Basic Design Plan

### On the Processor System (PS)

Running HUDSON on the PS is a proof of concept that all algorithms are working properly. If so a baseline output framerate will be established to compare against the accelerated version of HUDSON running on the PL.

1. Get comfortable with basic detection locally and on Pynqborad
2. Test on individual images from the game as input JPEGs from memory
3. Test on game clips (again input and output from memory)
4. Move onto real time HDMI data buffered through memory

### On the Programmable Logic (PL)

Running HUDSON on the PL is the final stage of development and the output framerate and accuracy of the algorithm will determine its real-world viability.

1. Repeat steps 2 - 4 from the PS design plan