import cv2
import numpy as np

def draw_rectangle(draw_point, size):
	cv2.rectangle(clip, draw_point, (draw_point[0] + size, draw_point[1] + size), (0, 0, 255), 0)

def threshold_image(frame):
	orig = frame

	ret,thresh1 = cv2.threshold(frame,125,255,cv2.THRESH_BINARY)

	return thresh1

while True:
	closed = False
	cap = cv2.VideoCapture('team_wipe.mov')
	cv2.namedWindow("clip")

	while True:
		success, clip = cap.read()

		if success:
			clip = threshold_image(clip)
			cv2.imshow("clip", clip)

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
