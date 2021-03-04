# The HUDSON Project

Nick Craffey & John Craffey

___

## March 4th Update & Initial Demo

Since proposing the original project, we have started doing different experiments to get more comfortable with handling HDMI signals on the pynqboard as well as learn the image processing limitations of the processing system. We ran a few experiments to better understand which types of tasks take a long time to complete and therefore might benefit from hardware acceleration. We also learned which tasks execute quickly enough to possibly remain in software.

Overall the final design of the project is still up in the air, other than to say that we will be doing some kind of accelerated image processing on an HDMI input. Ideally we will still be detecting enemy players, but it is still unclear if the required processing can be done in the PL, and more experiments need to be done.

## Experiment Results

### Pass-through latency

We tied the HDMI in and out together and ran a stopwatch on a computer attached to the input. By taking a picture of the input and output screens, we were able to determine the approximate overall latency of the system to be near 100ms. This value is quite high for gaming, as it is noticible to the naked eye, but low enough that a game would be technically playable.

### Pass-through framerate

We timed a loop of a known amount of frames and divided the number of frames by the final count to determine a max frame rate of 60FPS, the refresh rate of our monitor. This number decreases as the amount of processing increases.

### PS Image processing

1. Face Detection
   
    Using a Jupyter notebook from the Pynq github, we were able to run and time a face detection algorithm that used FaceCascade in OpenCV. The framerate of this was less than 1FPS.

2. Blob Detection on Game Clip*

    Using some common techniques we were able to run a blob detection OpenCV program on a pre recorded game clip fed in via HDMI from a laptop. The frame rate of this experiment was about 5FPS when processing on every frame

3. Edge Detection on Game Clip*

    Using a Canny filter edge detection jupyter notebook from pynq's github, we were able to do an experiment similar to the blob detection, except with edge detection. This algorithm  was able to run at about 10FPS output when processing every frame.

    **Timing**

    We timed each of the algorithm steps in 2 and 3 in order to find out which steps were consuming most of the time and which ones were fast. For example, in a 20 second sample, 1 second might have been spent reading frames and 12 seconds might have been spent detecting blobs. This shows that optimizing the HDMI frame reads will give us less speedup then optimizing the blob detection.

    **Software Optimizations**

    By only running the heavy processing on every 5th frame, we were able to get the output framerate to about 30fps on these algorithms. While not processing every frame is not the ideal case, it shows a potential optimization if framerate becomes a constraint later on.
