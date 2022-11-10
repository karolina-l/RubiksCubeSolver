import numpy as np
import cv2 as cv
filename = './Images/EdgeDetection/sobelxy.png'
filename2 = './Images/EdgeDetection/canny.png'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst1 = cv.cornerHarris(gray,2,3,0.04)

img2 = cv.imread(filename2)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst2 = cv.cornerHarris(gray,2,3,0.04)

dst = np.intersect1d(dst1, dst2)
dst = cv.dilate(dst,None)
img[dst>0.01*dst.max()]=[0,0,255]

cv.imshow('dst',img)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
