import cv2
import os
import numpy as np



img = cv2.imread('./img/test_mask/result_1.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


#upper_yello = np.array([104,17,0])
#lower_yello = np.array([196,56 ,15])
upper = np.array([203, 18, 18])
lower = np.array([10, 0, 0])

img_mask = cv2.inRange(hsv, lower, upper)


img_color = cv2.bitwise_and(img, img, mask=img_mask)


cv2.imwrite('./img/result.png', img_color)
cv2.imwrite('./img/result1.png', img_mask)
cv2.imwrite('./img/result0.png', hsv)


