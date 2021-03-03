import cv2
import numpy as np

drawing = True
draw_point = (0, 0)

# segment_image = semantic_segmentation()
# segment_image.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5") 

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
	params.maxThreshold = 200


	# Filter by Area.
	params.filterByArea = True
	params.minArea = 30
	# params.maxArea =

	# Filter by Circularity
	params.filterByCircularity = True
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


	# gray = cv2.cvtColor(clip, cv2.COLOR_BGR2GRAY)

	# kernel = np.ones((5,5),np.float32)/25
	# blur = cv2.medianBlur(frame, 5)


	# detector = cv2.SimpleBlobDetector()

	# keypoints = detector.detect(blur)

	# blobs = cv2.drawKeypoints(blur, keypoints, orig, (0,255,255), cv.DRAW_MATCHES_FLAGS_DEFAULT)

	# contours = cv2.findContours(blur)
	# hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	# binary_img = cv2.inRange(blur, (0, 0, 0.0), (40, 1, 1))

	# hue = hsv[:,:,0]
	# hue = hue+0.5
	# for wtf in hue:
		# print(wtf)
	# my_cond = hue[:,:]>4.0
	# hue[my_cond] = hue[my_cond]-1.0
	# hsv[:,:,0] = hue


	# kernel = np.ones((5,5),np.uint8)
	# canny = cv2.Canny(gray, 100, 200)
	# opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
	# ret, clip = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
	# return orig


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
			# clip = process_image(clip)
			# Detect blobs.
			keypoints = detector.detect(clip)

			# Draw detected blobs as red circles.
			# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
			# the size of the circle corresponds to the size of blob

			im_with_keypoints = cv2.drawKeypoints(clip, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

			# Show blobs
			cv2.imshow("Keypoints", im_with_keypoints)

			# if drawing:
			# 	draw_rectangle()

			# cv2.imshow('clip', clip)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				closed = True
				break
		else:
			break
	if closed:
		break

cap.release()
cv2.destroyAllWindows()
