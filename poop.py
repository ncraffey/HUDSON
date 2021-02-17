import cv2

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while cap.isOpened():
	success, img = cap.read()
	if success:
		# Convert into grayscale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Detect faces
		faces = face_cascade.detectMultiScale(gray, 1.1, 4)
		# Draw rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

		# Display the output
		cv2.imshow('img', img)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
