# The HUDSON Project

Nick Craffey & John Craffey

___

## March 4th Update & Initial Demo

Since proposing the original project, we have started doing different experiments to get more comfortable with handling HDMI signals on the pynqboard as well as learn the image processing limitations of the processing system. We ran a few experiments to better understand which types of tasks take a long time to complete and therefore might benefit from hardware acceleration. We also learned which tasks execute quickly enough to possibly remain in software.

Overall the final design of the project is still up in the air, other than to say that we will be doing some kind of accelerated image processing on an HDMI input. Ideally we will still be detecting enemy players, but it is still unclear if the required processing can be done in the PL, and more experiments need to be done.

## Experiment Results

### Pass-through latency

We tied the HDMI in and out together and ran a stopwatch on a computer attached to the input. By taking a picture of the input and output screens, we were able to determine the approximate overall latency of the system to be near 100ms. This value is quite high for gaming, as it is noticible to the naked eye, but low enough that a game would be technically playable.

```
from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *

base = BaseOverlay("base.bit")
hdmi_in = base.video.hdmi_in
hdmi_out = base.video.hdmi_out

hdmi_in.configure()
hdmi_out.configure(hdmi_in.mode)

hdmi_in.start()
hdmi_out.start()

hdmi_in.tie(hdmi_out)

hdmi_out.close()
hdmi_in.close()
```

### Pass-through framerate

We timed a loop of a known amount of frames and divided the number of frames by the final count to determine a max frame rate of 60FPS, the refresh rate of our monitor. This number decreases as the amount of processing increases.

```
import time

numframes = 600
start = time.time()

for _ in range(numframes):
    f = hdmi_in.readframe()
    hdmi_out.writeframe(f)
    
end = time.time()
print("Frames per second:  " + str(numframes / (end - start)))
```

### PS Image processing

1. Face Detection
   
    Using a Jupyter notebook from the Pynq github, we were able to run and time a face detection algorithm that used FaceCascade in OpenCV. The framerate of this was less than 1FPS.

```
import cv2

frameWidth = 640
frameHeight = 480


# Load the cascade
face_cascade = cv2.CascadeClassifier('/home/xilinx/jupyter_notebooks/haarcascade_frontalface_default.xml')


start = time.time()
numframes = 10

for _ in range(numframes):
    success = 1
    img = hdmi_in.readframe()
    if success:
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the output
        hdmi_out.writeframe(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
end = time.time()
print("Frames per second:  " + str(numframes / (end - start)))
```

2. Blob Detection on Game Clip*

    Using some common techniques we were able to run a blob detection OpenCV program on a pre recorded game clip fed in via HDMI from a laptop. The frame rate of this experiment was about 5FPS when processing on every frame

```
import time

numframes = 480
start = time.time()
timestamp = time.time()
timeReadingFrames = 0
timeBlurring = 0
timeKeypoints = 0
timeDrawingPoints = 0
for ff in range(numframes):
    timestamp = time.time()
    clip = hdmi_in.readframe()
    timeReadingFrames += (time.time() - timestamp)
    
    # Only do the processing every 5th frame, else just pass the frame through
    # this increases framerate from ~6 FPS to ~25
    # TODO: get the box to stay for an extra two frames after
    # TODO: Hardware accelerate
    # TODO: make the bubbles actually form around enemies
    if (ff % 5 == 0):
        timestamp = time.time()
        blurred = process_image(clip)
        timeBlurring += (time.time() - timestamp)

        timestamp = time.time()
        keypoints = detector.detect(blurred)
        timeKeypoints += (time.time() - timestamp)

        timestamp = time.time()
        clip_with_keypoints = cv2.drawKeypoints(blurred, keypoints, clip, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        timeDrawingPoints += (time.time() - timestamp)

            #cv2.imshow("Keypoints", clip)

        outframe = hdmi_out.newframe()
        outframe[:] = clip
        hdmi_out.writeframe(outframe)
    else:
        hdmi_out.writeframe(clip)
    
end = time.time()
print("total time: " + str(end-start))
print("Frames per second:  " + str(numframes / (end - start)))
print("time reading frames: " + str(timeReadingFrames))
print("time blurring : " + str(timeBlurring))
print("time keypoints: " + str(timeKeypoints))
print("Time drawing points: " + str(timeDrawingPoints))
```

3. Edge Detection on Game Clip*

    Using a Canny filter edge detection jupyter notebook from pynq's github, we were able to do an experiment similar to the blob detection, except with edge detection. This algorithm  was able to run at about 10FPS output when processing every frame.

```
import cv2
import numpy as np
import time
numframes = 960
grayscale = np.ndarray(shape=(hdmi_in.mode.height, 
                              hdmi_in.mode.width), dtype=np.uint8)
blurred = np.ndarray(shape=(hdmi_in.mode.height, 
                              hdmi_in.mode.width), dtype=np.uint8)
result = np.ndarray(shape=(hdmi_in.mode.height, 
                           hdmi_in.mode.width), dtype=np.uint8)

start = time.time()
timestamp = time.time()
timeBW = 0
timeGauss = 0
timeCanny = 0
timeColor = 0

for ff in range(numframes):
    inframe = hdmi_in.readframe()
    
    
    if (ff % 5 == 0):
        timestamp = time.time()
        cv2.cvtColor(inframe,cv2.COLOR_RGB2GRAY,dst=grayscale)
        timeBW += (time.time() - timestamp)

        inframe.freebuffer()

        timestamp = time.time()
        cv2.GaussianBlur(grayscale,(5,5),0,dst=blurred)
        timeGauss += (time.time() - timestamp)

        timestamp = time.time()
        cv2.Canny(grayscale, 100, 110, edges=result)
        timeCanny += (time.time() - timestamp)
    
        outframe = hdmi_out.newframe()

        timestamp = time.time()
        cv2.cvtColor(result, cv2.COLOR_GRAY2RGB,dst=outframe)
        timeColor += (time.time() - timestamp)

        hdmi_out.writeframe(outframe)
    else :
        hdmi_out.writeframe(inframe)
end = time.time()
print("total time: " + str(end-start))
print("Frames per second:  " + str(numframes / (end - start)))
print("time to B&W: " + str(timeBW))
print("time Gaussian blur : " + str(timeGauss))
print("time canny: " + str(timeCanny))
print("Time back to clr: " + str(timeColor))

```

**Timing**

We timed each of the algorithm steps in 2 and 3 in order to find out which steps were consuming most of the time and which ones were fast. For example, in a 20 second sample, 1 second might have been spent reading frames and 12 seconds might have been spent detecting blobs. This shows that optimizing the HDMI frame reads will give us less speedup then optimizing the blob detection.

**Software Optimizations**

By only running the heavy processing on every 5th frame, we were able to get the output framerate to about 30fps on these algorithms. While not processing every frame is not the ideal case, it shows a potential optimization if framerate becomes a constraint later on.
