# The HUDSON Project

Nick Craffey & John Craffey

___

## Abstract

Utilize the  processor system combined with the programmable logic on the Xilinx Pynq board detect enemies in a video game, alerting the player to their presense (i.e. by drawing a box around them). Data will be input and output via the onboard HDMI I/O.

___

## Overview

### Inputs/Outputs

- Pynq board HDMI input max 1080p60FPS
- Pynq board HDMI output frame rate is TBD
- IP will likely process a subsection of the HDMI signal at a time (200x200 squares, maybe in parallel, chip space permitting)

### Algorithms (Still TBD based on experimentation)

- Edge dectection (accelerated by PL)
  - Determine sequence of kernels that can successfully outline players while exluding other in game artifacts
- OpenCV?
  -  pynq has an overlay supporting some openCV operations, may be depricated post Vivado 2018<sub>[5]<sub>
  -  Preliminary experiments running OpenCV in python on pyqboard yield 0.3 FPS output
___

## Design Plan

### Work Distribution

HUDSON is a group project between John Craffey and Nick Craffey. There are many milestones in the project that mostly need to happen sequentially. Because of this, we plan to work together on each step of the design as opposed to dividing up the work. At different stages, one of us may have more experience than the other, which will create a constant back and forth in the collaboration. We do not currently know everything we need to know in order to deploy a functional final product, but are confident based on some research that the concept is possible and within the limits of our skills.

### Software Milestones (PS)

- Data Collection
  1. Determine the data we will use for training. This will most likely be a collection of in-game screenshots either showing enemy player models or "neutral" (no enemy).
  2. Devise a method of pre-processing the data (cropped to certain resolution? Where etc.)
  3. Determine features for our machine learning model (what constitutes a "positive" detection.)
  4. Generate validation data.
  5. Train the model (TODO: determine technology; TensorFlow? Apple CreateML?)

- Model Validation
  1. Test the model in Python on screenshots of gameplay unknown to the model.
  2. Use Python to draw boxes around enemy players on static images as detected by the ML model.
  3. Test the model on pre-recorded video and tweak until functioning as intended (dynamically).
  4. Test the model on realtime HDMI input with live gameplay from Xbox. Note performance issues.

### Hardware Milestones (PL)

Running HUDSON on the PL is the final stage of development and the output framerate and accuracy of the algorithm will determine its real-world viability.

- HDMI Overlay<sub>[6]<sub>
  1. Use the HDMI I/O to pass through a static image from a source to a monitor
  2. Use the HDMI I/O to pass through a video from a source to a monitor

    *NOTE: May run into HDCP issues. Be sure to test from multiple different HDMI sources (especially a game console) to ensure we can move onto next step)*

- Accelerating the Algorithm
  1. Design custom HLS overlay to handle the image processing of each from the HDMI input buffer
       - Implement the necesary operations for edge detection
       - Experiment with different optimizations
  2. Allow PL to process smaller subsections of the input signal in parallel to reduce latency and increase frame throughput
    
### Possible Limitations

- If Pynqboard cannot handle the processing in a reasonable time
    - Dropped frames
    - Torn frames
    - Dropped player highlighting
- Latency of the Pynq system could be too high to play game in real time
	- Will need optimizations on the PL. Speed is more important than area 

## Resources

1. [Face detection in 2 minutes using OpenCV & Python](https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81)

2. [Video demonstrating viability of player model detection in Call of DuTy: Modern Warfare](https://www.youtube.com/watch?v=Qif8g2Ib5pI)

3. [GitHub Repo for above video (code and Data)](https://github.com/darkmatter2222/COD-MW-2019-DNN)

4. [Use Python, Pynq and OpenCV to Implement Computer Vision](https://www.hackster.io/adam-taylor/use-python-Pynq-and-opencv-to-implement-computer-vision-361e1b)

5. [PYNQ Computer Vision Github](https://github.com/Xilinx/PYNQ-ComputerVision)

6. [PYNQ HDMI intro](https://github.com/Xilinx/PYNQ/blob/master/boards/Pynq-Z1/base/notebooks/video/hdmi_introduction.ipynb)
