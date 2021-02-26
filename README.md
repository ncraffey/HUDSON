# The HUDSON Project

Nick Craffey & John Craffey

___

## Abstract

Utilize the processing system in conjunction with the programmable logic on the Xilinx Pynq board to detect enemies in a video game (*Call of Duty*) and alerting the player to their presence by drawing a box around them. Data will be input and output via the onboard HDMI I/O.

___

## Overview

### Inputs/Outputs

- Pynq board HDMI input max 1080p60FPS
- Pynq board HDMI output frame rate is TBD
- IP will likely process a subsection of the HDMI signal at a time (possibly in parallell; subdivide the screen into NxN squares of pixels for processing.)

### Algorithms (Still TBD based on experimentation)

- Edge dectection:
  1. Blur/smooth the image to reduce noise
  2. Convert to grayscale
  3. Use known edge/contour detection algorithms in conjunction with some kind of segmentation (most likely color segmentation) in order to best determine where the target image is.
  4. Overlay this hightight of the target image onto the original image.
- OpenCV
  -  pynq has an overlay supporting some openCV operations, may be deprecated post-Vivado 2018<sub>[5]<sub>
  -  the most computationally expensive task is going to be edge detection, and the underlying math can most likely be hardware-accelerated. 
  -  Preliminary experiments running OpenCV in python on pyqboard yield 0.3 FPS output......lots of room for improvement!
___

## Design Plan

### Work Distribution

HUDSON is a group project between John Craffey and Nick Craffey (we're cousins.) A number of milesones in this project must happen sequentially (designing/testing the software, designing/testing hardware overlay), so we plan to work together on each step of the design as opposed to dividing up the work. At different stages, one of us may have more experience than the other, which will create a constant back and forth in the collaboration. Our skills are complementary in different niches of hardware and software. We do not currently know everything we need to know in order to deploy a functional final product, but are confident based on some research and early prototyping that the concept is possible and within the limits of our skills.

### Software Milestones (PS)

So far we have enabled a test video stream to play via python, and we've set up the software infrastructure to draw a box on the image wherever we want, and have been using opencv to test out various prebuilt image processing approaches. So far, something like the following procedure looks promising:

1. Store the current frame.
2. Blur the frame to reduce noise.
3. Convert the blurred frame to a different colorspace (black+white, or more intense)
4. Use known algorithms (canny, contours) to detect edges.
5. Iterate on this design so we are mostly finding *only* the edges we want
6. Overlay these highlighted edges onto the originally stored frame.

This method avoids using anything too out-of-scope (intensive AI modeling) but still a large amount of image processing. We are looking into which part of the above procedure is most ripe for acceleration, or even if multiple steps could be accelerated. We do not expect this to run smoothly purely in software, but it will be interesting to see just how low the performance is. We'll do everything we can to keep things as performant as possible before hardware acceleration, as responsivenss is key in our case (playing a game in real-time.)

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
