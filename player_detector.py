import cv2
import numpy as np

drawing = True
draw_point = (0, 0)

def mouse_event(event, x, y, flags, param):
	global draw_point, drawing
	if event == cv2.EVENT_MOUSEMOVE:
		if drawing:
			draw_point = (x, y)

def draw_rectangle():
	cv2.rectangle(clip, draw_point, (draw_point[0] + 80, draw_point[1] + 80), (0, 0, 255), 0)

def blob_detector_params():
	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()

	# Change thresholds
	params.minThreshold = 10
	params.maxThreshold = 80


	# Filter by Area.
	params.filterByArea = True
	params.minArea = 80
	# params.maxArea =

	# Filter by Circularity
	params.filterByCircularity = False
	params.minCircularity = 0.1

	# Filter by Convexity
	params.filterByConvexity = False
	params.minConvexity = 0.87

	# Filter by Inertia
	params.filterByInertia = False
	params.minInertiaRatio = 0.01

	# Create a detector with the parameters
	return params

def process_image(frame):
	orig = frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# blur = cv2.medianBlur(gray, 5)
	# ret, clip = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY)
	# clip = cv2.Canny(gray, 60, 120, L2gradient=True) 
	return gray

while True:
	closed = False
	cap = cv2.VideoCapture('team_wipe.mov')
	cv2.namedWindow("clip")
	cv2.setMouseCallback('clip', mouse_event)
	while True:
		success, clip = cap.read()
		if success:
			params = blob_detector_params()
			detector = cv2.SimpleBlobDetector_create(params)
			gray = process_image(clip)
			# Detect blobs.
			keypoints = detector.detect(gray)

			# Draw detected blobs as red circles.
			# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
			# the size of the circle corresponds to the size of blob

			im_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

			# Show blobs
			cv2.imshow("Keypoints", im_with_keypoints)

			# if drawing:
			# 	draw_rectangle()

			if cv2.waitKey(1) & 0xFF == ord('q'):
				closed = True
				break
		else:
			break
	if closed:
		break

cap.release()
cv2.destroyAllWindows()
