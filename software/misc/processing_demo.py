import cv2

img = cv2.imread('warzone.jpg', 0)
# blurred = cv2.medianBlur(img, 5)
# edges = cv2.Canny(img, 150, 200)
median = cv2.medianBlur(img, 25)
ret,thresh = cv2.threshold(median, 30, 255, cv2.THRESH_BINARY)

cv2.imwrite("thresh.jpg", thresh)