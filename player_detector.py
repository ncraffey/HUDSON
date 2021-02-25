import cv2

drawing = True
draw_point = (0, 0)

def mouse_event(event, x, y, flags, param):
	global draw_point, drawing
	if event == cv2.EVENT_MOUSEMOVE:
		if drawing:
			draw_point = (x, y)

while True:
	closed = False
	cap = cv2.VideoCapture('team_wipe.mov')
	cv2.namedWindow("clip")
	cv2.setMouseCallback('clip', mouse_event)
	while True:
		success, clip = cap.read()
		if success:
			if drawing:
				print("drawing rect at ", draw_point[0], draw_point[1])
				cv2.rectangle(clip, draw_point, (draw_point[0] + 80, draw_point[1] + 80), (0, 0, 255), 0)
				# gray = cv2.cvtColor(clip, cv2.COLOR_BGR2GRAY)
				# canny = cv2.Canny(gray, 10, 70)
				# ret, clip = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
			cv2.imshow('clip', clip)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				closed = True
				break
		else:
			break
	if closed:
		break

cap.release()
cv2.destroyAllWindows()
