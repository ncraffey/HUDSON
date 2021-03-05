import cv2
import numpy as np

def draw_rectangle(draw_point, size):
	cv2.rectangle(clip, draw_point, (draw_point[0] + size, draw_point[1] + size), (0, 0, 255), 0)

def process_image(frame):
	orig = frame

	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	blur = cv2.blur(gray, ksize=(25,25))
	_, binary = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
	
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
