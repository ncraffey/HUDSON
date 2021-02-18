# The HUDSON Project

## Objective:

Utilize the  FPGA on the Xilinx Pynqboard to detect and draw a dynamic outline around enemies in a video game, alerting the player to their presense

## Inputs/Outputs

- HDMI input max 1080p60FPS
- HDMI output ideally same as input

## Design Plan

### Software Milestones (PS)

**Data Collection:**
1. Determine the data we will use for training. This will most likely be a collection of in-game screenshots either showing enemy player models or "neutral" (no enemy).
2. Devise a method of pre-processing the data (cropped to certain resolution? Where etc.)
3. Determine features for our machine learning model (what constitutes a "positive" detection.)
4. Generate validation data.
5. Train the model (TODO: determine technology; TensorFlow? Apple CreateML?)

**Model Validation:**
1. Test the model in Python on screenshots of gameplay unknown to the model.
2. Use Python to draw boxes around enemy players on static images as detected by the ML model.
3. Test the model on pre-recorded video and tweak until functioning as intended (dynamically).
4. Test the model on realtime HDMI input with live gameplay from Xbox. Note performance issues.

### Hardware Milestones (PL)

Running HUDSON on the PL is the final stage of development and the output framerate and accuracy of the algorithm will determine its real-world viability.

**HDMI Overlay**
1. Use the HDMI I/O to pass through a static image from a source to a monitor
2. Use the HDMI I/O to pass through a video from a source to a monitor

    *NOTE: May run into HDCP issues. Be sure to test from multiple different HDMI sources (especially a game console) to ensure we can move onto next step)*

**Accelerating the Algorithm**
1. Design custom HLS overlay to handle the image processing of each from the HDMI input buffer

## Work Distribution

HUDSON is a group project between John Craffey and Nick Craffey. There are many milestones in the project that mostly need to happen sequentially. Because of this, we plan to work together on every step of the design as opposed to dividing up the work. At different stages, one of us may have more experience than the other, which will create a constant back and forth in the collaboration. We do not currently know everything we need to know in order to deploy a functional final product, but are confident based on some research that the concept is possible and within the limits of our skills as well as the performance of the Pynqboard.

## Possible Limitations

- If input framerate is too high
    - dropped frames
    - dropped player highlighting
    - latency could be too high

## Resources

1. [Face detection in 2 minutes using OpenCV & Python](https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81)

2. [Video demonstrating viability of player model detection in Call of DuTy: Modern Warfare](https://www.youtube.com/watch?v=Qif8g2Ib5pI)

3. [GitHub Repo for above video (code and Data)](https://github.com/darkmatter2222/COD-MW-2019-DNN)
