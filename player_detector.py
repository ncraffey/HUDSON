import cv2
import numpy as np

body_cascade = cv2.CascadeClassifier()
body_cascade.load(cv2.samples.findFile("haarcascade_fullbody.xml"))

def draw_rectangle(draw_point, size):
	cv2.rectangle(clip, draw_point, (draw_point[0] + size, draw_point[1] + size), (0, 0, 255), 0)

def process_image(frame):
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame_gray = cv2.equalizeHist(frame_gray)
	bodies = body_cascade.detectMultiScale(frame_gray)

	for (x, y, w, h) in bodies:
		center = (x + w//2, y + h//2)
		cv2.rectangle(frame, center, (center[0] + 50, center[1] + 50), (0, 0, 255), 0)

	
	return frame

while True:
	closed = False
	cap = cv2.VideoCapture('team_wipe.mov')
	cv2.namedWindow("clip")

	while True:
		success, clip = cap.read()
		if success:
			result = process_image(clip)
			cv2.imshow("clip", result)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				closed = True
				break
			elif cv2.waitKey(1) & 0xFF == ord('p'):
				while(cv2.waitKey(1) & 0xFF != ord('p')):
					pass
		else:
			break
	if closed:
		break

cap.release()
cv2.destroyAllWindows()
